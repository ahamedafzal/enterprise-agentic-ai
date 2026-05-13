from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.agents.base_agent import BaseAgent
from backend.core.config import settings
import json

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("OrchestratorAgent")
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.1,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    @traceable(name="orchestrator_agent")
    async def run(self, input_data: dict) -> dict:
        query = input_data.get("query", "")
        self.log("Decomposing query", query=query)

        messages = [
            SystemMessage(content="""You are an enterprise AI orchestrator.
Your job is to decompose a user query into subtasks for specialist agents.
Always respond with valid JSON only. No explanation, no markdown.
Return format:
{
  "subtasks": [
    {"agent": "document_analyst", "task": "specific instruction"},
    {"agent": "data_retrieval", "task": "specific instruction"},
    {"agent": "report_generator", "task": "specific instruction"}
  ],
  "summary": "one line description of what will be done"
}
Available agents: document_analyst, data_retrieval, report_generator"""),
            HumanMessage(content=f"Decompose this enterprise query: {query}"),
        ]

        response = await self.llm.ainvoke(messages)
        raw = response.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        result = json.loads(raw.strip())
        self.log("Query decomposed", subtasks=len(result["subtasks"]))
        return {
            "agent":  self.name,
            "status": "completed",
            "output": result,
        }