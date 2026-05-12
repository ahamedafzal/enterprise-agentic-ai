from duckduckgo_search import DDGS
import structlog

logger = structlog.get_logger()

def web_search(query: str, max_results: int = 3) -> str:
    """Search the web using DuckDuckGo — free, no API key needed."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"{i}. {r.get('title', 'No title')}\n"
                f"   {r.get('body', 'No description')}\n"
                f"   Source: {r.get('href', 'Unknown')}"
            )

        return "\n\n".join(formatted)

    except Exception as e:
        logger.error("Web search failed", error=str(e))
        return f"Web search unavailable: {str(e)}"


def calculate(expression: str) -> str:
    """Safe calculator tool for agents."""
    try:
        # Only allow safe mathematical expressions
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return "Error: Only mathematical expressions allowed"
        result = eval(expression)  # noqa: S307
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"