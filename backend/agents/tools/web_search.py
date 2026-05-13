from ddgs import DDGS
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