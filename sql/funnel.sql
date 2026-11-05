-- SQLite dialect. Roll up many-side tables before joining to prevent fan-out.
-- Originating lead cohort; every stage is measured within 30 elapsed days.
WITH response AS (
 SELECT lead_id,MIN(occurred_at) AS first_response FROM activities
 WHERE activity_type='First response' GROUP BY lead_id
), quote AS (
 SELECT lead_id,MIN(quoted_at) AS first_quote FROM quotes GROUP BY lead_id
), booking AS (
 SELECT lead_id,MIN(booked_at) AS first_booking FROM bookings GROUP BY lead_id
), joined AS (
 SELECT l.*,r.first_response,q.first_quote,b.first_booking,
 (julianday(r.first_response)-julianday(l.created_at))*24 AS response_hours,
 julianday(:snapshot)-julianday(l.created_at)>=30 AS mature
 FROM leads l LEFT JOIN response r ON l.lead_id=r.lead_id
 LEFT JOIN quote q ON l.lead_id=q.lead_id
 LEFT JOIN booking b ON l.lead_id=b.lead_id
)
SELECT *,SUBSTR(created_at,1,7) AS cohort,
 CASE WHEN julianday(first_response)-julianday(created_at) BETWEEN 0 AND 30 THEN 1 ELSE 0 END AS responded,
 CASE WHEN julianday(first_quote)-julianday(created_at) BETWEEN 0 AND 30 THEN 1 ELSE 0 END AS quoted,
 CASE WHEN julianday(first_booking)-julianday(created_at) BETWEEN 0 AND 30 THEN 1 ELSE 0 END AS booked
FROM joined ORDER BY lead_id;
