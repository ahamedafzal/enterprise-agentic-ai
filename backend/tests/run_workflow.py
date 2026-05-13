import asyncio
from dotenv import load_dotenv

load_dotenv()

from backend.agents.workflow_graph import graph  # noqa: E402


async def main():
    print("\n🚀 Running NEXUS Agentic Workflow...\n")

    initial_state = {
        "query": "Analyse our Q4 project delays, identify the highest risk projects, and generate an executive action plan",
        "subtasks": None,
        "document_findings": None,
        "data_findings": None,
        "final_report": None,
        "status": "pending",
        "error": None,
    }

    result = await graph.ainvoke(initial_state)

    print("=" * 60)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"\nSubtasks planned: {len(result.get('subtasks') or [])}")
    print("\n📊 FINAL REPORT:")
    print(result.get("final_report", "No report generated"))


if __name__ == "__main__":
    asyncio.run(main())