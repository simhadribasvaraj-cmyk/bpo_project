"""
================================================================================
VOICESERVE BPO - POWER BI ASSETS & STAR SCHEMA GENERATOR
DA-06: Employee Performance, Compensation and Attrition Trend Analysis
Team: DataVerse Squad, Codegnan
================================================================================
Generates import-ready CSVs for Star Schema modeling, complete DAX formulas,
and the complete dashboard build guide.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_employee_data.csv")
PBI_DIR = os.path.join(BASE_DIR, "powerbi")
os.makedirs(PBI_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("Preparing Power BI Star-Schema Datasets...")

# -------------------------------------------------------------
# 1. STAR SCHEMA TABLES
# -------------------------------------------------------------
# Dim_Centre
dim_centre = pd.DataFrame({
    "centre_id": [1, 2, 3],
    "centre": ["Hyderabad (Hitec City)", "Hyderabad (Gachibowli)", "Visakhapatnam (Rushikonda)"],
    "city": ["Hyderabad", "Hyderabad", "Visakhapatnam"],
    "tier": ["Tier-1 Metro", "Tier-1 Metro", "Tier-2 Coastal"],
    "facility_type": ["Main Campus", "Secondary Campus", "Regional Tech Park"]
})
dim_centre.to_csv(os.path.join(PBI_DIR, "Dim_Centre.csv"), index=False)

# Dim_Process
processes = df["process"].unique().tolist()
dim_process = pd.DataFrame({
    "process_id": list(range(1, len(processes) + 1)),
    "process": processes,
    "voice_flag": ["Voice" if "Voice" in p or "Inbound" in p or "Outbound" in p else "Non-Voice / Hybrid" for p in processes],
    "target_aht_seconds": [320, 240, 480, 0, 0]
})
dim_process.to_csv(os.path.join(PBI_DIR, "Dim_Process.csv"), index=False)

# Dim_Shift
shifts = ["Day", "Night", "Rotational"]
dim_shift = pd.DataFrame({
    "shift_id": [1, 2, 3],
    "shift": shifts,
    "shift_timing": ["08:00 AM - 05:00 PM", "09:00 PM - 06:00 AM", "Rotational (Weekly Changes)"],
    "night_allowance_eligible": ["No", "Yes", "Partial"]
})
dim_shift.to_csv(os.path.join(PBI_DIR, "Dim_Shift.csv"), index=False)

# Dim_Role
roles = df["role"].unique().tolist()
dim_role = pd.DataFrame({
    "role_id": list(range(1, len(roles) + 1)),
    "role": roles,
    "role_hierarchy_level": [1 if "Executive" in r and "Senior" not in r else (2 if "Senior" in r or "Specialist" in r else 3) for r in roles]
})
dim_role.to_csv(os.path.join(PBI_DIR, "Dim_Role.csv"), index=False)

# Dim_Date (Calendar Table: 2023-01-01 to 2026-12-31)
date_range = pd.date_range(start="2023-01-01", end="2026-12-31", freq="D")
dim_date = pd.DataFrame({
    "date": date_range.strftime("%Y-%m-%d"),
    "year": date_range.year,
    "quarter": "Q" + date_range.quarter.astype(str),
    "month_num": date_range.month,
    "month_name": date_range.strftime("%B"),
    "year_month": date_range.strftime("%Y-%m"),
    "day_of_week": date_range.strftime("%A"),
    "is_weekend": (date_range.weekday >= 5).astype(int)
})
dim_date.to_csv(os.path.join(PBI_DIR, "Dim_Date.csv"), index=False)

# Master Analytical Fact Table (Fact_Workforce)
# Map IDs
fact_df = df.copy()
fact_df = fact_df.merge(dim_centre[["centre", "centre_id"]], on="centre", how="left")
fact_df = fact_df.merge(dim_process[["process", "process_id"]], on="process", how="left")
fact_df = fact_df.merge(dim_shift[["shift", "shift_id"]], on="shift", how="left")
fact_df = fact_df.merge(dim_role[["role", "role_id"]], on="role", how="left")

fact_df.to_csv(os.path.join(PBI_DIR, "Fact_Workforce.csv"), index=False)
fact_df.to_csv(os.path.join(PBI_DIR, "VoiceServe_Master_PowerBI.csv"), index=False)

print(f"Exported Star Schema tables to {PBI_DIR}.")

# -------------------------------------------------------------
# 2. DAX MEASURES FILE (powerbi/DAX_Measures.dax)
# -------------------------------------------------------------
dax_content = """/*
================================================================================
VOICESERVE BPO - POWER BI DAX MEASURES SPECIFICATION
DA-06: Employee Performance, Compensation and Attrition Trend Analysis
Team: DataVerse Squad, Codegnan
================================================================================
Paste these measures into your Power BI Data Model under a dedicated '_Measures' table.
*/

