from pathlib import Path
import sys,unittest,sqlite3,csv,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze import summarize,load_data
ROOT=Path(__file__).resolve().parents[1]
class FunnelTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:');self.db.row_factory=sqlite3.Row
        self.db.executescript('''CREATE TABLE leads(lead_id TEXT,created_at TEXT,source TEXT,service TEXT,owner TEXT);
        CREATE TABLE activities(lead_id TEXT,occurred_at TEXT,activity_type TEXT);
        CREATE TABLE quotes(lead_id TEXT,quoted_at TEXT);
        CREATE TABLE bookings(lead_id TEXT,booked_at TEXT);
        INSERT INTO leads VALUES ('L1','2026-01-01T08:00','Website','Clean','A'),('L2','2026-01-01T08:00','Phone','Clean','A'),('L3','2026-07-30T08:00','Phone','Clean','A');
        INSERT INTO activities VALUES ('L1','2026-01-01T13:00','First response'),('L1','2026-01-02T08:00','Follow-up'),('L1','2026-01-03T08:00','Follow-up');
        INSERT INTO quotes VALUES ('L1','2026-01-04T08:00');
        INSERT INTO bookings VALUES ('L1','2026-01-06T08:00');''')
    def tearDown(self):self.db.close()
    def rows(self):return [dict(r) for r in self.db.execute((ROOT/'sql/funnel.sql').read_text(),{'snapshot':'2026-07-31T23:59:59'})]
    def test_many_activities_do_not_multiply_leads_or_bookings(self):
        rows=self.rows();self.assertEqual(len(rows),3);self.assertEqual(sum(r['booked'] for r in rows),1)
    def test_nonresponders_retained_with_blank_duration(self):
        row=self.rows()[1];self.assertEqual(row['responded'],0);self.assertIsNone(row['response_hours'])
    def test_immature_lead_excluded_from_denominator(self):
        summary=summarize(self.rows());self.assertEqual(summary['leads'],2);self.assertEqual(summary['immature_excluded'],1)
    def test_threshold_changes_late_count_without_changing_conversion(self):
        rows=self.rows();a=summarize(rows,4);b=summarize(rows,8)
        self.assertEqual(a['late'],1);self.assertEqual(b['late'],0);self.assertEqual(a['booked'],b['booked'])
    def test_late_booking_excluded_from_thirty_day_window(self):
        self.db.execute("UPDATE bookings SET booked_at='2026-02-10T08:00'")
        self.assertEqual(self.rows()[0]['booked'],0)
    def test_booking_exactly_at_thirty_days_is_included(self):
        self.db.execute("UPDATE bookings SET booked_at='2026-01-31T08:00:00'")
        self.assertEqual(self.rows()[0]['booked'],1)
    def test_booking_one_second_after_thirty_days_is_excluded(self):
        self.db.execute("UPDATE bookings SET booked_at='2026-01-31T08:00:01'")
        self.assertEqual(self.rows()[0]['booked'],0)
    def test_cohort_exactly_thirty_days_old_is_mature(self):
        self.db.execute("UPDATE leads SET created_at='2026-07-01T23:59:59' WHERE lead_id='L3'")
        self.assertEqual(self.rows()[2]['mature'],1)
    def test_cohort_one_second_under_thirty_days_is_immature(self):
        self.db.execute("UPDATE leads SET created_at='2026-07-02T00:00:00' WHERE lead_id='L3'")
        self.assertEqual(self.rows()[2]['mature'],0)

class SourceIntegrityTests(unittest.TestCase):
    def fixture(self,path,booking_lead='L2',quote_id='Q1'):
        tables={
          'leads':(['lead_id','created_at','source','service','owner'],[
            ['L1','2026-01-01T08:00','Website','Clean','A'],['L2','2026-01-01T08:00','Phone','Clean','A']]),
          'activities':(['activity_id','lead_id','occurred_at','activity_type'],[['A1','L1','2026-01-01T09:00','First response']]),
          'quotes':(['quote_id','lead_id','quoted_at','quoted_amount'],[['Q1','L1','2026-01-02T08:00',100]]),
          'bookings':(['booking_id','lead_id','quote_id','booked_at'],[['B1',booking_lead,quote_id,'2026-01-03T08:00']])}
        for name,(headers,rows) in tables.items():
            with (path/f'{name}.csv').open('w',newline='',encoding='utf-8') as f:
                writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)
    def test_booking_referencing_another_leads_quote_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(Path(tmp));db,checks=load_data(tmp)
            try:
                failure=next(c for c in checks if c['check']=='Booking validity')
                self.assertEqual(failure['status'],'FAIL')
                self.assertIn('1 mismatched',failure['detail'])
            finally:db.close()
    def test_booking_with_nonexistent_quote_fails_foreign_key_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(Path(tmp),booking_lead='L1',quote_id='Q999');db,checks=load_data(tmp)
            try:self.assertTrue(any(c['check']=='bookings keys' and c['status']=='FAIL' for c in checks))
            finally:db.close()
if __name__=='__main__':unittest.main()
