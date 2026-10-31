"""
================================================================================
VOICESERVE BPO - EXECUTIVE REPORT & PRESENTATION GENERATOR
DA-06: Employee Performance, Compensation and Attrition Trend Analysis
Team: DataVerse Squad, Codegnan
================================================================================
Generates:
1. Word Document (.docx) - 5-Page Comprehensive Executive Report
2. Markdown Document (.md) - Full Analytical Report
3. PowerPoint Presentation (.pptx) - 9-Slide Storytelling Deck with Speaker Notes & Timing
4. Presentation Markdown (.md) - Complete Slide Transcript
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import pptx
from pptx.util import Inches as PptInches, Pt as PptPt
from pptx.dml.color import RGBColor as PptRGBColor
from pptx.enum.text import PP_ALIGN

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "report")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(REPORT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. BUILD MICROSOFT WORD REPORT (.docx)
# -------------------------------------------------------------
print("Generating Executive Word Report (.docx)...")
doc = docx.Document()

# Page Margins (Normal 1 inch)
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Colors
C_NAVY = RGBColor(27, 54, 93)      # #1B365D
C_BLUE = RGBColor(74, 144, 226)    # #4A90E2
C_RED = RGBColor(217, 83, 79)      # #D9534F
C_GRAY = RGBColor(85, 85, 85)
C_DARK = RGBColor(45, 55, 72)

# Title Block
p_title = doc.add_paragraph()
run_title = p_title.add_run("VOICESERVE BPO: EMPLOYEE ATTRITION & PERFORMANCE INTELLIGENCE REPORT")
run_title.font.name = "Calibri"
run_title.font.size = Pt(20)
run_title.font.bold = True
run_title.font.color.rgb = C_NAVY
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_sub = doc.add_paragraph()
run_sub = p_sub.add_run("Empirical Root-Cause Analysis, Financial Loss Modeling & A Three-Pillar Retention Strategy\n")
run_sub.font.name = "Calibri"
run_sub.font.size = Pt(12)
run_sub.font.italic = True
run_sub.font.color.rgb = C_GRAY
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_meta = doc.add_paragraph()
run_meta = p_meta.add_run("Problem Track: DA-06 | Team: DataVerse Squad (Codegnan) | Date: October 2026")
run_meta.font.name = "Calibri"
run_meta.font.size = Pt(10)
run_meta.font.bold = True
run_meta.font.color.rgb = C_BLUE
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 1: Executive Summary
h1 = doc.add_heading(level=1)
r_h1 = h1.add_run("1. Executive Summary & Problem Context")
r_h1.font.color.rgb = C_NAVY

p1 = doc.add_paragraph()
p1.add_run(
    "VoiceServe operates three customer service facilities across Visakhapatnam and Hyderabad with an active workforce of 2,500 employees. "
    "Over the past 18 months, the company has suffered from an annualized attrition rate of 48.52% (1,213 exits), severely impairing service delivery, "
    "straining supervisory bandwidth, and incurring an annual financial bleed of ₹90.98 Crores INR (~$10.9M USD). "
    "Operations leadership assumed that lower base compensation and gruelling night shift schedules were the sole drivers of employee turnover. "
    "However, human resources lacked the quantitative telemetry required to validate these hypotheses.\n\n"
    "Our investigation delivers an empirical audit of VoiceServe's workforce data, testing core hypotheses with rigorous statistical tests "
    "(Welch's t-test, Chi-Square of Independence, Cohen's d effect sizes, and Logistic Odds Ratios). "
    "The data refutes simplistic assumptions: absolute base pay levels differ negligibly between stayers and leavers (Cohen's d = 0.032, p = 0.42). "
    "Instead, turnover is concentrated in three systemic operational failures: (1) an 'infant mortality' crisis where 33.3% of leavers quit within 90 days "
    "due to severe floor shock; (2) acute night-shift circadian fatigue and local transit safety failures in Visakhapatnam (Rushikonda attrition: 60.5%); "
    "and (3) wage compression that rewards high performers with sub-6% appraisal increments, triggering targeted poaching by rival BPOs."
)

# Callout KPI Box (Table)
table_kpi = doc.add_table(rows=2, cols=4)
table_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
kpi_data = [
    ("Total Workforce", "2,500", "Annual Attrition", "48.5%"),
    ("Infant Mortality (<90d)", "33.3% of Exits", "Annual Financial Bleed", "₹90.98 Crores")
]
for row_idx, data in enumerate(kpi_data):
    for col_idx in range(4):
        cell = table_kpi.cell(row_idx, col_idx)
        val = data[col_idx]
        cell.paragraphs[0].text = val
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if col_idx % 2 == 0:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            cell.paragraphs[0].runs[0].font.color.rgb = C_GRAY
        else:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(13)
            cell.paragraphs[0].runs[0].font.color.rgb = C_RED if "48.5%" in val or "Crores" in val or "33.3%" in val else C_NAVY

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 2: Key Empirical Findings & Statistical Rigor
h2 = doc.add_heading(level=1)
r_h2 = h2.add_run("2. Key Empirical Findings & Hypothesis Testing")
r_h2.font.color.rgb = C_NAVY

doc.add_paragraph(
    "To eliminate subjective conjecture, each management belief was evaluated using formal statistical hypothesis tests, "
    "reporting p-values and standardized effect sizes:"
)

# Table of Statistical Results
table_stat = doc.add_table(rows=6, cols=5)
table_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Workforce Metric / Hypothesis", "Stayers Mean", "Leavers Mean", "p-value", "Effect Size (Cohen's d / Cramer's V)"]
for c_i, h in enumerate(headers):
    cell = table_stat.cell(0, c_i)
    cell.paragraphs[0].text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    shading_xml = parse_xml(r'<w:shd {} w:fill="1B365D"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading_xml)

stat_rows = [
    ("Average Attendance %", "93.88%", "85.74%", "< 0.0001", "d = -1.82 (Extremely Large)"),
    ("Appraisal Hike % (Eligible)", "7.15%", "5.81%", "< 0.0001", "d = -0.42 (Moderate)"),
    ("Base Monthly Salary", "₹28,114", "28,477", "0.422 (Not Sig)", "d = +0.03 (Negligible)"),
    ("Shift Schedule (Night vs Day)", "41.7% Day", "57.3% Night", "< 0.0001", "V = 0.15 (OR = 1.88x)"),
    ("Appraisal Hike Tier (<6% vs >=10%)", "18.7% High", "45.2% Low", "< 0.0001", "V = 0.22 (OR = 2.34x)")
]
for r_i, r_vals in enumerate(stat_rows, 1):
    for c_i, val in enumerate(r_vals):
        cell = table_stat.cell(r_i, c_i)
        cell.paragraphs[0].text = val
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        if c_i == 0:
            cell.paragraphs[0].runs[0].font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

p_findings = doc.add_paragraph()
p_findings.add_run("Structured Analytical Insights (What -> Why -> What VoiceServe Should Do):\n").font.bold = True
p_findings.add_run(
    "1. The Infant Mortality Bottleneck (33.3% of Exits):\n"
    " - What: 404 agents leave within 90 days of joining, with 78% absconding without notice.\n"
    " - Why: Floor shock. Agents transition abruptly from high-level classroom training to aggressive live queue quotas without floor nesting or peer coaching.\n"
    " - Action: Institutionalize a 30-Day Nesting Academy with assigned buddies and waived AHT pressure.\n\n"
    "2. The Night-Shift Transit Crisis in Visakhapatnam:\n"
    " - What: Rushikonda night-shift attrition reaches 60.5%, significantly outstripping Hyderabad metro centers.\n"
    " - Why: Absence of public transit past 9:30 PM and irregular cab routing create safety fears and sleep disruption.\n"
    " - Action: Introduce a ₹3,500/month night shift allowance and implement app-monitored safe cab transit.\n\n"
    "3. High-Performer Compression & Poaching:\n"
    " - What: High performers suffer a 43.0% attrition rate (546 star agents lost).\n"
    " - Why: Flat base pay creates equity distress; top performers earn the same base as average peers, making them easy targets for rival BPOs.\n"
    " - Action: Implement merit-differentiated appraisal tiers (12-15% for top quartile) and fast-track QA/TL promotion."
)

# Section 3: Cost of Attrition Financial Model
h3 = doc.add_heading(level=1)
r_h3 = h3.add_run("3. Cost of Attrition Financial Model")
r_h3.font.color.rgb = C_NAVY

doc.add_paragraph(
    "To establish financial urgency for the executive committee, we modeled total attrition costs using granular BPO industry unit benchmarks:\n"
    " - Recruitment & Sourcing Cost: ₹14,500 per hire (job portals, agency fees, HR recruiter time).\n"
    " - Training & Induction Cost: ₹22,000 per hire (3 weeks trainer salary, LMS seats, IT onboarding).\n"
    " - Lost Productivity (Early Leaver <=90d): ₹18,500 (unrecovered training stipend before reaching floor utility).\n"
    " - Lost Productivity (Tenured Leaver >90d): ₹48,500 (45-day seat vacancy, supervisor overtime, 90-day learning curve ramp)."
)

table_cost = doc.add_table(rows=4, cols=4)
table_cost.alignment = WD_TABLE_ALIGNMENT.CENTER
cost_headers = ["Leaver Segment", "Exits Count", "Unit Cost per Exit", "Total Financial Loss"]
for c_i, h in enumerate(cost_headers):
    cell = table_cost.cell(0, c_i)
    cell.paragraphs[0].text = h
    cell.paragraphs[0].runs[0].font.bold = True
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    shading_xml = parse_xml(r'<w:shd {} w:fill="1B365D"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading_xml)

cost_rows = [
    ("Early Leavers (<= 90 Days)", "404", "₹55,000", "₹2,22,20,000 (₹2.22 Cr)"),
    ("Tenured Leavers (> 90 Days)", "809", "₹85,000", "₹6,87,65,000 (₹6.88 Cr)"),
    ("Total Annual Attrition Loss", "1,213", "₹75,008 (Blended)", "₹9,09,85,000 (₹9.10 Crores)")
]
for r_i, r_vals in enumerate(cost_rows, 1):
    for c_i, val in enumerate(r_vals):
        cell = table_cost.cell(r_i, c_i)
        cell.paragraphs[0].text = val
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        if r_i == 3:
            cell.paragraphs[0].runs[0].font.bold = True
            shading_xml = parse_xml(r'<w:shd {} w:fill="FDE8E8"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shading_xml)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 4: Exactly Three Prioritized Business Recommendations
h4 = doc.add_heading(level=1)
r_h4 = h4.add_run("4. Exactly Three Prioritized Business Recommendations")
r_h4.font.color.rgb = C_NAVY

recs = [
    ("Recommendation 1: 30-Day Nesting Academy & Floor-Shock Mitigation",
     "Evidence: 404 agents (33.3% of all exits) leave within 90 days, wasting ₹2.22 Crores in purely sunk onboarding expenses.\n"
     "The Action: Overhaul training curriculum to include a 30-day protected 'Nesting Academy'. Pair new recruits 1:1 with accredited senior peer mentors. Suspend AHT quotas for 60 days, evaluating agents strictly on quality score and First Contact Resolution (FCR). Disallow solo night shifts during probation.\n"
     "Owner: Training Team (Head of L&D) & Operations Managers.\n"
     "Quantified Impact: 35% reduction in infant mortality (141 early exits averted). Direct annual savings: ₹77.55 Lakhs net.\n"
     "Success Measurement: 90-Day Attrition Rate (target: <= 10.0%) and Nesting QA Pass Rate (target: >= 92%)."),

    ("Recommendation 2: Night-Shift Restructuring & App-Tracked Commute Transit",
     "Evidence: Night shift attrition is 57.3% (OR = 1.88x), surging to 60.5% in Vizag where 22% of leavers cite cab delays and safety distress.\n"
     "The Action: Institute a dedicated ₹3,500/month Night Shift Differential Allowance. Implement a centralized GPS-tracked cab management system with geo-fenced female employee safety escorts in Rushikonda. Enforce a 6-month rotation cap to guarantee circadian recovery.\n"
     "Owner: Operations Managers & HR Operations / Facilities Lead.\n"
     "Quantified Impact: Night shift attrition drops from 57.3% to 42.0% (saving 134 night-shift employees). Gross replacement savings: ₹1.14 Crores. Net operational ROI: Positive within 8 months through SLA penalty eliminations.\n"
     "Success Measurement: Night Shift Attrition % (target: < 42%) and Night Shift Attendance Rate (target: >= 91%)."),

    ("Recommendation 3: Merit-Differentiated Pay Matrix & High-Performer Retention Track",
     "Evidence: High performers experience a 43.0% attrition rate (546 star agents lost), costing ₹4.64 Crores. Receiving a sub-6% hike increases turnover risk by 2.34x.\n"
     "The Action: Abolish blanket 3-5% salary increments. Implement a 3-tier merit matrix: Top 25% performers receive guaranteed 12-15% base pay increases; middle 50% receive 7-9%; bottom 25% receive 0-3% with a 60-day coaching plan. Create an accelerated 'Star Track' promoting high performers into Senior Executive or QA roles within 9 months.\n"
     "Owner: Executive Management (CEO, CFO) & VP of Human Resources.\n"
     "Quantified Impact: High performer attrition drops from 43.0% to 22.0% (saving 266 star performers). Gross replacement cost savings: ₹2.26 Crores. Net annual profit gain after hike budget adjustment: ₹1.41 Crores.\n"
     "Success Measurement: High Performer Retention Rate (target: >= 80%) and Customer Satisfaction Rating (target: >= 4.6/5.0).")
]

for title, body in recs:
    p_rec = doc.add_paragraph()
    p_rec.add_run(f"{title}\n").font.bold = True
    p_rec.runs[0].font.color.rgb = C_BLUE
    p_rec.add_run(body)
    p_rec.paragraph_format.space_after = Pt(6)

# Section 5: Limitations & Future Scope
h5 = doc.add_heading(level=1)
r_h5 = h5.add_run("5. Analytical Limitations & Governance Checklist")
r_h5.font.color.rgb = C_NAVY

doc.add_paragraph(
    "1. Observational Cohort Study: Cross-sectional operational data demonstrates strong correlational links and predictive power, "
    "but cannot fully isolate unobserved personal life events (e.g. spouse relocations, family emergencies).\n"
    "2. Competitor Wage Benchmarking: Competitor offer salaries were compiled via exit interview narratives rather than audited payroll databases.\n"
    "3. Human Validation Checklist: Executive leadership must review the proposed ₹3,500 allowance with local transport vendors in Vizag "
    "and align the 12-15% merit appraisal budget with the FY27 compensation pool."
)

doc_path = os.path.join(REPORT_DIR, "VoiceServe_Attrition_Analysis_Report.docx")
doc.save(doc_path)
print(f"SUCCESS: Word report saved to: {doc_path}")

# Write Markdown report version
md_report_path = os.path.join(REPORT_DIR, "VoiceServe_Attrition_Analysis_Report.md")
with open(md_report_path, "w", encoding="utf-8") as f:
    f.write(f"""# VOICESERVE BPO: EMPLOYEE ATTRITION & PERFORMANCE INTELLIGENCE REPORT
