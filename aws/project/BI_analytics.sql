-- Top 5 states by new cases on a given date

SELECT s.state_name, f.new_cases
FROM covid_gold.fact_cases_state_daily f
JOIN covid_gold.dim_state s ON s.state_code = f.state_code
WHERE f.date_id = 20200515
ORDER BY f.new_cases DESC
LIMIT 5;


-- Compute daily positivity; if you want a 7-day average, wrap with a window or pre-aggregate
SELECT d.full_date,
       (t.tests_pos_cum::double precision / NULLIF(t.tests_total_cum, 0)) AS positivity_rate
FROM covid_gold.fact_testing_state_daily t
JOIN covid_gold.dim_date d   ON d.date_id = t.date_id
WHERE t.state_code = 'NY'
ORDER BY d.full_date;


-- Daily cases vs tests for a state
SELECT d.full_date,
       c.new_cases,
       t.new_tests,
       (t.tests_pos_cum::double precision / NULLIF(t.tests_total_cum, 0)) AS positivity_rate
FROM covid_gold.fact_cases_state_daily   c
JOIN covid_gold.fact_testing_state_daily t
  ON t.date_id = c.date_id AND t.state_code = c.state_code
JOIN covid_gold.dim_date d ON d.date_id = c.date_id
WHERE c.state_code = 'CA'
ORDER BY d.full_date;
