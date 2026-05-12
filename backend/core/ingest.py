import json
import csv
import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.core.config import settings

def get_chroma_client():
    return chromadb.HttpClient(
        host=settings.CHROMA_HOST,
        port=settings.CHROMA_PORT,
        settings=ChromaSettings(anonymized_telemetry=False),
    )

def ingest_projects(client: chromadb.HttpClient):
    collection = client.get_or_create_collection(
        name="project_reports",
        metadata={"hnsw:space": "cosine"},
    )
    with open("data/synthetic/project_reports.json", encoding="utf-8") as f:
        projects = json.load(f)

    docs, ids, metas = [], [], []
    for p in projects:
        text = (
            f"Project: {p['name']}\n"
            f"Status: {p['status']}\n"
            f"Department: {p['department']}\n"
            f"Manager: {p['project_manager']}\n"
            f"Priority: {p['priority']}\n"
            f"Completion: {p['completion_pct']}%\n"
            f"Budget variance: {p['budget_variance']}%\n"
            f"Risks: {', '.join(p['risks'])}\n"
            f"Description: {p['description']}"
        )
        docs.append(text)
        ids.append(p["project_id"])
        metas.append({
            "status":     p["status"],
            "department": p["department"],
            "priority":   p["priority"],
        })

    collection.upsert(documents=docs, ids=ids, metadatas=metas)
    print(f"✅ Ingested {len(docs)} project reports into ChromaDB")

def ingest_contracts(client: chromadb.HttpClient):
    collection = client.get_or_create_collection(
        name="contracts",
        metadata={"hnsw:space": "cosine"},
    )
    with open("data/synthetic/contracts.json", encoding="utf-8") as f:
        contracts = json.load(f)

    docs, ids, metas = [], [], []
    for c in contracts:
        docs.append(c["full_text"])
        ids.append(c["contract_id"])
        metas.append({
            "vendor":  c["vendor_name"],
            "type":    c["contract_type"],
            "status":  c["status"],
            "value":   str(c["value_usd"]),
        })

    collection.upsert(documents=docs, ids=ids, metadatas=metas)
    print(f"✅ Ingested {len(docs)} contracts into ChromaDB")

def ingest_employees(client: chromadb.HttpClient):
    collection = client.get_or_create_collection(
        name="employees",
        metadata={"hnsw:space": "cosine"},
    )
    with open("data/synthetic/employee_data.csv", encoding="utf-8") as f:
        employees = list(csv.DictReader(f))

    docs, ids, metas = [], [], []
    for e in employees:
        text = (
            f"Employee: {e['name']}\n"
            f"Department: {e['department']}\n"
            f"Role: {e['role']}\n"
            f"KPI: {e['kpi_rating']}\n"
            f"Attrition risk: {e['attrition_risk']}\n"
            f"Location: {e['location']}\n"
            f"Active projects: {e['projects_active']}"
        )
        docs.append(text)
        ids.append(e["employee_id"])
        metas.append({
            "department":     e["department"],
            "attrition_risk": e["attrition_risk"],
            "kpi_rating":     e["kpi_rating"],
        })

    collection.upsert(documents=docs, ids=ids, metadatas=metas)
    print(f"✅ Ingested {len(docs)} employees into ChromaDB")

def run_ingestion():
    print("🔄 Connecting to ChromaDB...")
    client = get_chroma_client()
    print("✅ Connected\n")
    ingest_projects(client)
    ingest_contracts(client)
    ingest_employees(client)
    print("\n🎉 All data ingested into ChromaDB successfully!")

if __name__ == "__main__":
    run_ingestion()