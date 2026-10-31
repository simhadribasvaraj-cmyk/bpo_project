# VoiceServe BPO - Power BI Dashboard Click-by-Click Build Guide
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
1. **Total Headcount:** `[Total Headcount]` $ightarrow$ **2,500** (Callout color: `#1B365D`).
2. **Annual Attrition Rate:** `[Attrition Rate %]` $ightarrow$ **48.5%** (Callout color: `#D9534F`).
3. **Infant Mortality (<90 Days):** `[Early Attrition Share of Exits %]` $ightarrow$ **33.3%** of leavers (Color: `#D9534F`).
4. **Average Tenure:** `[Average Tenure (Months)]` $ightarrow$ **13.5 Mon** (Color: `#4A90E2`).
5. **Quality Score:** `[Average Quality Score %]` $ightarrow$ **89.0%** (Color: `#2E7D32`).
6. **Attendance Rate:** `[Average Attendance %]` $ightarrow$ **90.2%** (Color: `#F39C12`).
7. **Total Attrition Bleed:** `[Total Cost of Attrition (Crores)]` $ightarrow$ **₹9.10 Cr** (Callout color: `#D9534F`, Background: `#FDE8E8`).

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
  - *Category:* Recruitment (₹1.76 Cr) $ightarrow$ Training Sunk Cost (₹2.67 Cr) $ightarrow$ Lost Productivity (₹4.67 Cr) $ightarrow$ Total Bleed (₹9.10 Cr).

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
  - *Explain By:* `centre` $ightarrow$ `shift` $ightarrow$ `process` $ightarrow$ `low_hike_flag`.

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