-- =============================================================================
-- 1. HEADCOUNT & WORKFORCE VOLUME MEASURES
-- =============================================================================

Total Headcount = 
COUNTROWS(Fact_Workforce)
/* Measures total registered employee volume in the selected filter context */

Active Employees = 
CALCULATE(
    COUNTROWS(Fact_Workforce),
    Fact_Workforce[attrition_flag] = 0
)
/* Total employees who remain currently active / retained at VoiceServe */

Total Leavers = 
CALCULATE(
    COUNTROWS(Fact_Workforce),
    Fact_Workforce[attrition_flag] = 1
)
/* Total employees who have separated/exited from the organization */

-- =============================================================================
-- 2. ATTRITION RATE & RETENTION KPIs
-- =============================================================================

Attrition Rate % = 
DIVIDE([Total Leavers], [Total Headcount], 0)
/* Standardized Annual Attrition Rate % */

Early Leavers Count = 
CALCULATE(
    COUNTROWS(Fact_Workforce),
    Fact_Workforce[left_within_90_days] = 1
)
/* Count of employees leaving within their first 90 days of employment (Infant Mortality) */

Early Attrition Rate % = 
DIVIDE([Early Leavers Count], [Total Headcount], 0)
/* Share of total workforce leaving within the first 90 days */

Early Attrition Share of Exits % = 
DIVIDE([Early Leavers Count], [Total Leavers], 0)
/* Proportion of all company leavers who left within the first 90 days (Infant Mortality Share) */

Tenured Leavers Count = 
[Total Leavers] - [Early Leavers Count]
/* Exits occurring after 90 days of employment */

Average Tenure (Months) = 
AVERAGE(Fact_Workforce[tenure_months])
/* Mean duration of employment in months across selected segment */

Average Tenure of Leavers = 
CALCULATE(
    AVERAGE(Fact_Workforce[tenure_months]),
    Fact_Workforce[attrition_flag] = 1
)
/* Average months of service completed by employees before exiting */

-- =============================================================================
-- 3. FINANCIAL & ATTRITION COST MEASURES (ADJUSTABLE)
-- =============================================================================

Recruitment Unit Cost = 14500
/* Average agency sourcing, job board, and HR recruiter cost per replacement hire in INR */

Training Unit Cost = 22000
/* Classroom induction trainer salary, LMS license, and equipment cost per new hire in INR */

Lost Productivity Early Unit Cost = 18500
/* Sunk training stipend and negative productivity ROI for leavers exiting <= 90 days */

Lost Productivity Tenured Unit Cost = 48500
/* 45-day queue vacancy loss, TL overtime payout, and 90-day learning curve ramp in INR */

Blended Cost per Early Leaver = 
[Recruitment Unit Cost] + [Training Unit Cost] + [Lost Productivity Early Unit Cost]
/* INR 55,000 per early exit */

Blended Cost per Tenured Leaver = 
[Recruitment Unit Cost] + [Training Unit Cost] + [Lost Productivity Tenured Unit Cost]
/* INR 85,000 per tenured exit */

Total Cost of Early Attrition = 
[Early Leavers Count] * [Blended Cost per Early Leaver]
/* Aggregate financial loss from infant mortality exits */

Total Cost of Tenured Attrition = 
[Tenured Leavers Count] * [Blended Cost per Tenured Leaver]
/* Aggregate financial loss from tenured employee turnover */

Total Cost of Attrition = 
[Total Cost of Early Attrition] + [Total Cost of Tenured Attrition]
/* Comprehensive annualized financial bleed from employee attrition */

Total Cost of Attrition (Crores) = 
DIVIDE([Total Cost of Attrition], 10000000, 0)
/* Total attrition cost formatted in Indian Crores (₹ Cr) */

-- =============================================================================
-- 4. COMPENSATION & PERFORMANCE MEASURES
-- =============================================================================

Average Base Salary = 
AVERAGE(Fact_Workforce[monthly_salary])
/* Mean monthly base salary in INR */

Average Incentive Amount = 
AVERAGE(Fact_Workforce[incentive_amount])
/* Mean monthly variable incentive earned in INR */

