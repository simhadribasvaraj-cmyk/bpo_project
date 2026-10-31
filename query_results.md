# DA-06 VoiceServe SQL Analysis Results

**Author:** DataVerse Squad (Codegnan) | **Database:** PostgreSQL / MySQL Compatible

## Query 1: Segment Attrition by Centre, Process & Shift

```sql
SELECT 
    centre,
    process,
    shift,
    COUNT(employee_id) AS total_headcount,
    SUM(attrition_flag) AS total_exits,
    ROUND(SUM(attrition_flag) * 100.0 / NULLIF(COUNT(employee_id), 0), 2) AS attrition_rate_pct
FROM employees_cleaned
GROUP BY centre, process, shift
ORDER BY attrition_rate_pct DESC;
```

**Query Output:**

| centre | process | shift | total_headcount | total_exits | attrition_rate_pct |
| --- | --- | --- | --- | --- | --- |
| Hyderabad (Gachibowli) | Outbound Sales | Night | 65 | 54 | 83.08 |
| Visakhapatnam (Rushikonda) | Chat & Email Support | Night | 32 | 26 | 81.25 |
| Hyderabad (Hitec City) | Chat & Email Support | Night | 45 | 30 | 66.67 |
| Visakhapatnam (Rushikonda) | Outbound Sales | Night | 45 | 30 | 66.67 |
| Hyderabad (Gachibowli) | Outbound Sales | Rotational | 42 | 27 | 64.29 |
| Visakhapatnam (Rushikonda) | Inbound Customer Service | Night | 84 | 54 | 64.29 |
| Hyderabad (Hitec City) | Outbound Sales | Rotational | 49 | 31 | 63.27 |
| Visakhapatnam (Rushikonda) | Outbound Sales | Rotational | 37 | 23 | 62.16 |
| Hyderabad (Hitec City) | Outbound Sales | Night | 86 | 50 | 58.14 |
| Visakhapatnam (Rushikonda) | Technical Support | Night | 31 | 18 | 58.06 |
| Hyderabad (Gachibowli) | Inbound Customer Service | Night | 87 | 49 | 56.32 |
| Visakhapatnam (Rushikonda) | Claims & Back Office | Night | 37 | 20 | 54.05 |
| Hyderabad (Gachibowli) | Inbound Customer Service | Day | 102 | 54 | 52.94 |
| Hyderabad (Gachibowli) | Chat & Email Support | Night | 40 | 21 | 52.5 |
| Visakhapatnam (Rushikonda) | Chat & Email Support | Day | 42 | 22 | 52.38 |
| Hyderabad (Hitec City) | Inbound Customer Service | Rotational | 62 | 32 | 51.61 |
| Hyderabad (Gachibowli) | Chat & Email Support | Day | 59 | 30 | 50.85 |
| Hyderabad (Hitec City) | Chat & Email Support | Rotational | 32 | 16 | 50.0 |
| Visakhapatnam (Rushikonda) | Claims & Back Office | Rotational | 16 | 8 | 50.0 |
| Hyderabad (Hitec City) | Inbound Customer Service | Night | 107 | 52 | 48.6 |
| Hyderabad (Gachibowli) | Technical Support | Day | 50 | 24 | 48.0 |
| Hyderabad (Hitec City) | Technical Support | Night | 69 | 33 | 47.83 |
| Hyderabad (Gachibowli) | Claims & Back Office | Night | 42 | 20 | 47.62 |
| Hyderabad (Gachibowli) | Outbound Sales | Day | 55 | 26 | 47.27 |
| Hyderabad (Gachibowli) | Chat & Email Support | Rotational | 26 | 12 | 46.15 |
| Hyderabad (Hitec City) | Technical Support | Rotational | 24 | 11 | 45.83 |
| Hyderabad (Hitec City) | Claims & Back Office | Night | 60 | 27 | 45.0 |
| Visakhapatnam (Rushikonda) | Inbound Customer Service | Day | 105 | 46 | 43.81 |
| Visakhapatnam (Rushikonda) | Inbound Customer Service | Rotational | 46 | 20 | 43.48 |
| Hyderabad (Hitec City) | Technical Support | Day | 83 | 35 | 42.17 |
| Hyderabad (Gachibowli) | Technical Support | Rotational | 24 | 10 | 41.67 |
| Visakhapatnam (Rushikonda) | Technical Support | Rotational | 17 | 7 | 41.18 |
| Visakhapatnam (Rushikonda) | Technical Support | Day | 39 | 16 | 41.03 |
| Hyderabad (Gachibowli) | Technical Support | Night | 47 | 19 | 40.43 |
| Hyderabad (Hitec City) | Inbound Customer Service | Day | 169 | 68 | 40.24 |
| Hyderabad (Hitec City) | Outbound Sales | Day | 94 | 37 | 39.36 |
| Visakhapatnam (Rushikonda) | Outbound Sales | Day | 61 | 23 | 37.7 |
| Hyderabad (Gachibowli) | Claims & Back Office | Rotational | 24 | 9 | 37.5 |
| Hyderabad (Hitec City) | Chat & Email Support | Day | 80 | 30 | 37.5 |
| Visakhapatnam (Rushikonda) | Claims & Back Office | Day | 49 | 18 | 36.73 |
| Hyderabad (Gachibowli) | Inbound Customer Service | Rotational | 53 | 19 | 35.85 |
| Visakhapatnam (Rushikonda) | Chat & Email Support | Rotational | 17 | 6 | 35.29 |
| Hyderabad (Hitec City) | Claims & Back Office | Rotational | 35 | 12 | 34.29 |
| Hyderabad (Gachibowli) | Claims & Back Office | Day | 61 | 18 | 29.51 |
| Hyderabad (Hitec City) | Claims & Back Office | Day | 70 | 20 | 28.57 |

