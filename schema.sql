-- =============================================================================
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
