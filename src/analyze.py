from pathlib import Path
from datetime import datetime
import csv,json,sqlite3,statistics,hashlib

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT='2026-07-31T23:59:59'

def load_data(data_dir=None):
    data_dir = Path(data_dir) if data_dir is not None else ROOT/'data'
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.executescript('''PRAGMA foreign_keys=ON;
    CREATE TABLE leads(lead_id TEXT PRIMARY KEY,created_at TEXT NOT NULL,source TEXT NOT NULL,service TEXT NOT NULL,owner TEXT NOT NULL);
    CREATE TABLE activities(activity_id TEXT PRIMARY KEY,lead_id TEXT NOT NULL REFERENCES leads,occurred_at TEXT NOT NULL,activity_type TEXT NOT NULL);
    CREATE TABLE quotes(quote_id TEXT PRIMARY KEY,lead_id TEXT NOT NULL UNIQUE REFERENCES leads,quoted_at TEXT NOT NULL,quoted_amount REAL NOT NULL);
    CREATE TABLE bookings(booking_id TEXT PRIMARY KEY,lead_id TEXT NOT NULL UNIQUE REFERENCES leads,quote_id TEXT NOT NULL UNIQUE REFERENCES quotes,booked_at TEXT NOT NULL);''')
    checks=[]
    def check(name,passed,detail):checks.append(dict(check=name,status='PASS' if passed else 'FAIL',detail=detail))
    for table,datefield in [('leads','created_at'),('activities','occurred_at'),('quotes','quoted_at'),('bookings','booked_at')]:
        with (data_dir/f'{table}.csv').open(newline='',encoding='utf-8') as f:
            reader=csv.DictReader(f); records=list(reader)
        fields=[r['name'] for r in db.execute(f'PRAGMA table_info({table})')]
        check(table+' schema',reader.fieldnames==fields,'CSV headers must match the documented schema.')
        check(table+' completeness',all(all(r.get(k) not in (None,'') for k in fields) for r in records),'Required cells may not be empty.')
        valid=True
        for r in records:
            try:valid=valid and datetime.fromisoformat(r[datefield])<=datetime.fromisoformat(SNAPSHOT)
            except (ValueError,TypeError):valid=False
        check(table+' timestamps',valid,'All timestamps must parse and be at or before the fixed snapshot.')
        if any(c['status']=='FAIL' for c in checks):return db,checks
        try:db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" for _ in fields)})',[[r[k] for k in fields] for r in records])
        except sqlite3.IntegrityError as e:
            check(table+' keys',False,str(e));return db,checks
        check(table+' keys',True,f'{len(records)} records; primary, foreign, and documented unique keys enforced.')
    violations=db.execute('''SELECT COUNT(*) FROM activities a JOIN leads l USING(lead_id) WHERE a.occurred_at<l.created_at''').fetchone()[0]
    check('Activity sequence',violations==0,f'{violations} activities before lead creation.')
    invalid_quotes=db.execute('''SELECT COUNT(*) FROM quotes q JOIN leads l USING(lead_id) WHERE q.quoted_amount<0 OR q.quoted_at<l.created_at OR NOT EXISTS(SELECT 1 FROM activities a WHERE a.lead_id=q.lead_id AND a.activity_type='First response' AND a.occurred_at<=q.quoted_at)''').fetchone()[0]
    check('Quote validity',invalid_quotes==0,f'{invalid_quotes} quotes with invalid amount, sequence, or missing preceding response.')
    invalid_bookings=db.execute('''SELECT COUNT(*) FROM bookings b JOIN quotes q USING(quote_id) WHERE b.lead_id<>q.lead_id OR b.booked_at<q.quoted_at''').fetchone()[0]
    check('Booking validity',invalid_bookings==0,f'{invalid_bookings} mismatched quote/lead links or bookings before quote.')
    return db,checks

def summarize(rows,target=4):
    mature=[r for r in rows if r['mature']]
    times=[r['response_hours'] for r in mature if r['responded']]
    return dict(leads=len(mature),responded=sum(r['responded'] for r in mature),quoted=sum(r['quoted'] for r in mature),booked=sum(r['booked'] for r in mature),median_response_hours=statistics.median(times) if times else None,late=sum(r['responded'] and r['response_hours']>target for r in mature),no_response=sum(not r['responded'] for r in mature),immature_excluded=len(rows)-len(mature))

