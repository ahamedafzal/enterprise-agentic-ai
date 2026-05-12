import json
import csv
import os
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

OUTPUT_DIR = "data/synthetic"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 1. Employee data (500 rows) ──────────────────────────────────────────────
DEPARTMENTS = ["Engineering", "Finance", "HR", "Operations", "AI Research",
               "Sales", "Legal", "Product", "Marketing", "Procurement"]
KPI_LABELS  = ["Exceeds Expectations", "Meets Expectations",
               "Needs Improvement",   "Critical"]

employees = []
for i in range(1, 501):
    employees.append({
        "employee_id":   f"EMP{i:04d}",
        "name":          fake.name(),
        "department":    random.choice(DEPARTMENTS),
        "role":          fake.job(),
        "email":         fake.company_email(),
        "hire_date":     fake.date_between(start_date="-8y", end_date="-6m").isoformat(),
        "salary_usd":    random.randint(45_000, 180_000),
        "kpi_rating":    random.choice(KPI_LABELS),
        "projects_active": random.randint(1, 6),
        "attrition_risk":  random.choice(["Low", "Medium", "High"]),
        "location":      random.choice(["Dubai", "Abu Dhabi", "Riyadh", "Remote"]),
    })

with open(f"{OUTPUT_DIR}/employee_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=employees[0].keys())
    writer.writeheader()
    writer.writerows(employees)

print(f"✅ employee_data.csv — {len(employees)} rows")

# ── 2. Project reports (50 reports) ─────────────────────────────────────────
STATUSES  = ["On Track", "At Risk", "Delayed", "Completed", "On Hold"]
RISKS     = ["Budget overrun", "Resource shortage", "Technical debt",
             "Scope creep", "Vendor delay", "Regulatory compliance",
             "Integration issues", "Data quality issues"]

projects = []
for i in range(1, 51):
    start = fake.date_between(start_date="-1y", end_date="-3m")
    end   = start + timedelta(days=random.randint(30, 180))
    budget = random.randint(50_000, 2_000_000)
    spent  = int(budget * random.uniform(0.3, 1.2))
    status = random.choice(STATUSES)
    projects.append({
        "project_id":        f"PROJ{i:03d}",
        "name":              f"{fake.bs().title()} Initiative",
        "department":        random.choice(DEPARTMENTS),
        "project_manager":   fake.name(),
        "status":            status,
        "start_date":        start.isoformat(),
        "end_date":          end.isoformat(),
        "budget_usd":        budget,
        "spent_usd":         spent,
        "budget_variance":   round((spent - budget) / budget * 100, 2),
        "completion_pct":    random.randint(10, 100),
        "risks":             random.sample(RISKS, k=random.randint(1, 3)),
        "team_size":         random.randint(3, 20),
        "priority":          random.choice(["Critical", "High", "Medium", "Low"]),
        "description":       fake.paragraph(nb_sentences=4),
        "last_updated":      fake.date_between(start_date="-30d", end_date="today").isoformat(),
    })

with open(f"{OUTPUT_DIR}/project_reports.json", "w", encoding="utf-8") as f:
    json.dump(projects, f, indent=2)

print(f"✅ project_reports.json — {len(projects)} projects")

# ── 3. Vendor contracts (20 contracts as text) ───────────────────────────────
CONTRACT_TYPES = ["Software License", "Consulting Services", "Cloud Infrastructure",
                  "Data Analytics", "AI Model Training", "Security Audit",
                  "Hardware Supply", "Maintenance Agreement"]

contracts = []
for i in range(1, 21):
    start  = fake.date_between(start_date="-2y", end_date="-1m")
    expiry = start + timedelta(days=random.randint(180, 730))
    value  = random.randint(10_000, 500_000)
    contracts.append({
        "contract_id":    f"CON{i:03d}",
        "vendor_name":    fake.company(),
        "contract_type":  random.choice(CONTRACT_TYPES),
        "value_usd":      value,
        "start_date":     start.isoformat(),
        "expiry_date":    expiry.isoformat(),
        "status":         random.choice(["Active", "Expiring Soon", "Expired", "Under Review"]),
        "payment_terms":  random.choice(["Net 30", "Net 60", "Monthly", "Quarterly"]),
        "auto_renew":     random.choice([True, False]),
        "key_obligations": [fake.sentence() for _ in range(3)],
        "penalties":      f"${random.randint(1000, 50000):,} for breach of SLA",
        "contact_person": fake.name(),
        "contact_email":  fake.company_email(),
        "full_text": (
            f"CONTRACT AGREEMENT\n\n"
            f"This agreement is between NEXUS Enterprise and {fake.company()} "
            f"for the provision of {random.choice(CONTRACT_TYPES)} services.\n\n"
            f"OBLIGATIONS:\n"
            + "\n".join([f"- {fake.sentence()}" for _ in range(5)])
            + f"\n\nPAYMENT TERMS: {random.choice(['Net 30','Net 60','Monthly'])}\n"
            f"VALUE: ${value:,}\n"
            f"PENALTY CLAUSE: {fake.sentence()}\n"
            f"GOVERNING LAW: UAE Federal Law\n"
        ),
    })

with open(f"{OUTPUT_DIR}/contracts.json", "w", encoding="utf-8") as f:
    json.dump(contracts, f, indent=2)

print(f"✅ contracts.json — {len(contracts)} contracts")

# ── 4. Financial summary (quarterly) ────────────────────────────────────────
quarters = []
for year in [2023, 2024, 2025]:
    for q in range(1, 5):
        revenue  = random.randint(800_000, 5_000_000)
        expenses = int(revenue * random.uniform(0.55, 0.85))
        quarters.append({
            "period":           f"Q{q} {year}",
            "revenue_usd":      revenue,
            "expenses_usd":     expenses,
            "profit_usd":       revenue - expenses,
            "profit_margin":    round((revenue - expenses) / revenue * 100, 2),
            "headcount":        random.randint(80, 500),
            "new_projects":     random.randint(2, 15),
            "completed_projects": random.randint(1, 10),
            "ai_investment_usd": random.randint(50_000, 800_000),
        })

with open(f"{OUTPUT_DIR}/financial_summary.json", "w", encoding="utf-8") as f:
    json.dump(quarters, f, indent=2)

print(f"✅ financial_summary.json — {len(quarters)} quarters")
print("\n🎉 All synthetic datasets generated in data/synthetic/")