Average Total Monthly Pay = 
AVERAGE(Fact_Workforce[total_pay])
/* Mean total monthly compensation (Salary + Incentive) in INR */

Average Last Hike % = 
AVERAGE(Fact_Workforce[last_hike_percent])
/* Mean percentage hike received during the most recent performance appraisal */

Low Hike Employee Count = 
CALCULATE(
    COUNTROWS(Fact_Workforce),
    Fact_Workforce[low_hike_flag] = 1
)
/* Employees with tenure >= 6 months who received an appraisal hike < 6.0% */

Low Hike Attrition Rate % = 
CALCULATE(
    [Attrition Rate %],
    Fact_Workforce[low_hike_flag] = 1
)
/* Attrition rate among employees subject to low appraisal hikes */

Average Quality Score % = 
AVERAGE(Fact_Workforce[avg_quality_score])
/* Mean call/ticket quality audit score */

Average Customer Rating = 
AVERAGE(Fact_Workforce[avg_customer_rating])
/* Mean CSAT customer rating (1.0 to 5.0 scale) */

Average Attendance % = 
AVERAGE(Fact_Workforce[avg_attendance_percent])
/* Mean monthly attendance percentage */

Average Engagement Survey Score = 
AVERAGE(Fact_Workforce[survey_score])
/* Mean annual employee engagement survey score (1.0 to 5.0 scale) */

-- =============================================================================
-- 5. RISK & TARGETING DAX MEASURES
-- =============================================================================

High Risk Active Employees = 
CALCULATE(
    COUNTROWS(Fact_Workforce),
    Fact_Workforce[attrition_flag] = 0,
    Fact_Workforce[avg_attendance_percent] < 88.0 || 
    (Fact_Workforce[shift] = "Night" && Fact_Workforce[low_hike_flag] = 1) ||
    Fact_Workforce[survey_score] < 3.0
)
/* Active employees demonstrating critical turnover warning signs */
"""

with open(os.path.join(PBI_DIR, "DAX_Measures.dax"), "w", encoding="utf-8") as f:
    f.write(dax_content)

# -------------------------------------------------------------
# 3. STAR SCHEMA DOCUMENTATION (powerbi/Star_Schema_Model.md)
# -------------------------------------------------------------
star_schema_doc = """# VoiceServe BPO - Power BI Star-Schema Data Model Specification
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
| **Dim_Centre** | `centre_id` | **Fact_Workforce** | `centre_id` | $1 : *$ (One-to-Many) | Single (Dim $\rightarrow$ Fact) |
| **Dim_Process** | `process_id` | **Fact_Workforce** | `process_id` | $1 : *$ (One-to-Many) | Single (Dim $\rightarrow$ Fact) |
| **Dim_Shift** | `shift_id` | **Fact_Workforce** | `shift_id` | $1 : *$ (One-to-Many) | Single (Dim $\rightarrow$ Fact) |
| **Dim_Role** | `role_id` | **Fact_Workforce** | `role_id` | $1 : *$ (One-to-Many) | Single (Dim $\rightarrow$ Fact) |
| **Dim_Date** | `date` | **Fact_Workforce** | `join_date` | $1 : *$ (Active) | Single (Dim $\rightarrow$ Fact) |
| **Dim_Date** | `date` | **Fact_Workforce** | `exit_date` | $1 : *$ (Inactive) | Single (Dim $\rightarrow$ Fact) |

*(Note: The `exit_date` relationship is kept inactive and invoked in DAX via `USERELATIONSHIP(Fact_Workforce[exit_date], Dim_Date[date])` when plotting leaver cohorts over time).*

---

## 3. Dimension & Fact Details
- **Fact_Workforce.csv**: 2,500 rows, 34 columns. Contains all employee records, transactional performance aggregates, compensation fields, and retention flags.
- **Dim_Centre.csv**: 3 centres (Hyderabad Hitec City, Hyderabad Gachibowli, Visakhapatnam Rushikonda).
- **Dim_Process.csv**: 5 operations processes (Inbound Customer Service, Outbound Sales, Technical Support, Chat & Email Support, Claims & Back Office).
- **Dim_Shift.csv**: 3 shifts (Day, Night, Rotational) with policy attributes.
- **Dim_Role.csv**: 5 operational roles with hierarchy levels.
- **Dim_Date.csv**: Comprehensive 4-year calendar table (1,461 daily records).
"""

with open(os.path.join(PBI_DIR, "Star_Schema_Model.md"), "w", encoding="utf-8") as f:
    f.write(star_schema_doc)

# -------------------------------------------------------------
# 4. DASHBOARD BUILD GUIDE (powerbi/Dashboard_Build_Guide.md)
# -------------------------------------------------------------
build_guide = """# VoiceServe BPO - Power BI Dashboard Click-by-Click Build Guide
**Problem DA-06: Employee Performance, Compensation and Attrition Trend Analysis**
**Team:** DataVerse Squad, Codegnan
**Files Provided:** `Fact_Workforce.csv`, `Dim_Centre.csv`, `Dim_Process.csv`, `Dim_Shift.csv`, `Dim_Role.csv`, `Dim_Date.csv`, `DAX_Measures.dax`