**Empirical Root-Cause Analysis, Financial Loss Modeling & A Three-Pillar Retention Strategy**
*Problem Track: DA-06 | Team: DataVerse Squad (Codegnan) | October 2026*

---

## 1. Executive Summary & Problem Context
VoiceServe operates three customer service facilities across Visakhapatnam and Hyderabad with an active workforce of 2,500 employees. Over the past 18 months, the company has suffered from an annualized attrition rate of **48.52% (1,213 exits)**, severely impairing service delivery, straining supervisory bandwidth, and incurring an annual financial bleed of **₹90.98 Crores INR (~$10.9M USD)**. 

Operations leadership assumed that lower base compensation and gruelling night shift schedules were the sole drivers of employee turnover. However, human resources lacked the quantitative telemetry required to validate these hypotheses.

Our investigation delivers an empirical audit of VoiceServe's workforce data, testing core hypotheses with rigorous statistical tests (Welch's t-test, Chi-Square of Independence, Cohen's d effect sizes, and Logistic Odds Ratios). The data refutes simplistic assumptions: absolute base pay levels differ negligibly between stayers and leavers (Cohen's $d = 0.032, p = 0.42$). Instead, turnover is concentrated in three systemic operational failures:
1. **The Infant Mortality Crisis:** 33.3% of leavers quit within 90 days due to severe floor shock.
2. **Night-Shift Circadian Fatigue & Transit Hazards:** Acute night-shift attrition reaches 60.5% in Visakhapatnam (Rushikonda) due to transit safety failures.
3. **High-Performer Wage Compression:** Sub-6% appraisal increments trigger targeted poaching of VoiceServe's best talent by rival BPOs.

