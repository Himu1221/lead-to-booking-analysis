# Improvement roadmap

## Implemented in this revision
| Improvement | Business value | Verification |
|---|---|---|
| Overview, Response Review, and Quality views | Separates executive overview from record investigation and definitions | Navigation and shared-filter checks |
| Monthly originating-cohort conversion trend | Shows variation over time without mixing acquisition and booking periods | Uses the same mature cohort definition as the SQL funnel |
| Unanswered and late categories | Makes both exception types directly accessible | Distinct counts and threshold validation |
| Search and pagination | Makes all matching exceptions reachable | Page boundaries and empty-state checks |
| Lead journey detail | Lets a reviewer inspect first recorded stage timestamps | Uses derived source dates, with missing stages shown explicitly |
| CSV exports | Supports handoff and independent inspection | Exports all matched review rows, not just the visible page, with filter context |

## Next analytical improvements worth doing
1. **Capture non-booking reasons from a real business.** Validate a reason taxonomy and distinguish declined quotes, no contact, capacity constraints, duplicates, and open decisions. Current stage gaps cannot identify causes.
2. **Add a staffed-hours calendar after discovery.** Model opening hours, holidays, handoffs, and response-due rules. Elapsed clock hours should not be labeled a business-hours SLA.
3. **Pilot the proposed workflow with an actual stakeholder.** Record interview evidence, changes to requirements, and UAT feedback with permission. Keep hypothetical requirements distinct from elicited ones.
4. **Measure the reminder intervention.** Agree eligibility, baseline, rollout/comparison design, sample size, duration, and workload guardrails before testing. Do not assume that faster responses cause higher conversion.
5. **Add uncertainty estimates if comparisons will drive decisions.** Report sample sizes and confidence intervals with a documented method; avoid ranking very small cohorts as reliable winners.

Operational CRM functionality such as editing ownership, sending reminders, and storing personal contact details belongs in a separately scoped implementation after discovery. This portfolio currently demonstrates analysis and proposed process improvement.