---

## 1. Canvas Settings & Executive Theme Palette
- **Canvas Size:** 16:9 widescreen (1280 x 720 px or 1920 x 1080 px).
- **Background Color:** `#F8F9FA` (Soft Off-White).
- **Card / Container Fill:** `#FFFFFF` (Pure White) with subtle drop shadow (Blur: 8px, Transparency: 85%).
- **Color Palette:**
  - **Primary Corporate:** `#1B365D` (Deep Navy Blue)
  - **Secondary Brand:** `#4A90E2` (Vibrant Blue)
  - **Alert / Attrition Leavers:** `#D9534F` (Coral Crimson Red)
  - **Retention / Active Stayers:** `#2E7D32` (Forest Emerald Green)
  - **Warning / Neutral:** `#F39C12` (Amber Orange)
  - **Neutral Gray:** `#7F8C8D` (Slate Gray)

---

## 2. Global Header & Filter Slicers (Present on All Pages)
At the top of every dashboard page, insert an executive header strip (Height: 70px, Fill: `#1B365D`):
- **Title Text:** "VOICESERVE BPO | WORKFORCE PERFORMANCE & RETENTION COCKPIT" (Font: Segoe UI, Size 18, Bold, Color: White).
- **Subtitle Text:** "Enterprise Attrition Intelligence & Cost Governance Dashboard" (Size 10, Color: `#BDC3C7`).
- **Global Slicers Banner (Horizontal Tile / Dropdown Slicers):**
  1. **Operating Centre** (`Dim_Centre[centre]` - Dropdown, Multi-select with Search).
  2. **Process Line** (`Dim_Process[process]` - Dropdown).
  3. **Work Shift** (`Dim_Shift[shift]` - Horizontal Pill/Tile).
  4. **Job Role** (`Dim_Role[role]` - Dropdown).
  5. **Tenure Band** (`Fact_Workforce[tenure_band]` - Dropdown).

---

## 3. Page-by-Page Layout Specifications

### PAGE 1: EXECUTIVE SUMMARY (Overview & Financial Exposure)
*Target Audience: Chief Operating Officer, VP of HR, Chief Financial Officer*

#### A. Top Row: 7 KPI Cards (Card Visuals, Font: Segoe UI Bold, Height: 90px)
1. **Total Headcount:** `[Total Headcount]` $\rightarrow$ **2,500** (Callout color: `#1B365D`).
2. **Annual Attrition Rate:** `[Attrition Rate %]` $\rightarrow$ **48.5%** (Callout color: `#D9534F`).
3. **Infant Mortality (<90 Days):** `[Early Attrition Share of Exits %]` $\rightarrow$ **33.3%** of leavers (Color: `#D9534F`).
4. **Average Tenure:** `[Average Tenure (Months)]` $\rightarrow$ **13.5 Mon** (Color: `#4A90E2`).
5. **Quality Score:** `[Average Quality Score %]` $\rightarrow$ **89.0%** (Color: `#2E7D32`).
6. **Attendance Rate:** `[Average Attendance %]` $\rightarrow$ **90.2%** (Color: `#F39C12`).
7. **Total Attrition Bleed:** `[Total Cost of Attrition (Crores)]` $\rightarrow$ **₹9.10 Cr** (Callout color: `#D9534F`, Background: `#FDE8E8`).

#### B. Main Visuals Grid
- **Visual 1 (Top Left - Donut Chart):** "Attrition Status Composition"
  - *Values:* `[Total Leavers]` (Crimson `#D9534F`) vs `[Active Employees]` (Navy `#1B365D`).
  - *Insight:* Shows the 48.5% vs 51.5% split at a glance.
- **Visual 2 (Top Right - Clustered Column & Line Chart):** "Monthly Exits Trend vs Headcount"
  - *Shared Axis:* `Dim_Date[year_month]`.
  - *Column Values:* `[Total Leavers]`.
  - *Line Values:* `[Attrition Rate %]`.
  - *Colors:* Columns `#4A90E2`, Line `#D9534F` (Width 3px).