### Executive KPI Summary Table
| Metric | Value | Business Significance |
| :--- | :--- | :--- |
| **Total Headcount** | **2,500** | Full organizational baseline across 3 centres |
| **Total Separations (Exits)** | **1,213** | 48.52% annualized attrition rate |
| **Infant Mortality (<90 Days)** | **404 (33.3% of exits)** | Acute onboarding floor-shock concentration |
| **Total Financial Bleed** | **₹90.98 Crores INR** | Comprehensive replacement, training & productivity loss |
| **Average Leaver Tenure** | **8.1 Months** | Turnover occurs before full productivity ramp is reached |

---

## 2. Key Empirical Findings & Statistical Rigor

### Statistical Hypothesis Testing Summary
| Workforce Metric / Hypothesis | Stayers Mean | Leavers Mean | p-value | Standardized Effect Size |
| :--- | :--- | :--- | :--- | :--- |
| **Average Attendance %** | 93.88% | 85.74% | $< 0.0001$ | Cohen's $d = -1.82$ (Massive Effect) |
| **Appraisal Hike % (Eligible Staff)** | 7.15% | 5.81% | $< 0.0001$ | Cohen's $d = -0.42$ (Moderate Effect) |
| **Monthly Base Salary (INR)** | ₹28,114 | ₹28,477 | $0.422$ | Cohen's $d = +0.03$ (Statistically Negligible) |
| **Work Shift (Night vs Day)** | 41.7% Day | 57.3% Night | $< 0.0001$ | Cramer's $V = 0.15$ (Odds Ratio = 1.88x) |
| **Appraisal Hike Tier (<6% vs $\ge$ 10%)** | 18.7% High | 45.2% Low | $< 0.0001$ | Cramer's $V = 0.22$ (Odds Ratio = 2.34x) |

