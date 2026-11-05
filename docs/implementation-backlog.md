# Prioritized implementation backlog

Priorities and acceptance criteria are proposed for the fictional brief. This is a handoff-ready starting point for discovery, not an approved or fully estimated production backlog. Effort labels are relative discussion prompts, not delivery commitments.

| Story | Proposed priority | Dependencies | Relative effort | Status |
|---|---|---|---|---|
| US-01 Cohort reporting | Must | Agreed grain, snapshot, stage definitions | Medium | Implemented in analysis/workspace |
| US-02 Response exception review | Must | US-01; agreed response interpretation | Medium | Historical workspace implemented |
| US-03 Inquiry intake and duplicate review | Must | Discovery D1/D2/D8 | Medium | Proposed operational feature |
| US-04 Ownership and reassignment history | Must | US-03; D3 | Medium | Proposed operational feature |
| US-05 Due follow-up and reminders | Should | US-04; D4/D8 | Medium | Proposed operational feature |
| US-06 Quote acceptance and booking lineage | Must | US-03; D5/D6 | Medium | Source validation implemented; operational workflow proposed |
| US-07 Outcome and non-booking reasons | Should | US-03; D6/D7 | Small–Medium | Proposed; no invented reason data |
| US-08 Pilot evaluation and rollout | Must before wider adoption | Validated process; US-03/04; D9 | Medium | Proposed evaluation |

## US-01 — Cohort reporting
As an owner, I want a consistent inquiry-to-booking funnel so I can evaluate progression using the same originating leads.

- Given a lead with several contact activities, when reporting refreshes, then the lead and its first booking count once.
- Given an event exactly 30 days after creation, it is included; one second later is excluded.
- Given a lead exactly 30 days old at snapshot, it is eligible; one second younger is excluded and visible in the exclusion count.
- Filtered exports must include filter context and use the same cohort definition as the displayed measures.

Evidence: `sql/funnel.sql`, `tests/test_analysis.py`, Overview view. Trace: R1/R2/R5.

## US-02 — Response exception review
As an analyst, I want to separate unanswered and late inquiries so I can inspect the underlying records without treating missing responses as zero-hour responses.

- Unanswered records have a blank duration and enter the unanswered category.
- A recorded response strictly above a valid selected threshold enters the late category; changing the target does not change conversion.
- Search and pagination must make all matching records reachable. CSV export includes all matches, not only the current page.
- Selecting a lead opens its first recorded stage timestamps and identifies missing stages explicitly.

Evidence: Response Review view; analytical threshold/missing-response tests and documented manual UI checks. Trace: R3/R5/R6. Does not send messages or change assignments.

## US-03 — Inquiry intake and duplicate review
As an inquiry handler, I want consistent intake records so I can distinguish a new opportunity from a repeated contact.

- Proposed required fields are agreed during discovery; an incomplete required field blocks record creation with a clear message.
- A possible duplicate prompts a review and does not silently merge or delete records.
- The handling decision and link to an existing lead, if applicable, are recorded.
- Collect only approved data and contact preferences. No personal details are required in this demonstration.

Status: not implemented. Trace: D1/D2/D8, A1.

## US-04 — Ownership and reassignment history
As a team coordinator, I want one accountable owner with history so inquiries remain traceable through handoffs.

- An inquiry has one active accountable owner or an explicit unassigned status.
- Reassignment records previous owner, new owner, timestamp, actor, and reason.
- A coordinator can review unassigned records and assignment history.
- Production access roles and reassignment authority must be agreed before implementation.

Status: not implemented. Trace: R7, D3.

## US-05 — Due follow-up and reminders
As an inquiry handler, I want an agreed next-action queue so I can plan follow-up within staffed hours and contact preferences.

- A next action has an owner, due time, and status.
- Due-time calculation uses an approved staffing calendar if business-hours commitments apply.
- Completed or superseded actions do not continue appearing as overdue.
- Internal reminders do not automatically contact customers; outbound behavior needs separately agreed requirements.

Status: not implemented. Trace: R8, D4/D8, A4.

## US-06 — Quote acceptance and booking lineage
As a coordinator, I want bookings linked to the accepted quote so their origin and sequence can be checked.

- A booking cannot reference a missing quote or a quote belonging to another lead.
- A booking timestamp cannot precede its quote timestamp.
- Revise the data model before accepting quote revisions or repeat bookings, which the current unique-key contract excludes.
- A confirmed booking is reported separately from completed service and collected revenue.

Evidence: key/sequence validation and invalid-link tests. Creating or editing operational quotes/bookings is not implemented. Trace: R4, D5/D6, A2.

## US-07 — Outcome and non-booking reasons
As an owner, I want validated outcome reasons so I can distinguish avoidable process issues from customer decisions or open inquiries.

- Agree a small reason taxonomy with the business; include unknown/open rather than forcing a fabricated reason.
- A reason's author and time are traceable; later changes retain history.
- Reporting distinguishes the measured 30-day window from eventual outcomes.

Status: not implemented; no reason fields have been added to simulated records. Trace: D6/D7.

## US-08 — Pilot evaluation and rollout
As a sponsor, I want an agreed evaluation so I can decide whether a wider rollout is justified.

- Before launch, document eligibility, baseline, comparison method where feasible, duration, success measures, and stop criteria.
- Evaluate mature cohorts and monitor workload, duplicate handling, and completed-service quality alongside conversion.
- Reconcile pilot data, record actual UAT feedback, and resolve release-blocking defects before expanding.
- Report measured outcomes with limitations; do not translate simulated stage gaps into promised uplift or revenue.

Status: not implemented. Trace: D9, executive measurement plan.
