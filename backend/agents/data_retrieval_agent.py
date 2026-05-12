import json
import csv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.agents.base_agent import BaseAgent
from backend.agents.tools.web_search import web_search
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
            delayed     = [p for p in projects if p["status"] == "Delayed"]
            at_risk     = [p for p in projects if p["status"] == "At Risk"]
            over_budget = [p for p in projects if p["budget_variance"] > 0]
            context.append(
                f"PROJECT STATS:\n"
                f"- Total projects: {len(projects)}\n"
                f"- Delayed: {len(delayed)}\n"
                f"- At risk: {len(at_risk)}\n"
                f"- Over budget: {len(over_budget)}\n"
                f"Sample delayed: " + ", ".join([p["name"] for p in delayed[:3]])
            )
        except Exception as e:
            context.append(f"Projects: error - {e}")

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
                f"- Total: {len(employees)}\n"
                f"- High attrition risk: {len(high_risk)}\n"
                f"- By department: {json.dumps(by_dept)}"
            )
        except Exception as e:
            context.append(f"Employees: error - {e}")

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
            context.append(f"Financials: error - {e}")

        # Web search for live context
        try:
            search_query = f"UAE enterprise {query} 2025 best practices"
            web_results  = web_search(search_query, max_results=2)
            context.append(f"LIVE WEB CONTEXT:\n{web_results}")
        except Exception as e:
            context.append(f"Web search: unavailable - {e}")

        return "\n\n".join(context)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    @traceable(name="data_retrieval_agent")
    async def run(self, input_data: dict) -> dict:
        task             = input_data.get("task", "")
        query            = input_data.get("query", "")
        document_findings = input_data.get("document_findings", "")
        self.log("Retrieving structured data", task=task)

        structured_data = self._load_structured_data(query)

        messages = [
            SystemMessage(content="""You are an enterprise data analyst.
Analyse the structured data and web context provided.
Extract key metrics and findings relevant to the task.
Be specific with numbers and percentages.
Reference the web context where relevant to add industry benchmarks."""),
            HumanMessage(content=(
                f"Task: {task}\n\n"
                f"Document findings for context:\n{document_findings}\n\n"
                f"Structured data and web context:\n{structured_data}"
            )),
        ]

        response = await self.llm.ainvoke(messages)
        self.log("Data retrieval complete")
        return {
            "agent":  self.name,
            "status": "completed",
            "output": response.content,
        }