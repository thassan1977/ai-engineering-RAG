

from ranker.ranker import Ranker
from model.query import Query

class HybridRanker(Ranker):
    def __init__(self,
                 bm25Ranker: Ranker,
                 semanticRanker: Ranker,
                 rrf_constant: int = 60,
                 bm25_weight: float = 1.0,
                 semantic_weight: float = 1.0):
        if rrf_constant < 0:
            raise ValueError("rrf_constant must be non-negative")

        if bm25_weight < 0 or semantic_weight < 0:
            raise ValueError("weights must be non-negative")
        
        self.bm25Ranker = bm25Ranker
        self.semanticRanker = semanticRanker
        self.rrf_constant = rrf_constant
        self.bm25_weight = bm25_weight
        self.semantic_weight = semantic_weight

    def rank(self, query: Query, top_k: int):
        if top_k <= 0:
            raise ValueError("top_k must be positive")


        candidate_k = max(top_k * 10, 20)
        fused_docs: dict[str, float] = {}


        bm25_results = self.bm25Ranker.rank(query, candidate_k)
        semantic_results = self.semanticRanker.rank(query, candidate_k)
        

        for rank, doc_id in enumerate(bm25_results, start=1):
            fused_docs[doc_id] = fused_docs.get(doc_id, 0.0) + self.bm25_weight / (self.rrf_constant + rank)
    
        for rank, doc_id in enumerate(semantic_results, start=1):
            fused_docs[doc_id] = fused_docs.get(doc_id, 0.0) + self.semantic_weight / (self.rrf_constant + rank)

        for rank, doc_id in enumerate(semantic_results, start=1):
            fused_docs[doc_id] = (
                fused_docs.get(doc_id, 0.0)
                + self.semantic_weight / (self.rrf_constant + rank)
            )

        ranked_docs = sorted(
            fused_docs.items(), key=lambda item: (-item[1], item[0])
        )

        return [doc_id for doc_id, _ in ranked_docs[:top_k]]