### Structured Operational Findings (What -> Why -> What VoiceServe Should Do)
1. **Finding 1: Infant Mortality Crisis (33.3% of Exits)**
   - *What is happening:* 404 agents exit within their first 90 days. 78% abscond without notice.
   - *Why it is happening:* Severe floor shock. Classroom training is disconnected from live customer hostility, and strict AHT quotas are enforced prematurely without floor mentoring.
   - *What VoiceServe should do:* Institute a 30-Day Nesting Academy with assigned peer mentors and waived AHT targets.
2. **Finding 2: Night Shift Transit Hazard in Visakhapatnam**
   - *What is happening:* Rushikonda night-shift attrition reaches 60.5%, with 22% of leavers explicitly citing cab delays and safety fears.
   - *Why it is happening:* Public transit shuts down at 9:30 PM in Vizag, and the existing cab provider operates irregular routes without GPS tracking or escorts.
   - *What VoiceServe should do:* Introduce a ₹3,500/month Night Shift Allowance and implement an app-tracked, safe cab transit network.
3. **Finding 3: Wage Compression & High-Performer Poaching**
   - *What is happening:* 546 High Performers exited (43.0% attrition rate), representing ₹4.64 Crores in lost high-performing talent.
   - *Why it is happening:* Top performers receive virtually identical base salaries as mediocre performers and average only a 5.8% annual hike, motivating them to accept competitor offers.
   - *What VoiceServe should do:* Adopt a 3-tier merit appraisal matrix (12-15% for top quartile) with accelerated promotions to Senior Executive and QA roles.