- **Visual 3 (Bottom Left - Clustered Bar Chart):** "Attrition Rate by Process Service Line"
  - *Y-Axis:* `Dim_Process[process]`.
  - *X-Axis:* `[Attrition Rate %]`.
  - *Data Labels:* ON. Outbound Sales (61.2%) clearly highlighted in dark red.
- **Visual 4 (Bottom Right - Financial Waterfall Chart):** "Attrition Cost Breakdown by Component"
  - *Category:* Recruitment (₹1.76 Cr) $\rightarrow$ Training Sunk Cost (₹2.67 Cr) $\rightarrow$ Lost Productivity (₹4.67 Cr) $\rightarrow$ Total Bleed (₹9.10 Cr).

---

### PAGE 2: ATTRITION DRIVERS (Root Cause & Shift Dynamics)
*Target Audience: VP Operations, Shift Delivery Managers*

#### Visuals:
- **Visual 1 (Top Left - 100% Stacked Bar Chart):** "Attrition Rate % by Shift Schedule"
  - *Y-Axis:* `Dim_Shift[shift]` (Night, Rotational, Day).
  - *X-Axis:* `[Total Leavers]` vs `[Active Employees]`.
  - *Data Labels:* Percentage. Displays Night Shift attrition (57.3%) vs Day Shift (41.7%).
- **Visual 2 (Top Right - Grouped Column Chart):** "Appraisal Hike Tier vs Attrition Rate by Shift"
  - *X-Axis:* Appraisal Hike Tier (`<6% Low`, `6-10% Medium`, `>10% High`).
  - *Y-Axis:* `[Attrition Rate %]`.
  - *Legend:* `Dim_Shift[shift]`.
  - *Callout:* Clearly visualizes the **68.4% spike** for Night Shift employees receiving a sub-6% hike.
- **Visual 3 (Bottom Left - Scatter Plot):** "Attendance Collapse vs Attrition Propensity"
  - *X-Axis:* `[Average Attendance %]` (Range: 60% to 100%).
  - *Y-Axis:* `[Average Quality Score %]`.
  - *Legend:* `Fact_Workforce[attrition_flag]` (0 = Active, 1 = Exited).
  - *Trendline:* ON. Demonstrates that attendance dips below 88% strongly predict imminent departure.
- **Visual 4 (Bottom Right - Table / Matrix Visual):** "Operational Risk Matrix"
  - *Rows:* `centre`, `process`, `shift`.
  - *Values:* `[Total Headcount]`, `[Total Leavers]`, `[Attrition Rate %]`, `[Total Cost of Attrition]`.
  - *Conditional Formatting:* Data bars on Attrition Rate % (Color: Red gradient).

---

### PAGE 3: PAY & PERFORMANCE (Compensation Equity & Star Retention)
*Target Audience: Compensation & Benefits (C&B) Lead, HR Business Partners*

#### Visuals:
- **Visual 1 (Top Left - Matrix Visual):** "Performer Category Compensation Profile"
  - *Rows:* `Fact_Workforce[performer_category]` (High, Medium, Low).
  - *Values:* `[Total Headcount]`, `[Average Base Salary]`, `[Average Incentive Amount]`, `[Average Total Monthly Pay]`, `[Average Quality Score %]`, `[Attrition Rate %]`.
  - *Insight:* Highlights wage compression where High Performers earn virtually identical base salary (₹28,082) as Medium Performers (₹28,492), driving 43.0% star attrition.
- **Visual 2 (Top Right - Clustered Column Chart):** "Incentive vs Base Salary Spread by Role"
  - *X-Axis:* `Dim_Role[role]`.
  - *Y-Axis:* `[Average Base Salary]` and `[Average Incentive Amount]`.
- **Visual 3 (Bottom Left - Box & Whisker / Distribution Chart):** "Total Pay Distribution of Leavers vs Stayers"
  - *Category:* `Fact_Workforce[attrition_flag]` (Active vs Exited).
  - *Value:* `Fact_Workforce[total_pay]`.
- **Visual 4 (Bottom Right - Multi-Row Card / KPI List):** "Star Performer Flight Exposure"
  - *Metrics:* 546 High Performers Lost, ₹4.64 Cr Financial Loss in Star Talent, Average CSAT of Leavers: 4.44.

---

