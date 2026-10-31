"""
================================================================================
VOICESERVE BPO - SYNTHETIC DATASET GENERATOR
DA-06: Employee Performance, Compensation & Attrition Trend Analysis
Team: DataVerse Squad, Codegnan
================================================================================
Generates 2,500 employee records with realistic BPO dynamics:
- Centers: Visakhapatnam (Rushikonda), Hyderabad (Hitec City), Hyderabad (Gachibowli)
- Annual Attrition ~42%
- Infant mortality (early attrition within 90 days) ~28% of leavers
- Night shift & low-hike attrition spikes
- High performer wage compression
- Free-text exit reasons
- Intentional real-world messiness: casing inconsistencies, duplicates, nulls,
  bad dates, and outlier entries.
================================================================================
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

# Set reproducible seeds
np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(DATA_RAW_DIR, exist_ok=True)

NUM_EMPLOYEES = 2500

# Reference Date Anchor for the study period: 2026-10-31
STUDY_END_DATE = datetime.date(2026, 10, 31)
STUDY_START_DATE = datetime.date(2025, 1, 1)

CENTRES = ["Hyderabad (Hitec City)", "Hyderabad (Gachibowli)", "Visakhapatnam (Rushikonda)"]
CENTRE_WEIGHTS = [0.45, 0.30, 0.25]

PROCESSES = [
    "Inbound Customer Service",
    "Outbound Sales",
    "Technical Support",
    "Chat & Email Support",
    "Claims & Back Office"
]
PROCESS_WEIGHTS = [0.35, 0.20, 0.15, 0.15, 0.15]

ROLES = [
    "Customer Support Executive",
    "Senior Customer Support Executive",
    "Technical Support Specialist",
    "Quality Analyst",
    "Team Leader"
]
ROLE_WEIGHTS = [0.65, 0.15, 0.10, 0.05, 0.05]

SHIFTS = ["Day", "Night", "Rotational"]
SHIFT_WEIGHTS = [0.45, 0.35, 0.20]

AGE_GROUPS = ["<21", "21-25", "26-30", "31-35", ">35"]
AGE_WEIGHTS = [0.12, 0.48, 0.25, 0.10, 0.05]

# Base Salary distributions by role (INR per month)
BASE_SALARY_CONFIG = {
    "Customer Support Executive": (20000, 27000),
    "Senior Customer Support Executive": (28000, 38000),
    "Technical Support Specialist": (30000, 42000),
    "Quality Analyst": (32000, 45000),
    "Team Leader": (42000, 60000)
}

# Rich pool of realistic exit reasons
EXIT_REASONS = [
    "Better compensation offer from competitor (Genpact / Teleperformance)",
    "Severe sleep disruption and chronic fatigue from persistent night shifts",
    "Lack of reliable late-night cab transport and safety concerns in Rushikonda",
    "Dissatisfied with annual appraisal - received meager 3% hike after exceeding targets",
    "Relocation to hometown due to family commitments and parents' health",
    "Pursuing higher education (full-time MBA / MS entrance preparations)",
    "Unreasonable AHT targets, relentless call volume, and toxic floor pressure",
    "Hostile micromanagement and punitive QA score deductions from Team Leader",
    "Stagnant career growth; passed over for Team Leader internal promotion",
    "Lack of proper onboarding training and thrown directly onto live voice queue",
    "Health complications (severe throat strain, back pain, migraine from headset)",
    "Shift rotation schedule changes communicated with less than 24 hours notice",
    "Higher base pay offer in non-voice chat process closer to residence",
    "Incentive scheme constantly modified, making monthly targets impossible to hit",
    "Personal reasons / Marriage",
    "Found an IT software job after completing technical certification",
    "Burnout from back-to-back angry customer escalations without de-escalation support"
]

print("Generating synthetic VoiceServe employee dataset...")

# -------------------------------------------------------------
# 1. GENERATE EMPLOYEES
# -------------------------------------------------------------
employees = []
pay_records = []
engagement_records = []
exit_records = []
performance_records = []

# Generate joining dates spanning 2023-01-01 to 2026-08-31
min_join_ordinal = datetime.date(2023, 1, 1).toordinal()
max_join_ordinal = datetime.date(2026, 8, 31).toordinal()

for i in range(1, NUM_EMPLOYEES + 1):
    emp_id = f"VS{i:05d}"
    
    centre = np.random.choice(CENTRES, p=CENTRE_WEIGHTS)
    process = np.random.choice(PROCESSES, p=PROCESS_WEIGHTS)
    role = np.random.choice(ROLES, p=ROLE_WEIGHTS)
    shift = np.random.choice(SHIFTS, p=SHIFT_WEIGHTS)
    age_group = np.random.choice(AGE_GROUPS, p=AGE_WEIGHTS)
    
    # Skew join dates so we have healthy mix of tenures
    join_ordinal = int(np.random.triangular(min_join_ordinal, max_join_ordinal - 180, max_join_ordinal))
    join_date = datetime.date.fromordinal(join_ordinal)
    
    # Salary calculation based on role
    sal_min, sal_max = BASE_SALARY_CONFIG[role]
    monthly_salary = int(np.random.uniform(sal_min, sal_max))
    # Round to nearest 500
    monthly_salary = int(round(monthly_salary / 500.0) * 500)
    
    # Performance profile (latent capability of employee: 0.0 to 1.0)
    perf_factor = np.random.beta(5, 2)  # slightly skewed towards competent
    
    # Last hike determination
    tenure_days_to_end = (STUDY_END_DATE - join_date).days
    if tenure_days_to_end < 180:
        last_hike_percent = 0.0
        last_hike_date = None
    else:
        # Determine hike percentage based on performance and market budget
        # VoiceServe management kept budget low: 40% get < 6% hike
        if np.random.rand() < 0.40:
            last_hike_percent = round(float(np.random.uniform(1.0, 5.5)), 1)
        elif np.random.rand() < 0.75:
            last_hike_percent = round(float(np.random.uniform(6.0, 9.5)), 1)
        else:
            last_hike_percent = round(float(np.random.uniform(10.0, 18.0)), 1)
        
        # Hike date in last 12-18 months
        hike_offset = random.randint(30, min(365, max(31, tenure_days_to_end - 90)))
        last_hike_date = STUDY_END_DATE - datetime.timedelta(days=hike_offset)

    # Average monthly incentive
    if perf_factor > 0.7:
        incentive_amount = int(round(np.random.uniform(3500, 10000) / 100) * 100)
    elif perf_factor > 0.4:
        incentive_amount = int(round(np.random.uniform(1000, 3500) / 100) * 100)
    else:
        incentive_amount = int(round(np.random.uniform(0, 1000) / 100) * 100)

    # Engagement data
    training_hours = int(np.random.normal(25, 10))
    training_hours = max(4, min(65, training_hours))
    
    survey_score = round(float(np.random.normal(3.4, 0.9)), 1)
    survey_score = max(1.0, min(5.0, survey_score))
    
    promotions = 0
    if tenure_days_to_end > 500 and perf_factor > 0.75:
        promotions = np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])
    
    # -------------------------------------------------------------
    # DETERMINING ATTRITION PROBABILITY
    # -------------------------------------------------------------
    # Realistic BPO hazard drivers:
    # 1. Base rate ~ 0.32
    # 2. Night shift: +0.15
    # 3. Low hike (<6%): +0.18
    # 4. Outbound Sales: +0.12 (high burnout)
    # 5. Low survey score (<3.0): +0.14
    # 6. Infant mortality: early exit hazard in first 90 days is very prominent
    
    attr_prob = 0.28
    if shift == "Night":
        attr_prob += 0.16
    elif shift == "Rotational":
        attr_prob += 0.08
        
    if last_hike_percent > 0 and last_hike_percent < 6.0:
        attr_prob += 0.17
    elif last_hike_percent >= 12.0:
        attr_prob -= 0.14
        
    if process == "Outbound Sales":
        attr_prob += 0.12
    elif process == "Claims & Back Office":
        attr_prob -= 0.08
        
    if centre == "Visakhapatnam (Rushikonda)" and shift == "Night":
        attr_prob += 0.09  # transport & localized cab issue
        
    if survey_score < 2.5:
        attr_prob += 0.15
    elif survey_score >= 4.2:
        attr_prob -= 0.12
        
    # Infant mortality factor: new hires experiencing floor shock
    is_early_candidate = (np.random.rand() < 0.26)
    if is_early_candidate:
        attr_prob += 0.22

    attr_prob = max(0.08, min(0.85, attr_prob))
    
    has_exited = (np.random.rand() < attr_prob)
    
    exit_date = None
    exit_reason = None
    notice_served = None
    
    if has_exited:
        # Determine exit date
        # Check if infant mortality leaver (<90 days)
        if is_early_candidate and np.random.rand() < 0.65:
            early_tenure_days = random.randint(18, 88)
            proposed_exit = join_date + datetime.timedelta(days=early_tenure_days)
            if proposed_exit <= STUDY_END_DATE:
                exit_date = proposed_exit
        
        if exit_date is None:
            # Regular leaver: leaves between join_date + 90 days and STUDY_END_DATE
            min_exit_ord = join_date.toordinal() + 30
            max_exit_ord = STUDY_END_DATE.toordinal()
            if min_exit_ord < max_exit_ord:
                exit_date = datetime.date.fromordinal(random.randint(min_exit_ord, max_exit_ord))
            else:
                exit_date = STUDY_END_DATE
                
        # Assign exit reason correlated with attributes
        if (exit_date - join_date).days <= 90:
            early_reasons = [
                "Lack of proper onboarding training and thrown directly onto live voice queue",
                "Severe sleep disruption and chronic fatigue from persistent night shifts",
                "Unreasonable AHT targets, relentless call volume, and toxic floor pressure",
                "Hostile micromanagement and punitive QA score deductions from Team Leader",
                "Better compensation offer from competitor (Genpact / Teleperformance)"
            ]
            exit_reason = random.choice(early_reasons)
            notice_served = np.random.choice(["No", "Yes"], p=[0.72, 0.28]) # Most early exits abscond/no notice
        elif shift == "Night" and random.random() < 0.45:
            if centre == "Visakhapatnam (Rushikonda)" and random.random() < 0.5:
                exit_reason = "Lack of reliable late-night cab transport and safety concerns in Rushikonda"
            else:
                exit_reason = "Severe sleep disruption and chronic fatigue from persistent night shifts"
            notice_served = np.random.choice(["Yes", "No"], p=[0.55, 0.45])
        elif last_hike_percent > 0 and last_hike_percent < 6.0 and random.random() < 0.50:
            exit_reason = "Dissatisfied with annual appraisal - received meager 3% hike after exceeding targets"
            notice_served = np.random.choice(["Yes", "No"], p=[0.65, 0.35])
        elif perf_factor > 0.75 and random.random() < 0.45:
            exit_reason = "Better compensation offer from competitor (Genpact / Teleperformance)"
            notice_served = "Yes"
        else:
            exit_reason = random.choice(EXIT_REASONS)
            notice_served = np.random.choice(["Yes", "No"], p=[0.60, 0.40])
            
    # Record data
    employees.append({
        "employee_id": emp_id,
        "join_date": join_date.strftime("%Y-%m-%d"),
        "centre": centre,
        "process": process,
        "role": role,
        "shift": shift,
        "age_group": age_group
    })
    
    pay_records.append({
        "employee_id": emp_id,
        "monthly_salary": monthly_salary,
        "incentive_amount": incentive_amount,
        "last_hike_percent": last_hike_percent,
        "last_hike_date": last_hike_date.strftime("%Y-%m-%d") if last_hike_date else None
    })
    
    engagement_records.append({
        "employee_id": emp_id,
        "survey_score": survey_score,
        "training_hours": training_hours,
        "promotions_count": promotions
    })
    
    exit_records.append({
        "employee_id": emp_id,
        "exit_date": exit_date.strftime("%Y-%m-%d") if exit_date else None,
        "exit_reason": exit_reason,
        "notice_served": notice_served
    })
    
    # -------------------------------------------------------------
    # 2. MONTHLY PERFORMANCE RECORDS (2025-01 to 2026-10)
    # -------------------------------------------------------------
    # Generate monthly performance records for months employee was active
    start_eval = max(join_date, datetime.date(2025, 1, 1))
    end_eval = exit_date if exit_date else STUDY_END_DATE
    
    # Monthly iteration
    cur_year = start_eval.year
    cur_month = start_eval.month
    
    while True:
        m_start = datetime.date(cur_year, cur_month, 1)
        if m_start > end_eval:
            break
            
        m_str = f"{cur_year}-{cur_month:02d}"
        
        # Monthly performance parameters
        # Calls handled varies by process
        base_calls = 1100 if "Support" in process or "Service" in process else 850
        calls_handled = int(np.random.normal(base_calls * (0.8 + 0.4 * perf_factor), 120))
        calls_handled = max(350, min(2100, calls_handled))
        
        # Quality score (0 to 100%)
        qs = np.random.normal(75 + 20 * perf_factor, 6.5)
        qs = round(float(max(55.0, min(99.5, qs))), 1)
        
        # Customer rating (1 to 5)
        cr = np.random.normal(3.2 + 1.5 * perf_factor, 0.35)
        cr = round(float(max(1.8, min(5.0, cr))), 2)
        
        # Attendance percent (70 to 100%)
        # Disengaged or soon-to-leave employees show attendance dip
        att_base = 94.0 if not has_exited else 89.0
        if exit_date and (exit_date - m_start).days < 60:
            att_base -= 8.0 # noticeable attendance drop prior to exit
            
        att = np.random.normal(att_base, 4.5)
        att = round(float(max(60.0, min(100.0, att))), 1)
        
        performance_records.append({
            "employee_id": emp_id,
            "month": m_str,
            "calls_handled": calls_handled,
            "quality_score": qs,
            "customer_rating": cr,
            "attendance_percent": att
        })
        
        # Next month
        if cur_month == 12:
            cur_year += 1
            cur_month = 1
        else:
            cur_month += 1

# Convert to DataFrames
df_emp = pd.DataFrame(employees)
df_pay = pd.DataFrame(pay_records)
df_eng = pd.DataFrame(engagement_records)
df_exit = pd.DataFrame(exit_records)
df_perf = pd.DataFrame(performance_records)

print(f"Base data created: {len(df_emp)} employees, {len(df_perf)} performance records.")
print(f"Raw exits count: {df_exit['exit_date'].notna().sum()} ({(df_exit['exit_date'].notna().sum()/len(df_emp))*100:.1f}%)")

# -------------------------------------------------------------
# 3. INTRODUCE INTENTIONAL REAL-WORLD MESSINESS
# -------------------------------------------------------------
print("Injecting intentional real-world messiness (nulls, duplicates, casing, bad dates, outliers)...")

# A. Inconsistent casing in categorical columns
casing_variants_shift = {"Day": ["Day", "day", "DAY", " Day"], "Night": ["Night", "night", "NIGHT"], "Rotational": ["Rotational", "rotational", "ROTATIONAL"]}
for shift_val, variants in casing_variants_shift.items():
    mask = df_emp["shift"] == shift_val
    sub_indices = df_emp[mask].index
    chosen = np.random.choice(sub_indices, size=int(len(sub_indices) * 0.25), replace=False)
    for idx in chosen:
        df_emp.at[idx, "shift"] = random.choice(variants)

casing_variants_centre = {
    "Hyderabad (Hitec City)": ["Hyderabad (Hitec City)", "hyderabad (hitec city)", "HYD - HITEC", "Hyderabad (Hitec City) "],
    "Visakhapatnam (Rushikonda)": ["Visakhapatnam (Rushikonda)", "visakhapatnam (rushikonda)", "VIZAG (Rushikonda)", "Visakhapatnam (Rushikonda)"]
}
for c_val, variants in casing_variants_centre.items():
    mask = df_emp["centre"] == c_val
    sub_indices = df_emp[mask].index
    chosen = np.random.choice(sub_indices, size=int(len(sub_indices) * 0.15), replace=False)
    for idx in chosen:
        df_emp.at[idx, "centre"] = random.choice(variants)

# B. Inconsistent date formats in employees join_date
for idx in np.random.choice(df_emp.index, size=150, replace=False):
    orig = df_emp.at[idx, "join_date"]
    dt = datetime.datetime.strptime(orig, "%Y-%m-%d")
    fmt = random.choice(["%d/%m/%Y", "%m-%d-%Y", "%Y/%m/%d"])
    df_emp.at[idx, "join_date"] = dt.strftime(fmt)

# C. Missing values (nulls)
# Missing survey scores (10% didn't fill survey)
null_survey_idx = np.random.choice(df_eng.index, size=int(len(df_eng) * 0.10), replace=False)
df_eng.loc[null_survey_idx, "survey_score"] = np.nan

# Missing incentives (8% recorded as NaN instead of 0)
null_inc_idx = np.random.choice(df_pay.index, size=int(len(df_pay) * 0.08), replace=False)
df_pay.loc[null_inc_idx, "incentive_amount"] = np.nan

# Missing quality score in performance (some un-audited months ~3%)
null_qs_idx = np.random.choice(df_perf.index, size=int(len(df_perf) * 0.03), replace=False)
df_perf.loc[null_qs_idx, "quality_score"] = np.nan

# D. Outliers / Typos
# Monthly salary typo (extra zero or negative)
typo_sal_1 = np.random.choice(df_pay.index, size=3, replace=False)
for idx in typo_sal_1:
    df_pay.at[idx, "monthly_salary"] = df_pay.at[idx, "monthly_salary"] * 10 # e.g. 250000

typo_sal_2 = np.random.choice(df_pay.index, size=2, replace=False)
for idx in typo_sal_2:
    df_pay.at[idx, "monthly_salary"] = -abs(df_pay.at[idx, "monthly_salary"])

# Calls handled outlier (e.g. 9999 or -5)
typo_perf_1 = np.random.choice(df_perf.index, size=5, replace=False)
for idx in typo_perf_1:
    df_perf.at[idx, "calls_handled"] = 9999

typo_perf_2 = np.random.choice(df_perf.index, size=3, replace=False)
for idx in typo_perf_2:
    df_perf.at[idx, "attendance_percent"] = 115.0 # Impossible attendance > 100%

# E. Duplicate rows
dup_emp = df_emp.sample(n=12, random_state=42)
df_emp = pd.concat([df_emp, dup_emp], ignore_index=True)

dup_perf = df_perf.sample(n=35, random_state=42)
df_perf = pd.concat([df_perf, dup_perf], ignore_index=True)

# -------------------------------------------------------------
# 4. SAVE RAW DATASETS
# -------------------------------------------------------------
df_emp.to_csv(os.path.join(DATA_RAW_DIR, "employees.csv"), index=False)
df_pay.to_csv(os.path.join(DATA_RAW_DIR, "pay.csv"), index=False)
df_eng.to_csv(os.path.join(DATA_RAW_DIR, "engagement.csv"), index=False)
df_exit.to_csv(os.path.join(DATA_RAW_DIR, "exit.csv"), index=False)
df_perf.to_csv(os.path.join(DATA_RAW_DIR, "performance.csv"), index=False)

print("\nSUCCESS: Raw synthetic files generated in data/raw/:")
print(f" - employees.csv:   {len(df_emp)} rows")
print(f" - pay.csv:         {len(df_pay)} rows")
print(f" - engagement.csv:  {len(df_eng)} rows")
print(f" - exit.csv:        {len(df_exit)} rows")
print(f" - performance.csv: {len(df_perf)} rows")