def main():
    out=ROOT/'reports';out.mkdir(exist_ok=True)
    db,checks=load_data()
    (out/'quality.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    if any(c['status']=='FAIL' for c in checks):raise ValueError('Data validation failed. See reports/quality.json; analytical reports were not refreshed.')
    rows=[dict(r) for r in db.execute((ROOT/'sql/funnel.sql').read_text(),{'snapshot':SNAPSHOT})]
    if len(rows)!=db.execute('SELECT COUNT(*) FROM leads').fetchone()[0]:raise ValueError('Lead grain changed after joins')
    if not all(r['booked']<=r['quoted']<=r['responded'] for r in rows):raise ValueError('Funnel stage ordering failed')
    db.execute('CREATE TABLE lead_funnel AS '+(ROOT/'sql/funnel.sql').read_text(),{'snapshot':SNAPSHOT})
    sources=[dict(r) for r in db.execute((ROOT/'sql/source_performance.sql').read_text())]
    totals=summarize(rows)
    if sum(s['leads'] for s in sources)!=totals['leads'] or sum(s['booked'] for s in sources)!=totals['booked']:raise ValueError('Grouped totals do not reconcile')
    metadata={'snapshot':SNAPSHOT,'simulation_seed':1221,'source':'Included deterministic simulation; no external data','source_checksums':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data').glob('*.csv'))},'grain':'One row per originating lead; events rolled up before joins','validation':'Input keys, completeness, timestamps, sequence, funnel grain, stage ordering, and grouped reconciliation passed'}
    (out/'results.json').write_text(json.dumps(dict(metadata=metadata,summary=totals,sources=sources),indent=2),encoding='utf-8')
    with (out/'lead_funnel.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    best=sources[0];gaps=[('Inquiry to response',totals['leads']-totals['responded']),('Response to quote',totals['responded']-totals['quoted']),('Quote to booking',totals['quoted']-totals['booked'])];gap=max(gaps,key=lambda x:x[1])
    report=f'''# Executive brief — Lead-to-Booking Improvement

## Decision
Propose a shared inquiry queue with assigned ownership, response reminders, and standardized quote follow-up. Validate the assumed workflow with an actual business before implementing changes. Do not interpret this simulation as evidence of a real operational problem.

## Computed baseline in the simulation
- Mature leads: {totals['leads']}; excluded immature leads: {totals['immature_excluded']}.
- Responses within 30 days: {totals['responded']}; quotes: {totals['quoted']}; bookings: {totals['booked']}.
- Lead-to-booking conversion: {totals['booked']/totals['leads']:.1%}.
- Median first-response time among responded mature leads: {totals['median_response_hours']:.1f} elapsed hours.
- {totals['late']} responded leads exceed the proposed four-hour threshold; {totals['no_response']} lack a response within 30 days. These groups are reported separately.
- The largest stage gap is {gap[0]}: {gap[1]} originating leads. A gap does not establish a reason for non-progression, nor prove an avoidable loss.
- {best['source']} has the highest observed lead-to-booking rate ({best['lead_to_booking']:.1%}, {best['leads']} leads). Source differences are partly designed into the simulation; this finding is not a marketing recommendation.

## Options and tradeoffs
| Option | Benefit | Constraint |
|---|---|---|
| Shared spreadsheet and daily review | Low implementation effort; tests field definitions | Manual reminders and weak history controls |
| Configure a lightweight CRM | Ownership, reminders, and activity history | Requires tool selection, operating cost, training, and data migration |
| Build a custom system | Tailored workflow | Development and maintenance effort unlikely to be justified without further discovery |

Recommended sequence: validate needs with a business owner, pilot a shared queue, and use the evidence to decide whether CRM configuration is warranted. No vendor selection or purchase is included.

## Measurement plan
Use originating-lead cohorts and a fixed 30-day conversion window. Evaluate response coverage, median first-response time, lead-to-booking conversion, and quote-to-booking conversion. Track workload, duplicate inquiries, and completed-service quality as guardrails once those operational data sources exist. Select evaluation duration, comparison method, and acceptable thresholds before launch. Randomize reminder rollout if feasible; a simple before/after comparison can be confounded by seasonality, source mix, and staffing.

## Missing evidence and proposed discovery
Interview the owner and inquiry handlers to validate inquiry sources, current tools, staffing hours, handoffs, reasons for non-booking, duplicate inquiries, and consent/contact preferences. Review a sample of real records with permission. The four-hour setting is a demonstration assumption, not a negotiated SLA. Business-hours rules require an actual staffing calendar.

## Quality and limits
{metadata['validation']}. All data is fictional. Activity joins are aggregated to prevent duplicate lead counts. No booking is treated as realized revenue. A 30-day stage gap can contain leads that book later, decline, or remain open; the source does not classify every reason. Outcomes are not simulated as a function of response delay, and no causal uplift is estimated. Full source checks are in quality.json.
'''
    (out/'executive-brief.md').write_text(report,encoding='utf-8')
    template=(ROOT/'src/booking-workspace.html').read_text(encoding='utf-8')
    template=template.replace('__ROWS__',json.dumps(rows).replace('<','\\u003c')).replace('__QUALITY__',json.dumps(checks).replace('<','\\u003c'))
    (out/'dashboard.html').write_text(template,encoding='utf-8')
    print(json.dumps(totals,indent=2))
    db.close()

if __name__=='__main__':main()