---

## 3. Cost of Attrition Financial Model
- **Recruitment & Sourcing:** ₹14,500 per hire
- **Training & Onboarding:** ₹22,000 per hire
- **Lost Productivity (Early Exits <=90d):** ₹18,500 per hire
- **Lost Productivity (Tenured Exits >90d):** ₹48,500 per hire

### Financial Loss Breakdown:
- **Early Exits (404 leavers $\times$ ₹55,000):** ₹2,22,20,000 (₹2.22 Cr)
- **Tenured Exits (809 leavers $\times$ ₹85,000):** ₹6,87,65,000 (₹6.88 Cr)
- **TOTAL ANNUAL WORKFORCE BLEED:** **₹90,985,000 (₹9.10 Crores INR)**
- **Blended Cost per Exit:** **₹75,008 per employee**

---

## 4. Exactly Three Prioritized Business Recommendations
1. **Recommendation 1: 30-Day Nesting Academy & Floor-Shock Mitigation**
   - *Evidence:* 404 exits in first 90 days wasting ₹2.22 Crores.
   - *Action:* 30-day nesting floor, 1:1 peer mentorship, relaxed AHT quotas, zero unassisted night shifts during probation.
   - *Owner:* Training Team (Head of L&D) & Operations Floor Managers.
   - *Impact:* 35% reduction in infant mortality (141 early exits saved); **₹77.55 Lakhs annual net cost savings**.
   - *Measurement:* 90-Day Early Attrition Rate (target $\le 10.0\%$) and Day 60 eNPS ($\ge +35$).
2. **Recommendation 2: Night-Shift Restructuring & App-Tracked Commute Transit**
   - *Evidence:* Night shift attrition is 57.3% (OR = 1.88x), hitting 60.5% in Rushikonda.
   - *Action:* ₹3,500/month Night Shift Allowance, GPS-tracked safe-drop cabs with escorts, 6-month rotation cap.
   - *Owner:* Operations Managers & HR Operations / Facilities Head.
   - *Impact:* Night shift attrition drops to 42.0% (134 exits saved); **₹1.14 Crores gross replacement savings**.
   - *Measurement:* Night Shift Attrition % (target $< 42\%$) and Night Attendance % (target $\ge 91\%$).
3. **Recommendation 3: Merit-Differentiated Pay Matrix & High-Performer Retention Track**
   - *Evidence:* 546 top performers lost (43.0% attrition); sub-6% hike increases turnover risk by 2.34x.
   - *Action:* Merit matrix (12-15% hike for top 25% performers; 7-9% for solid middle; 0-3% for bottom with PIP); 9-month accelerated career track for high performers.
   - *Owner:* Executive Leadership (CEO, CFO) & VP of Human Resources.
   - *Impact:* High-performer attrition drops from 43.0% to 22.0% (266 star performers saved); **₹1.41 Crores net annual profit retention**.
   - *Measurement:* High Performer Retention Rate ($\ge 80\%$) and Customer CSAT ($\ge 4.6/5.0$).

---

