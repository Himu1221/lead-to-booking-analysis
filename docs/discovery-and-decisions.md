# Discovery, assumptions, and decision log

## Evidence status
This is an independent case study. No stakeholder interviews, observation sessions, client approvals, or production UAT have occurred. Dataset facts come from the included simulation; operating assumptions below remain unvalidated. Proposed roles are responsibilities to discuss, not people who have committed to work.

## Discovery plan
Proposed first session: a 45-minute conversation with the owner and inquiry handler, followed by a permissioned review of a few representative real inquiries. Validate the current process before selecting software. Record actual answers and evidence only after the session takes place.

| ID | Question to ask | Evidence to request, with permission | How the answer changes the design | Status |
|---|---|---|---|---|
| D1 | What constitutes a new lead rather than a duplicate inquiry or repeat customer? | Examples of repeat contacts and existing identifiers | Determines deduplication and conversion denominator; may require a customer entity | Pending interview |
| D2 | Which channels receive inquiries, and where are they recorded? | Anonymized examples from each source | Determines intake integration and required fields | Pending interview |
| D3 | Who owns a lead during absence, shift changes, or reassignment? | Current handoff procedure | Determines assignment rules, escalation, and ownership history | Pending interview |
| D4 | What are staffed hours, holidays, and actual response commitments? | Staffing calendar and existing promises | Replaces elapsed-hour thresholds with an approved calendar-aware rule | Pending interview |
| D5 | What makes a quote valid, and can it be revised? | Quote lifecycle and acceptance evidence | May replace the one-quote-per-lead assumption with versioned quotes | Pending interview |
| D6 | What counts as a confirmed booking, cancellation, or completion? | Existing status definitions | Determines terminal states, booking lineage, and downstream measures | Pending interview |
| D7 | Why do inquiries or quotes not progress, and how is this recorded? | Existing reason codes or anonymized notes | Determines a validated outcome taxonomy; prevents calling all gaps losses | Pending interview |
| D8 | What contact preferences and retention rules apply? | Existing policies and approved contact channels | Constrains reminders, record retention, and what data the pilot should collect | Pending interview |
| D9 | Which outcome would justify a change, and at what operating cost? | Owner's decision criteria and budget constraints | Determines pilot measures, guardrails, and tool-selection criteria | Pending interview |

## Assumption register
| ID | Current assumption | Risk if wrong | Proposed validation | Current treatment |
|---|---|---|---|---|
| A1 | One record is one originating inquiry | Duplicate contacts inflate lead counts | D1 plus sample record review | Explicitly documented; no deduplication claim |
| A2 | One quote and one first booking per lead | Revisions or repeat bookings are rejected or misrepresented | D5/D6 | Enforced source contract; model change required for production |
| A3 | Thirty days is a useful evaluation horizon | Longer sales cycles appear to have poor conversion | D6/D9 plus historical cycle analysis | Demonstration window only; immature cohorts excluded |
| A4 | Four elapsed hours is a useful review threshold | Unstaffed periods are unfairly labeled late | D4 | Proposed setting; not an agreed SLA |
| A5 | A shared queue is a suitable low-effort pilot | Existing tools may already solve the problem | D2/D3 and tool inventory | Recommendation subject to discovery |
| A6 | First-response activities mean outbound response | Acknowledgments may be mistaken for meaningful engagement | D2 and activity examples | Uses explicit simulated activity type |

## Decision log
These are case-study design decisions made during development. They are not client approvals.

| ID | Decision | Rationale and evidence | Alternative considered | Revisit when |
|---|---|---|---|---|
| DEC-01 | Use a fictional dataset with a reproducible seed | No permissioned client data is available | Presenting invented records as client evidence is inappropriate | A real organization provides authorized data |
| DEC-02 | Aggregate activities before joining | A lead can have multiple activities; raw joins can multiply counts | Direct joins followed by unqualified COUNT | Model grain or downstream measures change |
| DEC-03 | Use originating cohorts and a fixed 30-day window | Keeps conversion numerators and denominators aligned | Comparing inquiry counts and booking counts from unrelated calendar months | Sales-cycle evidence supports another window |
| DEC-04 | Report missing responses separately | Missing timestamps are not zero elapsed hours | Excluding nonresponders without disclosure | The business distinguishes more contact outcomes |
| DEC-05 | Offer a historical response-review workspace | Enables record inspection without pretending to operate a CRM | Editable assignments or automatic outreach | A separate implementation is scoped and approved |
| DEC-06 | Recommend discovery and a shared-queue pilot before vendor selection | Process and cost constraints are not validated | Selecting a CRM based only on simulated conversion | Discovery supplies decision criteria |

## Proposed feedback capture
For each real session, record date, participant role, permission/consent context, question ID, anonymized answer, evidence reference, affected assumption/requirement, decision owner, and unresolved follow-up. Do not populate this with fictional interview answers. Mark requirements approved only after the actual reviewer approves them.
