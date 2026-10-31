"""
Execute SQL Analysis and generate judge-ready SQL scripts and results.
DA-06: Employee Performance, Compensation & Attrition Trend Analysis
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_employee_data.csv")
SQL_DIR = os.path.join(BASE_DIR, "sql")
os.makedirs(SQL_DIR, exist_ok=True)

df_clean = pd.read_csv(DATA_PATH)

# Create in-memory SQLite database
conn = sqlite3.connect(":memory:")
df_clean.to_sql("employees_cleaned", conn, index=False, if_exists="replace")

print(f"Loaded {len(df_clean)} records into SQL engine.")

queries = {}

# Query 1A: Monthly Attrition Rate by Centre, Process, and Shift (Aggregated Segment View)
queries["Query 1: Segment Attrition by Centre, Process & Shift"] = """
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
"""

# Query 1B: Monthly Exit Trend
queries["Query 1B: Monthly Exit Trend by Centre & Shift"] = """
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
"""

# Query 2: Employees who left within 90 days of joining and their common traits
queries["Query 2: Early Leavers (<= 90 Days) Common Traits"] = """
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
"""

# Query 3: Average pay and incentives of high vs low performers
queries["Query 3: Pay & Incentives of High vs Low Performers"] = """
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
"""

# Query 4: Average tenure by role and process
queries["Query 4: Average Tenure by Role and Process"] = """
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
"""

# Query 5: Leavers vs stayers on pay, shift and engagement
queries["Query 5: Leavers vs Stayers on Pay, Shift & Engagement"] = """
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
"""

# Query 6: Night shift and low-hike vs attrition
queries["Query 6: Night Shift and Low-Hike (<6%) vs Attrition"] = """
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
"""

# Execute and store results
results_md = "# DA-06 VoiceServe SQL Analysis Results\n\n"
results_md += "**Author:** DataVerse Squad (Codegnan) | **Database:** PostgreSQL / MySQL Compatible\n\n"

sql_queries_file_content = """/*
================================================================================
VOICESERVE BPO - JUDGE-READY SQL ANALYSIS SCRIPT
DA-06: Employee Performance, Compensation and Attrition Trend Analysis
Team: DataVerse Squad, Codegnan
Compatible with: PostgreSQL 12+, MySQL 8.0+, SQLite 3.30+
================================================================================
*/

"""

def df_to_markdown(df):
    headers = list(df.columns)
    lines = ["| " + " | ".join(str(h) for h in headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(val) for val in row) + " |")
    return "\n".join(lines)

for q_name, q_sql in queries.items():
    print(f"Executing {q_name}...")
    res_df = pd.read_sql_query(q_sql, conn)
    
    # Text table format for SQL comments
    tab_text = res_df.to_string(index=False)
    commented_tab = "\n".join([f"    -- {line}" for line in tab_text.split("\n")])
    
    sql_queries_file_content += f"""
-- =============================================================================
-- {q_name}
-- =============================================================================
{q_sql.strip()}

/*
OUTPUT RESULTS:
{commented_tab}
*/

"""

    # Markdown format
    results_md += f"## {q_name}\n\n```sql\n{q_sql.strip()}\n```\n\n"
    results_md += "**Query Output:**\n\n"
    results_md += df_to_markdown(res_df) + "\n\n---\n\n"

# Write sql/queries.sql
with open(os.path.join(SQL_DIR, "queries.sql"), "w", encoding="utf-8") as f:
    f.write(sql_queries_file_content)

# Write sql/query_results.md
with open(os.path.join(SQL_DIR, "query_results.md"), "w", encoding="utf-8") as f:
    f.write(results_md)

# Write sql/schema.sql
schema_sql = """-- =============================================================================
-- VOICESERVE BPO - DATABASE SCHEMA (PostgreSQL / MySQL)
-- =============================================================================

DROP TABLE IF EXISTS performance_logs CASCADE;
DROP TABLE IF EXISTS exits CASCADE;
DROP TABLE IF EXISTS engagement CASCADE;
DROP TABLE IF EXISTS payroll CASCADE;
DROP TABLE IF EXISTS employees CASCADE;

