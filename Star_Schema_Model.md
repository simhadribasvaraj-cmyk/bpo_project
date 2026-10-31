# VoiceServe BPO - Power BI Star-Schema Data Model Specification
**Problem DA-06: Employee Performance, Compensation and Attrition Trend Analysis**
**Team:** DataVerse Squad, Codegnan

---

## 1. Architectural Overview & Star-Schema Topology
The Power BI analytical model utilizes a high-performance **Star-Schema** design optimized for fast in-memory DAX tabular engine evaluation (VertiPaq). A central transactional and workforce fact table (`Fact_Workforce`) is surrounded by dedicated, normalized dimension tables.

```
       +-----------------------+
       |       Dim_Date        |
       +-----------------------+
       | Date (PK)             |
       +-----------+-----------+
                   | 1
                   |
                   | * (join_date / exit_date)
+------------------+------------------+       +-----------------------+
|            Dim_Centre               |       |       Dim_Shift       |
+-------------------------------------+       +-----------------------+
| centre_id (PK)                      |       | shift_id (PK)         |
| centre                              |       | shift                 |
| city                                |       | shift_timing          |
| tier                                |       | night_allowance_elig  |
+------------------+------------------+       +-----------+-----------+
                   | 1                                    | 1
                   |                                      |
                   | *                                    | *
         +---------+--------------------------------------+---------+
         |                      Fact_Workforce                      |
         +----------------------------------------------------------+
         | employee_id (PK)                                         |
         | join_date (FK -> Dim_Date)                               |
         | exit_date (FK -> Dim_Date)                               |
         | centre_id (FK -> Dim_Centre)                             |
         | process_id (FK -> Dim_Process)                           |
         | shift_id (FK -> Dim_Shift)                               |
         | role_id (FK -> Dim_Role)                                 |
         | monthly_salary, incentive_amount, total_pay              |
         | last_hike_percent, survey_score, training_hours          |
         | avg_calls_handled, avg_quality_score, avg_customer_rating|
         | avg_attendance_percent, attrition_flag                   |
         | tenure_months, tenure_band, left_within_90_days          |
         +---------+--------------------------------------+---------+
                   | *                                    | *
                   |                                      |
                   | 1                                    | 1
+------------------+------------------+       +-----------+-----------+
|             Dim_Role                |       |      Dim_Process      |
+-------------------------------------+       +-----------------------+
| role_id (PK)                        |       | process_id (PK)       |
| role                                |       | process               |
| role_hierarchy_level                |       | voice_flag            |
+-------------------------------------+       | target_aht_seconds    |
                                              +-----------------------+
```

---

## 2. Table Relationships & Cardinalities

| From Table (Dimension) | From Column (PK) | To Table (Fact) | To Column (FK) | Cardinality | Cross-Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dim_Centre** | `centre_id` | **Fact_Workforce** | `centre_id` | $1 : *$ (One-to-Many) | Single (Dim $ightarrow$ Fact) |
| **Dim_Process** | `process_id` | **Fact_Workforce** | `process_id` | $1 : *$ (One-to-Many) | Single (Dim $ightarrow$ Fact) |
| **Dim_Shift** | `shift_id` | **Fact_Workforce** | `shift_id` | $1 : *$ (One-to-Many) | Single (Dim $ightarrow$ Fact) |
| **Dim_Role** | `role_id` | **Fact_Workforce** | `role_id` | $1 : *$ (One-to-Many) | Single (Dim $ightarrow$ Fact) |
| **Dim_Date** | `date` | **Fact_Workforce** | `join_date` | $1 : *$ (Active) | Single (Dim $ightarrow$ Fact) |
| **Dim_Date** | `date` | **Fact_Workforce** | `exit_date` | $1 : *$ (Inactive) | Single (Dim $ightarrow$ Fact) |

*(Note: The `exit_date` relationship is kept inactive and invoked in DAX via `USERELATIONSHIP(Fact_Workforce[exit_date], Dim_Date[date])` when plotting leaver cohorts over time).*

---

## 3. Dimension & Fact Details
- **Fact_Workforce.csv**: 2,500 rows, 34 columns. Contains all employee records, transactional performance aggregates, compensation fields, and retention flags.
- **Dim_Centre.csv**: 3 centres (Hyderabad Hitec City, Hyderabad Gachibowli, Visakhapatnam Rushikonda).
- **Dim_Process.csv**: 5 operations processes (Inbound Customer Service, Outbound Sales, Technical Support, Chat & Email Support, Claims & Back Office).
- **Dim_Shift.csv**: 3 shifts (Day, Night, Rotational) with policy attributes.
- **Dim_Role.csv**: 5 operational roles with hierarchy levels.
- **Dim_Date.csv**: Comprehensive 4-year calendar table (1,461 daily records).
