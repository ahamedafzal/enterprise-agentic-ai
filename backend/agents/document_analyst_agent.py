import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from backend.agents.base_agent import BaseAgent
from backend.core.config import settings

class DocumentAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("DocumentAnalystAgent")
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.1,
        )
        self.chroma = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

    @traceable(name="document_analyst_agent")
    async def run(self, input_data: dict) -> dict:
        task  = input_data.get("task", "")
        query = input_data.get("query", "")
        self.log("Analysing documents", task=task)

        # Retrieve from all 3 collections
        context_parts = []
        for collection_name in ["project_reports", "contracts", "employees"]:
            try:
                col = self.chroma.get_collection(collection_name)
                results = col.query(query_texts=[query], n_results=5)
                docs = results["documents"][0]
                context_parts.append(
                    f"=== {collection_name.upper()} ===\n" + "\n\n".join(docs)
                )
            except Exception as e:
                self.log(f"Collection {collection_name} error", error=str(e))

        context = "\n\n".join(context_parts)

        messages = [
            SystemMessage(content="""You are an expert enterprise document analyst.
Analyse the provided documents and extract key insights relevant to the task.
Be specific, data-driven, and concise. Structure your response clearly."""),
            HumanMessage(content=f"Task: {task}\n\nDocuments:\n{context}"),
        ]

        response = await self.llm.ainvoke(messages)
        self.log("Document analysis complete")
        return {
            "agent": self.name,
            "status": "completed",
            "output": response.content,
            "sources": len(context_parts),
        }