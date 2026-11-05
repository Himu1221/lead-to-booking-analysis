-- lead_funnel is materialized from funnel.sql, with one record per lead.
-- Only fully mature cohorts enter comparable conversion denominators.
WITH grouped AS (
 SELECT source,COUNT(*) AS leads,SUM(responded) AS responded,SUM(quoted) AS quoted,
 SUM(booked) AS booked,AVG(CASE WHEN responded=1 THEN response_hours END) AS mean_response_hours
 FROM lead_funnel WHERE mature=1 GROUP BY source
)
SELECT *,1.0*booked/NULLIF(leads,0) AS lead_to_booking,
 1.0*booked/NULLIF(quoted,0) AS quote_to_booking,
 DENSE_RANK() OVER(ORDER BY 1.0*booked/NULLIF(leads,0) DESC) AS conversion_rank
FROM grouped ORDER BY conversion_rank,source;