### PAGE 4: EARLY ATTRITION & INFANT MORTALITY (<90 DAYS)
*Target Audience: Training Director, Talent Acquisition Head, Onboarding Leads*

#### Visuals:
- **Visual 1 (Top Left - Donut Chart):** "Infant Mortality Share (<90 Days vs Tenured Exits)"
  - *Slices:* Early Exits (404 leavers, 33.3%) vs Tenured Exits (809 leavers, 66.7%).
- **Visual 2 (Top Right - Clustered Column Chart):** "Early Exits by Tenure Band"
  - *X-Axis:* `Fact_Workforce[tenure_band]` (`0-3 Months`, `3-6 Months`, `6-12 Months`, `1-2 Years`, `2+ Years`).
  - *Y-Axis:* `[Total Leavers]`.
- **Visual 3 (Bottom Left - Bar Chart):** "Notice Period Compliance in Early Exits"
  - *Y-Axis:* `Fact_Workforce[notice_served]` (No vs Yes).
  - *X-Axis:* `[Early Leavers Count]`.
  - *Annotation:* 78.2% of early leavers abscond without serving notice.
- **Visual 4 (Bottom Right - Treemap):** "Early Exit Concentration by Process & Shift"
  - *Group:* `Dim_Process[process]`.
  - *Details:* `Dim_Shift[shift]`.
  - *Values:* `[Early Leavers Count]`.
  - *Color Saturation:* `[Early Attrition Rate %]`.

---

### PAGE 5: CENTRE-WISE COMPARISON (Multi-Location Operational Audit)
*Target Audience: Managing Director, Facility Heads (Hyderabad vs Visakhapatnam)*

#### Visuals:
- **Visual 1 (Top Left - Gauge / KPI Cards):** Centre Headcount & Attrition Overview
  - Hyderabad Hitec City: 1,125 Headcount | 48.0% Attrition | ₹4.09 Cr Bleed.
  - Hyderabad Gachibowli: 750 Headcount | 47.9% Attrition | ₹2.73 Cr Bleed.
  - Visakhapatnam Rushikonda: 625 Headcount | 50.2% Attrition | ₹2.28 Cr Bleed.
- **Visual 2 (Top Right - Clustered Column Chart):** "Centre Attrition Comparison by Shift"
  - *X-Axis:* `Dim_Centre[centre]`.
  - *Y-Axis:* `[Attrition Rate %]`.
  - *Legend:* `Dim_Shift[shift]`.
  - *Key Callout:* Rushikonda Night Shift reaches **60.5% attrition** due to public transport collapse and cab routing bottlenecks.
- **Visual 3 (Bottom Left - Radar / Spider or Grouped Bar Chart):** "Operational Health Scorecard across Centres"
  - Compares Quality Score %, Attendance %, Survey Engagement, and Training Hours across the 3 locations.
- **Visual 4 (Bottom Right - Decomposition Tree):** "Root Cause Explorer: What is Driving Exits?"
  - *Analyze:* `[Total Leavers]`.
  - *Explain By:* `centre` $\rightarrow$ `shift` $\rightarrow$ `process` $\rightarrow$ `low_hike_flag`.

---

## 4. Step-by-Step Instructions to Build the .pbix in Power BI Desktop
1. Open **Power BI Desktop**. Click **Get Data > Text/CSV**.
2. Select and import the following files from the `powerbi/` folder:
   - `Dim_Centre.csv`
   - `Dim_Process.csv`
   - `Dim_Shift.csv`
   - `Dim_Role.csv`
   - `Dim_Date.csv`
   - `Fact_Workforce.csv`
3. Click **Transform Data** (Power Query):
   - Verify that column data types are recognized (Dates as Date, IDs as Text/Integer, Pay as Decimal).
   - Click **Close & Apply**.
4. Go to **Model View** (left pane):
   - Create 1-to-many relationships from Dim tables to Fact table as detailed in `Star_Schema_Model.md`.
5. Create a Measures Table:
   - Click **Enter Data**, name the table `_Measures`, click Load.
   - Click **New Measure** and copy-paste the DAX formulas from `DAX_Measures.dax`.
6. Build Pages 1 through 5 following the exact visual layout specifications outlined above.
7. Save the report as `VoiceServe_Attrition_Analytics.pbix` and export pages to PDF via **File > Export > Export to PDF**.
"""

with open(os.path.join(PBI_DIR, "Dashboard_Build_Guide.md"), "w", encoding="utf-8") as f:
    f.write(build_guide)

print("SUCCESS: All Power BI assets, DAX measures, Star-Schema docs, and build guides generated.")
