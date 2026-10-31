-- =============================================================================
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