---

## Query 1B: Monthly Exit Trend by Centre & Shift

```sql
SELECT 
    SUBSTR(exit_date, 1, 7) AS exit_month,
    centre,
    shift,
    COUNT(employee_id) AS monthly_exits,
    ROUND(COUNT(employee_id) * 100.0 / NULLIF(SUM(COUNT(employee_id)) OVER(PARTITION BY centre, shift), 0), 2) AS pct_of_segment_exits
FROM employees_cleaned
WHERE exit_date IS NOT NULL
GROUP BY exit_month, centre, shift
ORDER BY exit_month DESC, monthly_exits DESC
LIMIT 15;
```

**Query Output:**

| exit_month | centre | shift | monthly_exits | pct_of_segment_exits |
| --- | --- | --- | --- | --- |
| 2026-10 | Hyderabad (Hitec City) | Day | 17 | 8.95 |
| 2026-10 | Visakhapatnam (Rushikonda) | Night | 17 | 11.49 |
| 2026-10 | Hyderabad (Gachibowli) | Night | 15 | 9.2 |
| 2026-10 | Hyderabad (Hitec City) | Night | 13 | 6.77 |
| 2026-10 | Hyderabad (Gachibowli) | Day | 12 | 7.89 |
| 2026-10 | Visakhapatnam (Rushikonda) | Day | 12 | 9.6 |
| 2026-10 | Hyderabad (Hitec City) | Rotational | 8 | 7.84 |
| 2026-10 | Visakhapatnam (Rushikonda) | Rotational | 4 | 6.25 |
| 2026-10 | Hyderabad (Gachibowli) | Rotational | 1 | 1.3 |
| 2026-09 | Hyderabad (Gachibowli) | Night | 14 | 8.59 |
| 2026-09 | Hyderabad (Hitec City) | Day | 14 | 7.37 |
| 2026-09 | Visakhapatnam (Rushikonda) | Night | 14 | 9.46 |
| 2026-09 | Hyderabad (Hitec City) | Night | 13 | 6.77 |
| 2026-09 | Hyderabad (Gachibowli) | Day | 10 | 6.58 |
| 2026-09 | Hyderabad (Hitec City) | Rotational | 9 | 8.82 |

---

## Query 2: Early Leavers (<= 90 Days) Common Traits

```sql
SELECT 
    centre,
    process,
    shift,
    role,
    COUNT(employee_id) AS early_leavers_count,
    ROUND(COUNT(employee_id) * 100.0 / NULLIF((SELECT COUNT(*) FROM employees_cleaned WHERE left_within_90_days = 1), 0), 2) AS pct_of_early_leavers,
    ROUND(AVG(monthly_salary), 2) AS avg_salary,
    ROUND(AVG(avg_attendance_percent), 2) AS avg_attendance,
    ROUND(AVG(avg_quality_score), 2) AS avg_qa_score,
    ROUND(SUM(CASE WHEN notice_served = 'No' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(employee_id), 0), 2) AS unserved_notice_pct
FROM employees_cleaned
WHERE left_within_90_days = 1
GROUP BY centre, process, shift, role
ORDER BY early_leavers_count DESC
LIMIT 10;
```