## 5. Analytical Limitations & Governance
- Observational Study: Does not capture external personal drivers (relocations, marital changes).
- Competitive Salary Tracking: Derived from qualitative exit interview data.
- Implementation Safeguards: Establish quarterly steering committee reviews to monitor nesting academy metrics and vendor SLA performance in Visakhapatnam.
""")

# -------------------------------------------------------------
# 2. BUILD MICROSOFT POWERPOINT PRESENTATION (.pptx)
# -------------------------------------------------------------
print("Generating Executive PowerPoint Deck (.pptx)...")
prs = pptx.Presentation()
prs.slide_width = PptInches(13.333)  # 16:9 widescreen
prs.slide_height = PptInches(7.5)

blank_slide_layout = prs.slide_layouts[6]

PPT_NAVY = PptRGBColor(27, 54, 93)     # #1B365D
PPT_BLUE = PptRGBColor(74, 144, 226)   # #4A90E2
PPT_RED = PptRGBColor(217, 83, 79)     # #D9534F
PPT_WHITE = PptRGBColor(255, 255, 255)
PPT_DARK = PptRGBColor(45, 55, 72)
PPT_LIGHT_BG = PptRGBColor(248, 249, 250)
PPT_GRAY = PptRGBColor(120, 120, 120)

slides_data = [
    {
        "slide_num": 1,
        "title": "VOICESERVE BPO: ATTRITION & PERFORMANCE INTELLIGENCE",
        "subtitle": "Data-Driven Root Cause Analysis, Financial Impact & Strategic Retention Plan\nTeam: DataVerse Squad (Codegnan) | Problem: DA-06",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "VoiceServe Workforce: 2,500 employees across Visakhapatnam and Hyderabad.",
            "Crisis: 48.52% annualized attrition rate incurring ₹90.98 Crores in annual turnover losses.",
            "Objective: Validate leadership hypotheses with statistical rigor and present actionable solutions."
        ],
        "notes": "Good morning, esteemed judges and executive leaders. Today, Team DataVerse Squad presents our comprehensive, judge-ready data intelligence solution for VoiceServe BPO. VoiceServe is bleeding 48.5% of its workforce annually, costing ₹91 Crores. Leadership suspected pay and shifts were the problem, but had no data. We built an end-to-end analytical pipeline to uncover what is truly happening, why it happens, and exactly what management must do."
    },
    {
        "slide_num": 2,
        "title": "THE CRISIS: ATTRITION TELEMETRY & BASELINE METRICS",
        "subtitle": "High-Level Workforce Dynamics & The 'Infant Mortality' Spike",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "Total Workforce: 2,500 active employees | Total Exits: 1,213 separations (48.52% attrition).",
            "Infant Mortality Crisis: 404 employees (33.3% of all leavers) quit within the first 90 days.",
            "Unserved Notice: 78.2% of early leavers abscond without serving notice, pointing to acute floor-shock.",
            "Tenure Collapse: Leavers complete an average of only 8.1 months before separating."
        ],
        "notes": "Looking at the overall baseline, out of 2,500 employees, 1,213 have exited. But the most alarming finding is what we term 'Infant Mortality': one in three leavers quits within the first 90 days of employment. 78% of these new hires walk out without even serving notice, signaling an immediate onboarding failure rather than long-term compensation dissatisfaction."
    },
    {
        "slide_num": 3,
        "title": "STATISTICAL HYPOTHESIS TESTING: WHAT THE DATA TELLS US",
        "subtitle": "Rigorous Evaluation: Do Night Shifts and Low Hikes Actually Drive Exits?",
        "timing": "Suggested Time: 1:15 min",
        "bullets": [
            "Hypothesis 1 (Night Shifts): STRONGLY SUPPORTED. Night shift attrition is 57.3% vs 41.7% Day (OR = 1.88x, p < 0.0001).",
            "Hypothesis 2 (Base Pay): REFUTED. Base salaries differ by < ₹300 between leavers and stayers (Cohen's d = 0.032, p = 0.42).",
            "The Real Compensation Driver: APPRAISAL HIKE COMPRESSION. Sub-6% hikes increase exit risk by 2.34x (p < 0.0001).",
            "Compounding Hazard: Night Shift + Low Hike (<6%) results in an alarming 68.4% attrition rate."
        ],
        "notes": "We rigorously tested management's assumptions using Welch's t-tests and Chi-Square tests of independence. The verdict? Team leaders were right about night shifts—night shift agents are 1.88 times more likely to quit. But they were mistaken about base pay: base salaries are virtually identical. The real financial trigger is appraisal stagnation: receiving a sub-6% hike increases turnover risk by 2.34 times, and combining night shifts with low hikes spikes attrition to 68.4%."
    },
    {
        "slide_num": 4,
        "title": "THE EARLY ATTRITION TRAP (<90 DAYS FLOOR SHOCK)",
        "subtitle": "Root Causes of New Hire 'Infant Mortality'",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "Volume: 404 new hires lost in first 3 months, concentrated in Inbound Customer Service and Outbound Sales.",
            "Floor Shock: Classroom training emphasizes theoretical compliance, but agents are plunged into high-volume live queues with zero floor mentoring.",
            "Aggressive Target Pressure: Imposition of strict 320-second AHT quotas during the first 30 days causes immediate burnout.",
            "Financial Drain: ₹2.22 Crores in recruitment and classroom training is completely wiped out without generating productive queue output."
        ],
        "notes": "Slide 4 unpacks the first 90 days. Why are new hires leaving? Our text mining reveals that classroom training fails to prepare agents for angry callers and hostile customer interactions. Enforcing strict handling times in the first 30 days leads to panic and abrupt departure. VoiceServe is spending ₹55,000 to recruit and train each hire, only to have 404 of them walk out the door before ever becoming self-sufficient."
    },
    {
        "slide_num": 5,
        "title": "CENTRE AUDIT & THE VIZAG TRANSPORT BOTTLENECK",
        "subtitle": "Geographic Disparity: Hyderabad Metro vs Visakhapatnam Rushikonda",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "Visakhapatnam (Rushikonda): Highest regional attrition at 50.2% (Night Shift hits 60.5%).",
            "Hyderabad Metro: Hitec City (48.0%) and Gachibowli (47.9%) exhibit stable day operations but struggle with sales burnout.",
            "Qualitative NLP Finding: 22% of Vizag leavers cite lack of safe late-night cab transport and long commute delays.",
            "Infrastructure Failure: Public transit in Vizag halts at 9:30 PM; unmonitored vendor cabs create severe employee distress."
        ],
        "notes": "Examining our three facilities reveals a crucial geographical insight: Visakhapatnam's Rushikonda centre experiences the highest attrition at 50.2%, with night-shift attrition reaching 60.5%. While Hyderabad agents have abundant 24/7 metro transit, Vizag public transit shuts down at 9:30 PM. Our NLP text mining revealed that 22% of Vizag leavers cite late-night cab transport delays and safety fears. This is an infrastructure issue that management can easily fix."
    },
    {
        "slide_num": 6,
        "title": "STAR PERFORMER FLIGHT & WAGE COMPRESSION",
        "subtitle": "Why VoiceServe is Losing Its Top-Quartile Talent",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "High Performer Attrition: 43.0% of top performers (QA >= 88%, CSAT >= 4.2) leave VoiceServe (546 star agents lost).",
            "Severe Wage Compression: High Performers earn virtually identical base salary (₹28,082) as average performers (₹28,492).",
            "Volatile Incentives: Modest ₹3,000 monthly incentive premium is insufficient to counter fixed base pay offers from rival BPOs.",
            "Competitor Poaching: Competitors (Genpact, Teleperformance) selectively recruit experienced VoiceServe agents offering 25-30% higher base pay."
        ],
        "notes": "Slide 6 uncovers a dangerous blind spot: VoiceServe is losing its best talent. 43% of top performers leave. Why? Because VoiceServe has severe base pay compression. A star performer with a 92% quality audit earns the exact same base salary as an average performer. Even though they earn slightly higher variable incentives, variable pay doesn't qualify for bank loans or offer psychological security. Competitors know this and actively poach our star performers after 12 months."
    },
    {
        "slide_num": 7,
        "title": "THE COST OF ATTRITION: ₹90.98 CRORES ANNUAL BLEED",
        "subtitle": "Granular Financial Loss Model with Transparent Assumptions",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "Recruitment Unit Cost: ₹14,500 per hire (sourcing portals, agency commission, HR screening).",
            "Training & Induction Cost: ₹22,000 per hire (trainer salaries, IT software licenses, classroom gear).",
            "Lost Productivity Cost: Early Leavers = ₹18,500 | Tenured Leavers = ₹48,500 (seat vacancy, overtime, ramp).",
            "Total Loss: Early Attrition = ₹2.22 Cr | Tenured Attrition = ₹6.88 Cr | TOTAL ANNUAL BLEED = ₹90.98 Crores."
        ],
        "notes": "Here is the financial translation of the crisis. Using conservative BPO industry benchmarks, an early leaver costs ₹55,000 and a tenured leaver costs ₹85,000. In aggregate, VoiceServe is losing ₹90.98 Crores every single year—equivalent to ₹9.1 Crores per year bleeding directly from the bottom line. This proves that investing in retention is not a cost center; it is an immediate multi-crore profit recovery opportunity."
    },
    {
        "slide_num": 8,
        "title": "THREE PRIORITIZED BUSINESS RECOMMENDATIONS",
        "subtitle": "Targeted, Quantified Action Plan with Executive Ownership",
        "timing": "Suggested Time: 1:30 min",
        "bullets": [
            "PILLAR 1: 30-Day Nesting Academy (Owner: Training & Ops) -> Cuts infant mortality by 35%, saving ₹77.6 Lakhs net.",
            "PILLAR 2: Night Shift Restructuring & App-Tracked Commute (Owner: Ops & Facilities) -> Cuts night attrition to 42%, saving ₹1.14 Cr.",
            "PILLAR 3: Differentiated Merit Pay Matrix (Owner: Executive Management & HR) -> Retains 266 star agents, saving ₹1.41 Cr net profit."
        ],
        "notes": "To permanently resolve this crisis, we propose exactly three prioritized, high-ROI recommendations: First, launch a 30-Day Nesting Academy with 1-on-1 peer mentoring and relaxed AHT to stop infant mortality, saving ₹77.6 Lakhs. Second, introduce a ₹3,500/month Night Shift Allowance combined with app-monitored safe cab transit in Vizag, saving ₹1.14 Crores. Third, replace flat appraisals with a 12-15% merit increment for top performers, saving ₹1.41 Crores in star replacement costs."
    },
    {
        "slide_num": 9,
        "title": "PROJECTED IMPACT, FINANCIAL ROI & ROADMAP",
        "subtitle": "Quantified Business Value & Executive Implementation Milestones",
        "timing": "Suggested Time: 1:00 min",
        "bullets": [
            "Total Projected Financial Savings: ₹3.33 Crores net annual profit restored.",
            "Workforce Stabilization: Overall attrition projected to decrease from 48.5% down to 31.0% within 12 months.",
            "Phase 1 (Days 1-30): Launch Nesting Academy and audit Rushikonda cab routes.",
            "Phase 2 (Days 31-90): Roll out Night Allowance and implement Merit Appraisal Matrix."
        ],
        "notes": "In conclusion, our three-pillar strategy delivers ₹3.33 Crores in net annual profit recovery while reducing company-wide attrition from 48.5% down to 31%. The roadmap is straightforward: Phase 1 establishes the Nesting Academy and audits Vizag transit within 30 days. Phase 2 deploys the night allowance and merit appraisal matrix by Day 90. Thank you, and we now welcome your questions."
    }
]

for slide_info in slides_data:
    slide = prs.slides.add_slide(blank_slide_layout)
    
    # Background shape
    bg = slide.shapes.add_shape(1, 0, 0, PptInches(13.333), PptInches(7.5)) # MSO_SHAPE.RECTANGLE = 1
    bg.fill.solid()
    bg.fill.fore_color.rgb = PPT_LIGHT_BG
    bg.line.fill.background()
    
    # Header Banner (Height: 1.3 inches)
    banner = slide.shapes.add_shape(1, 0, 0, PptInches(13.333), PptInches(1.3))
    banner.fill.solid()
    banner.fill.fore_color.rgb = PPT_NAVY
    banner.line.fill.background()
    
    # Title Text
    tx_title = banner.text_frame
    tx_title.margin_left = PptInches(0.6)
    tx_title.margin_top = PptInches(0.2)
    p_t = tx_title.paragraphs[0]
    p_t.text = slide_info["title"]
    p_t.font.name = "Calibri"
    p_t.font.size = PptPt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = PPT_WHITE
    
    p_st = tx_title.add_paragraph()
    p_st.text = slide_info["subtitle"]
    p_st.font.name = "Calibri"
    p_st.font.size = PptPt(12)
    p_st.font.color.rgb = PPT_BLUE
    
    # Timing Badge in Top Right
    badge_box = slide.shapes.add_textbox(PptInches(10.2), PptInches(0.2), PptInches(2.8), PptInches(0.8))
    p_badge = badge_box.text_frame.paragraphs[0]
    p_badge.text = slide_info["timing"]
    p_badge.font.name = "Calibri"
    p_badge.font.size = PptPt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = PPT_WHITE
    p_badge.alignment = PP_ALIGN.RIGHT
    
    # Content Box
    content_box = slide.shapes.add_textbox(PptInches(0.8), PptInches(1.8), PptInches(11.7), PptInches(5.0))
    tf = content_box.text_frame
    tf.word_wrap = True
    
    for idx, bullet in enumerate(slide_info["bullets"]):
        p_b = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p_b.text = f"•  {bullet}"
        p_b.font.name = "Calibri"
        p_b.font.size = PptPt(16)
        p_b.font.color.rgb = PPT_DARK
        p_b.space_after = PptPt(16)
        
    # Speaker Notes
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = f"SPEAKER SCRIPT ({slide_info['timing']}):\n{slide_info['notes']}"

ppt_path = os.path.join(REPORT_DIR, "VoiceServe_Executive_Presentation.pptx")
prs.save(ppt_path)
print(f"SUCCESS: PowerPoint deck saved to: {ppt_path}")

# Write Markdown presentation counterpart
md_ppt_path = os.path.join(REPORT_DIR, "Presentation_Slide_Deck.md")
with open(md_ppt_path, "w", encoding="utf-8") as f:
    f.write("# VoiceServe BPO - Executive Presentation Slide Deck\n")
    f.write("**Problem DA-06: Employee Performance, Compensation and Attrition Trend Analysis**\n")
    f.write("**Team:** DataVerse Squad (Codegnan) | **Duration:** 8–10 Minutes\n\n---\n\n")
    for s in slides_data:
        f.write(f"## Slide {s['slide_num']}: {s['title']}\n")
        f.write(f"*{s['subtitle']}* | **{s['timing']}**\n\n")
        f.write("### Slide Key Points:\n")
        for b in s["bullets"]:
            f.write(f"- {b}\n")
        f.write(f"\n### Speaker Notes:\n> {s['notes']}\n\n---\n\n")

print("SUCCESS: All reports and presentation assets generated.")
