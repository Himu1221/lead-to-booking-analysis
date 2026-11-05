# Executive brief — Lead-to-Booking Improvement

## Decision
Propose a shared inquiry queue with assigned ownership, response reminders, and standardized quote follow-up. Validate the assumed workflow with an actual business before implementing changes. Do not interpret this simulation as evidence of a real operational problem.

## Computed baseline in the simulation
- Mature leads: 360; excluded immature leads: 0.
- Responses within 30 days: 323; quotes: 241; bookings: 132.
- Lead-to-booking conversion: 36.7%.
- Median first-response time among responded mature leads: 4.8 elapsed hours.
- 198 responded leads exceed the proposed four-hour threshold; 37 lack a response within 30 days. These groups are reported separately.
- The largest stage gap is Quote to booking: 109 originating leads. A gap does not establish a reason for non-progression, nor prove an avoidable loss.
- Referral has the highest observed lead-to-booking rate (42.7%, 89 leads). Source differences are partly designed into the simulation; this finding is not a marketing recommendation.

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
Input keys, completeness, timestamps, sequence, funnel grain, stage ordering, and grouped reconciliation passed. All data is fictional. Activity joins are aggregated to prevent duplicate lead counts. No booking is treated as realized revenue. A 30-day stage gap can contain leads that book later, decline, or remain open; the source does not classify every reason. Outcomes are not simulated as a function of response delay, and no causal uplift is estimated. Full source checks are in quality.json.