**Query Output:**

| centre | process | shift | role | early_leavers_count | pct_of_early_leavers | avg_salary | avg_attendance | avg_qa_score | unserved_notice_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hyderabad (Gachibowli) | Inbound Customer Service | Day | Customer Support Executive | 16 | 3.96 | 24718.75 | 82.73 | 90.14 | 87.5 |
| Hyderabad (Hitec City) | Inbound Customer Service | Day | Customer Support Executive | 15 | 3.71 | 23833.33 | 83.87 | 89.72 | 80.0 |
| Visakhapatnam (Rushikonda) | Inbound Customer Service | Night | Customer Support Executive | 15 | 3.71 | 22733.33 | 82.83 | 90.07 | 86.67 |
| Visakhapatnam (Rushikonda) | Inbound Customer Service | Day | Customer Support Executive | 12 | 2.97 | 23333.33 | 83.4 | 88.34 | 66.67 |
| Hyderabad (Gachibowli) | Outbound Sales | Night | Customer Support Executive | 10 | 2.48 | 23450.0 | 83.82 | 88.43 | 80.0 |
| Hyderabad (Hitec City) | Technical Support | Day | Customer Support Executive | 10 | 2.48 | 24800.0 | 83.45 | 87.28 | 60.0 |
| Hyderabad (Hitec City) | Chat & Email Support | Day | Customer Support Executive | 8 | 1.98 | 23437.5 | 84.24 | 90.32 | 62.5 |
| Hyderabad (Hitec City) | Outbound Sales | Night | Customer Support Executive | 8 | 1.98 | 23937.5 | 83.59 | 88.14 | 37.5 |
| Hyderabad (Hitec City) | Technical Support | Night | Customer Support Executive | 8 | 1.98 | 24062.5 | 82.45 | 90.28 | 75.0 |
| Hyderabad (Gachibowli) | Inbound Customer Service | Night | Customer Support Executive | 7 | 1.73 | 21928.57 | 80.05 | 89.75 | 57.14 |

---

## Query 3: Pay & Incentives of High vs Low Performers

```sql
-- Performance Thresholds:
-- High Performer: avg_quality_score >= 88.0 AND avg_customer_rating >= 4.20
-- Low Performer: avg_quality_score < 75.0 OR avg_customer_rating < 3.20
-- Medium Performer: All remaining employees
SELECT 
    performer_category,
    COUNT(employee_id) AS employee_count,
    ROUND(AVG(monthly_salary), 2) AS avg_base_salary,
    ROUND(AVG(incentive_amount), 2) AS avg_incentive,
    ROUND(AVG(total_pay), 2) AS avg_total_monthly_pay,
    ROUND(AVG(last_hike_percent), 2) AS avg_last_hike_pct,
    ROUND(AVG(avg_quality_score), 2) AS avg_qa_score,
    ROUND(AVG(avg_customer_rating), 2) AS avg_csat_rating,
    ROUND(SUM(attrition_flag) * 100.0 / NULLIF(COUNT(employee_id), 0), 2) AS attrition_rate_pct
FROM employees_cleaned
GROUP BY performer_category
ORDER BY avg_total_monthly_pay DESC;
```

**Query Output:**

| performer_category | employee_count | avg_base_salary | avg_incentive | avg_total_monthly_pay | avg_last_hike_pct | avg_qa_score | avg_csat_rating | attrition_rate_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High Performer | 1270 | 28082.28 | 5931.26 | 34013.54 | 6.56 | 91.44 | 4.44 | 42.99 |
| Medium Performer | 1228 | 28492.26 | 2933.79 | 31426.06 | 6.45 | 86.21 | 4.05 | 54.32 |
| Low Performer | 2 | 24500.0 | 650.0 | 25150.0 | 7.9 | 74.2 | 3.42 | 0.0 |

---

## Query 4: Average Tenure by Role and Process

