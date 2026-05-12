from sentence_transformers import CrossEncoder
import structlog

logger = structlog.get_logger()

_model = None

def get_reranker() -> CrossEncoder:
    """Load cross-encoder model once and cache it."""
    global _model
    if _model is None:
        logger.info("Loading re-ranker model (first time only)...")
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        logger.info("Re-ranker model loaded")
    return _model

def rerank(query: str, documents: list[str], top_k: int = 3) -> list[str]:
    """
    Re-rank documents by relevance to query using cross-encoder.
    
    ChromaDB returns docs by vector similarity (fast but approximate).
    Cross-encoder re-ranks by actually reading query+doc together (slower but accurate).
    Returns top_k most relevant documents.
    """
    if not documents:
        return documents

    if len(documents) <= top_k:
        return documents

    try:
        model  = get_reranker()
        pairs  = [(query, doc) for doc in documents]
        scores = model.predict(pairs)

        # Zip scores with docs, sort descending, take top_k
        scored_docs = sorted(zip(scores, documents), reverse=True)
        reranked    = [doc for _, doc in scored_docs[:top_k]]

        logger.info(
            "Re-ranking complete",
            original_count=len(documents),
            returned_count=len(reranked),
            top_score=round(float(scored_docs[0][0]), 3),
        )
        return reranked

    except Exception as e:
        logger.warning("Re-ranking failed, using original order", error=str(e))
        return documents[:top_k]