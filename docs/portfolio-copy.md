# Portfolio and interview copy — draft

## Project title
Lead-to-Booking Improvement | Business Process and Data Analysis

## Website case study
**Problem:** A fictional cleaning business needs a consistent inquiry-to-booking process and reliable conversion reporting.

**Approach:** Designed a four-table simulated operational dataset; validated event sequence and keys; aggregated contact activities before joins; measured conversion using mature originating-lead cohorts; documented current/proposed processes, requirements, and UAT scenarios.

**Sample-data findings:** Of 360 generated leads, 323 received a response, 241 received a quote, and 132 booked within 30 days. The simulation's lead-to-booking conversion is 36.7%. Those figures describe the generated records and are not actual client outcomes.

**Recommendation:** Validate inquiry ownership, staffing calendars, and follow-up needs with a real business; pilot a shared queue before selecting a CRM. Agree an evaluation method and guardrails before testing reminders.

**Deliverables:** Interactive funnel dashboard; SQL analysis; reproducible synthetic data; data-quality checks; process maps; prioritized requirements; acceptance scenarios; executive brief; eleven automated analytical tests.

**Tools:** Python standard library, SQLite, HTML, CSS, JavaScript, Mermaid process notation.

**Status:** Independent demonstration. Proposed CRM functionality is documented, not implemented. Source: https://github.com/Himu1221/lead-to-booking-analysis. Dashboard: https://himu1221.github.io/projects/booking-desk/dashboard.html.

## LinkedIn draft
I built an independent lead-to-booking analysis case study for a fictional cleaning business.

The technical challenge was keeping inquiry counts reliable when each lead can have several contact activities. I rolled up the event tables before joining and used a consistent 30-day window for conversion.

The project combines SQL and Python analysis with an interactive dashboard, current and proposed process maps, prioritized requirements, and acceptance scenarios. Eleven automated tests cover duplicate counting, missing responses, cohort maturity, response thresholds, and booking cutoffs.

All data is simulated. The analysis is a demonstration of method, not a claim of real client results or improved conversion.

GitHub: https://github.com/Himu1221/lead-to-booking-analysis

Dashboard: https://himu1221.github.io/projects/booking-desk/dashboard.html

LinkedIn draft remains unpublished.

## Interview walkthrough
1. Explain the assumed business need and what real discovery would validate.
2. Draw the four-table model and show why a direct many-side join can inflate counts.
3. Explain cohort maturity and why a June inquiry booked in July still belongs to the June cohort.
4. Demonstrate missing-response handling and the proposed threshold; explain why it does not estimate uplift.
5. Walk through one requirement, its acceptance criterion, and its implemented or proposed status.
6. Explain how you would move from a simulated brief to a real, permissioned client engagement.