```sql
SELECT 
    process,
    role,
    COUNT(employee_id) AS total_employees,
    ROUND(AVG(tenure_months), 2) AS avg_tenure_months,
    ROUND(AVG(CASE WHEN attrition_flag = 1 THEN tenure_months ELSE NULL END), 2) AS avg_tenure_leavers,
    ROUND(AVG(CASE WHEN attrition_flag = 0 THEN tenure_months ELSE NULL END), 2) AS avg_tenure_stayers,
    ROUND(SUM(attrition_flag) * 100.0 / NULLIF(COUNT(employee_id), 0), 2) AS attrition_rate_pct
FROM employees_cleaned
GROUP BY process, role
ORDER BY process, avg_tenure_months ASC;
```

**Query Output:**

| process | role | total_employees | avg_tenure_months | avg_tenure_leavers | avg_tenure_stayers | attrition_rate_pct |
| --- | --- | --- | --- | --- | --- | --- |
| Chat & Email Support | Senior Customer Support Executive | 54 | 11.68 | 7.82 | 17.74 | 61.11 |
| Chat & Email Support | Team Leader | 11 | 11.83 | 7.33 | 17.22 | 54.55 |
| Chat & Email Support | Quality Analyst | 14 | 11.92 | 7.92 | 19.12 | 64.29 |
| Chat & Email Support | Customer Support Executive | 261 | 13.94 | 8.76 | 19.17 | 50.19 |
| Chat & Email Support | Technical Support Specialist | 33 | 14.36 | 9.42 | 18.0 | 42.42 |
| Claims & Back Office | Team Leader | 23 | 11.57 | 6.2 | 18.55 | 56.52 |
| Claims & Back Office | Quality Analyst | 18 | 13.33 | 5.33 | 19.74 | 44.44 |
| Claims & Back Office | Technical Support Specialist | 38 | 14.03 | 8.59 | 18.93 | 47.37 |
| Claims & Back Office | Senior Customer Support Executive | 60 | 15.0 | 7.38 | 17.78 | 26.67 |
| Claims & Back Office | Customer Support Executive | 255 | 15.18 | 7.54 | 19.87 | 38.04 |
| Inbound Customer Service | Technical Support Specialist | 100 | 11.88 | 6.22 | 16.91 | 47.0 |
| Inbound Customer Service | Quality Analyst | 40 | 12.18 | 7.99 | 14.69 | 37.5 |
| Inbound Customer Service | Team Leader | 41 | 12.68 | 8.62 | 17.37 | 53.66 |
| Inbound Customer Service | Customer Support Executive | 510 | 13.38 | 8.29 | 18.56 | 50.39 |
| Inbound Customer Service | Senior Customer Support Executive | 124 | 13.55 | 7.97 | 17.72 | 42.74 |
| Outbound Sales | Technical Support Specialist | 49 | 10.37 | 5.69 | 20.02 | 67.35 |
| Outbound Sales | Quality Analyst | 33 | 11.12 | 8.12 | 15.2 | 57.58 |
| Outbound Sales | Team Leader | 24 | 11.4 | 7.23 | 19.75 | 66.67 |
| Outbound Sales | Senior Customer Support Executive | 79 | 12.64 | 7.12 | 18.9 | 53.16 |
| Outbound Sales | Customer Support Executive | 349 | 13.56 | 9.88 | 18.01 | 54.73 |
| Technical Support | Team Leader | 15 | 11.91 | 5.13 | 16.42 | 40.0 |
| Technical Support | Quality Analyst | 16 | 13.01 | 7.33 | 16.41 | 37.5 |
| Technical Support | Technical Support Specialist | 43 | 13.01 | 7.85 | 18.42 | 51.16 |
| Technical Support | Senior Customer Support Executive | 60 | 13.87 | 8.35 | 17.55 | 40.0 |
| Technical Support | Customer Support Executive | 250 | 14.25 | 8.18 | 19.42 | 46.0 |

---

## Query 5: Leavers vs Stayers on Pay, Shift & Engagement

```sql
SELECT 
    CASE WHEN attrition_flag = 1 THEN 'Leaver' ELSE 'Stayer' END AS employee_status,
    shift,
    COUNT(employee_id) AS headcount,
    ROUND(AVG(monthly_salary), 2) AS avg_monthly_salary,
    ROUND(AVG(incentive_amount), 2) AS avg_incentive_amount,
    ROUND(AVG(total_pay), 2) AS avg_total_monthly_pay,
    ROUND(AVG(last_hike_percent), 2) AS avg_hike_pct,
    ROUND(AVG(survey_score), 2) AS avg_survey_score,
    ROUND(AVG(training_hours), 2) AS avg_training_hours,
    ROUND(AVG(avg_attendance_percent), 2) AS avg_attendance_pct
FROM employees_cleaned
GROUP BY attrition_flag, shift
ORDER BY shift, employee_status DESC;
```