CREATE TABLE employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    join_date DATE NOT NULL,
    centre VARCHAR(50) NOT NULL,
    process VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL,
    shift VARCHAR(20) NOT NULL,
    age_group VARCHAR(20) NOT NULL
);

CREATE TABLE payroll (
    employee_id VARCHAR(10) PRIMARY KEY REFERENCES employees(employee_id),
    monthly_salary NUMERIC(10, 2) NOT NULL,
    incentive_amount NUMERIC(10, 2) DEFAULT 0.0,
    last_hike_percent NUMERIC(5, 2),
    last_hike_date DATE
);

CREATE TABLE engagement (
    employee_id VARCHAR(10) PRIMARY KEY REFERENCES employees(employee_id),
    survey_score NUMERIC(3, 2),
    training_hours INT,
    promotions_count INT DEFAULT 0
);

CREATE TABLE exits (
    employee_id VARCHAR(10) PRIMARY KEY REFERENCES employees(employee_id),
    exit_date DATE,
    exit_reason TEXT,
    notice_served VARCHAR(10)
);

CREATE TABLE performance_logs (
    log_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(10) REFERENCES employees(employee_id),
    month VARCHAR(7) NOT NULL,
    calls_handled INT,
    quality_score NUMERIC(5, 2),
    customer_rating NUMERIC(3, 2),
    attendance_percent NUMERIC(5, 2),
    CONSTRAINT uq_emp_month UNIQUE(employee_id, month)
);

-- Analytical View / Master Cleaned Table DDL
CREATE TABLE employees_cleaned (
    employee_id VARCHAR(10) PRIMARY KEY,
    join_date DATE NOT NULL,
    centre VARCHAR(50) NOT NULL,
    process VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL,
    shift VARCHAR(20) NOT NULL,
    age_group VARCHAR(20) NOT NULL,
    monthly_salary NUMERIC(10, 2) NOT NULL,
    incentive_amount NUMERIC(10, 2) DEFAULT 0.0,
    last_hike_percent NUMERIC(5, 2),
    last_hike_date DATE,
    survey_score NUMERIC(3, 2),
    training_hours INT,
    promotions_count INT,
    exit_date DATE,
    exit_reason TEXT,
    notice_served VARCHAR(10),
    total_months_active INT,
    avg_calls_handled NUMERIC(8, 2),
    avg_quality_score NUMERIC(5, 2),
    avg_customer_rating NUMERIC(3, 2),
    avg_attendance_percent NUMERIC(5, 2),
    attrition_flag INT NOT NULL,
    tenure_days INT NOT NULL,
    tenure_months NUMERIC(6, 1) NOT NULL,
    left_within_90_days INT NOT NULL,
    tenure_band VARCHAR(20) NOT NULL,
    total_pay NUMERIC(10, 2) NOT NULL,
    low_hike_flag INT NOT NULL,
    performer_category VARCHAR(25) NOT NULL
);
"""

with open(os.path.join(SQL_DIR, "schema.sql"), "w", encoding="utf-8") as f:
    f.write(schema_sql)

# Write sql/load_data.sql
load_sql = r"""-- =============================================================================
-- VOICESERVE BPO - DATA LOADING SCRIPTS
-- =============================================================================

-- 1. PostgreSQL \COPY Syntax:
-- Run in psql:
/*
\COPY employees_cleaned FROM 'C:/path/to/data/cleaned_employee_data.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
*/

-- 2. MySQL LOAD DATA INFILE Syntax:
/*
LOAD DATA LOCAL INFILE 'C:/path/to/data/cleaned_employee_data.csv'
INTO TABLE employees_cleaned
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 ROWS;
*/
"""

with open(os.path.join(SQL_DIR, "load_data.sql"), "w", encoding="utf-8") as f:
    f.write(load_sql)

print("\nSUCCESS: All SQL files generated successfully in /sql/:")
print(" - sql/schema.sql")
print(" - sql/load_data.sql")
print(" - sql/queries.sql (with outputs pasted in comments)")
print(" - sql/query_results.md (with formatted markdown tables)")
