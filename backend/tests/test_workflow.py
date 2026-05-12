
def test_workflow_state_structure():
    """Test that WorkflowState has correct keys."""
    from backend.agents.workflow_graph import WorkflowState
    state: WorkflowState = {
        "query": "test query",
        "subtasks": None,
        "document_findings": None,
        "data_findings": None,
        "final_report": None,
        "status": "pending",
        "error": None,
    }
    assert state["query"] == "test query"
    assert state["status"] == "pending"

def test_graph_builds():
    """Test that LangGraph compiles without errors."""
    from backend.agents.workflow_graph import build_graph
    g = build_graph()
    assert g is not None

def test_agents_import():
    """Test all agents import correctly."""
    from backend.agents.orchestrator_agent import OrchestratorAgent
    from backend.agents.document_analyst_agent import DocumentAnalystAgent
    from backend.agents.data_retrieval_agent import DataRetrievalAgent
    from backend.agents.report_generator_agent import ReportGeneratorAgent
    assert OrchestratorAgent is not None
    assert DocumentAnalystAgent is not None
    assert DataRetrievalAgent is not None
    assert ReportGeneratorAgent is not None