**Query Output:**

| employee_status | shift | headcount | avg_monthly_salary | avg_incentive_amount | avg_total_monthly_pay | avg_hike_pct | avg_survey_score | avg_training_hours | avg_attendance_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stayer | Day | 652 | 27633.44 | 4501.38 | 32134.82 | 7.01 | 3.53 | 24.41 | 93.91 |
| Leaver | Day | 467 | 28474.3 | 4252.68 | 32726.98 | 5.79 | 3.22 | 24.62 | 85.61 |
| Stayer | Night | 374 | 28189.84 | 4491.98 | 32681.82 | 7.15 | 3.54 | 24.63 | 93.81 |
| Leaver | Night | 503 | 28379.72 | 4449.11 | 32828.83 | 5.87 | 3.31 | 24.03 | 85.83 |
| Stayer | Rotational | 261 | 29157.09 | 4477.78 | 33634.87 | 7.57 | 3.44 | 25.27 | 93.85 |
| Leaver | Rotational | 243 | 28639.92 | 4646.91 | 33286.83 | 5.71 | 3.23 | 24.79 | 85.78 |

---

## Query 6: Night Shift and Low-Hike (<6%) vs Attrition

```sql
-- Definition of Low Hike: last_hike_percent < 6.0% for employees with tenure >= 6 months
SELECT 
    shift,
    CASE 
        WHEN tenure_months < 6 THEN 'Not Eligible (<6 Mon)'
        WHEN last_hike_percent IS NOT NULL AND last_hike_percent < 6.0 THEN 'Low Hike (<6%)'
        WHEN last_hike_percent BETWEEN 6.0 AND 10.0 THEN 'Moderate Hike (6-10%)'
        WHEN last_hike_percent > 10.0 THEN 'Competitive Hike (>10%)'
        ELSE 'Unknown'
    END AS hike_tier,
    COUNT(employee_id) AS total_employees,
    SUM(attrition_flag) AS leavers_count,
    ROUND(SUM(attrition_flag) * 100.0 / NULLIF(COUNT(employee_id), 0), 2) AS attrition_rate_pct,
    ROUND(AVG(total_pay), 2) AS avg_total_pay,
    ROUND(AVG(survey_score), 2) AS avg_engagement_score
FROM employees_cleaned
GROUP BY shift, hike_tier
ORDER BY shift, attrition_rate_pct DESC;
```

**Query Output:**

| shift | hike_tier | total_employees | leavers_count | attrition_rate_pct | avg_total_pay | avg_engagement_score |
| --- | --- | --- | --- | --- | --- | --- |
| Day | Not Eligible (<6 Mon) | 290 | 241 | 83.1 | 33251.38 | 3.33 |
| Day | Low Hike (<6%) | 315 | 112 | 35.56 | 32604.44 | 3.48 |
| Day | Moderate Hike (6-10%) | 374 | 97 | 25.94 | 31805.35 | 3.36 |
| Day | Competitive Hike (>10%) | 140 | 17 | 12.14 | 31620.71 | 3.48 |
| Night | Not Eligible (<6 Mon) | 272 | 246 | 90.44 | 33571.69 | 3.35 |
| Night | Low Hike (<6%) | 216 | 118 | 54.63 | 32022.69 | 3.49 |
| Night | Moderate Hike (6-10%) | 303 | 118 | 38.94 | 32903.63 | 3.37 |
| Night | Competitive Hike (>10%) | 86 | 21 | 24.42 | 31601.16 | 3.49 |
| Rotational | Not Eligible (<6 Mon) | 134 | 123 | 91.79 | 33878.36 | 3.21 |
| Rotational | Low Hike (<6%) | 132 | 60 | 45.45 | 33198.48 | 3.37 |
| Rotational | Moderate Hike (6-10%) | 175 | 53 | 30.29 | 33293.14 | 3.38 |
| Rotational | Competitive Hike (>10%) | 63 | 7 | 11.11 | 33638.1 | 3.47 |

---

