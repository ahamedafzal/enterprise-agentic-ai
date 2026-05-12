from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from backend.agents.base_agent import BaseAgent
from backend.core.config import settings
from datetime import datetime

class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportGeneratorAgent")
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.2,
        )

    @traceable(name="report_generator_agent")
    async def run(self, input_data: dict) -> dict:
        query             = input_data.get("query", "")
        document_findings = input_data.get("document_findings", "")
        data_findings     = input_data.get("data_findings", "")
        self.log("Generating executive report")

        messages = [
            SystemMessage(content="""You are a senior enterprise AI consultant.
Generate a structured executive report based on the findings provided.
Use this exact markdown structure:

# Executive Report
**Date:** [today]
**Query:** [the original query]

## Executive Summary
[2-3 sentence overview]

## Key Findings
### Document Analysis
[bullet points from document findings]

### Data Analysis
[bullet points from data findings]

## Risk Assessment
[identified risks with severity: High/Medium/Low]

## Recommendations
[numbered list of actionable recommendations]

## Action Items
| Action | Owner | Priority | Deadline |
|--------|-------|----------|----------|
[3-5 action items]

## Conclusion
[1-2 sentences]"""),
            HumanMessage(content=(
                f"Original Query: {query}\n\n"
                f"Document Analysis Findings:\n{document_findings}\n\n"
                f"Data Analysis Findings:\n{data_findings}\n\n"
                f"Today's date: {datetime.now().strftime('%B %d, %Y')}"
            )),
        ]

        response = await self.llm.ainvoke(messages)
        self.log("Report generation complete")
        return {
            "agent": self.name,
            "status": "completed",
            "output": response.content,
        }