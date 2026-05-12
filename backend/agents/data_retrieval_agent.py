import json
import csv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from backend.agents.base_agent import BaseAgent
from backend.core.config import settings

class DataRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataRetrievalAgent")
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.1,
        )

    def _load_structured_data(self, query: str) -> str:
        context = []

        # Load project stats
        try:
            with open("data/synthetic/project_reports.json", encoding="utf-8") as f:
                projects = json.load(f)
            delayed    = [p for p in projects if p["status"] == "Delayed"]
            at_risk    = [p for p in projects if p["status"] == "At Risk"]
            over_budget = [p for p in projects if p["budget_variance"] > 0]
            context.append(
                f"PROJECT STATS:\n"
                f"- Total projects: {len(projects)}\n"
                f"- Delayed: {len(delayed)}\n"
                f"- At risk: {len(at_risk)}\n"
                f"- Over budget: {len(over_budget)}\n"
                f"Sample delayed projects: "
                + ", ".join([p["name"] for p in delayed[:3]])
            )
        except Exception as e:
            context.append(f"Projects: error loading - {e}")

        # Load employee stats
        try:
            with open("data/synthetic/employee_data.csv", encoding="utf-8") as f:
                employees = list(csv.DictReader(f))
            high_risk = [e for e in employees if e["attrition_risk"] == "High"]
            by_dept   = {}
            for e in employees:
                by_dept[e["department"]] = by_dept.get(e["department"], 0) + 1
            context.append(
                f"EMPLOYEE STATS:\n"
                f"- Total employees: {len(employees)}\n"
                f"- High attrition risk: {len(high_risk)}\n"
                f"- By department: {json.dumps(by_dept)}"
            )
        except Exception as e:
            context.append(f"Employees: error loading - {e}")

        # Load financial stats
        try:
            with open("data/synthetic/financial_summary.json", encoding="utf-8") as f:
                financials = json.load(f)
            latest = financials[-2:]
            context.append(
                "FINANCIAL STATS (latest 2 quarters):\n"
                + "\n".join([
                    f"- {q['period']}: Revenue ${q['revenue_usd']:,}, "
                    f"Profit margin {q['profit_margin']}%"
                    for q in latest
                ])
            )
        except Exception as e:
            context.append(f"Financials: error loading - {e}")

        return "\n\n".join(context)

    @traceable(name="data_retrieval_agent")
    async def run(self, input_data: dict) -> dict:
        task  = input_data.get("task", "")
        query = input_data.get("query", "")
        self.log("Retrieving structured data", task=task)

        structured_data = self._load_structured_data(query)

        messages = [
            SystemMessage(content="""You are an enterprise data analyst.
Analyse the structured data provided and extract key metrics and findings
relevant to the task. Be specific with numbers and percentages."""),
            HumanMessage(content=f"Task: {task}\n\nData:\n{structured_data}"),
        ]

        response = await self.llm.ainvoke(messages)
        self.log("Data retrieval complete")
        return {
            "agent": self.name,
            "status": "completed",
            "output": response.content,
        }