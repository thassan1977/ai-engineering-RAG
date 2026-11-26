

import math

from metric.metric import Metric
from .types import RelevanceJudgments


class NDCG(Metric):
    def score(self, relevance : RelevanceJudgments, retrieved_ids: list[str]) -> float | None:
        if not relevance:
            return None
        if not retrieved_ids:
            return 0

        if len(retrieved_ids[:self.k]) != len(set(retrieved_ids[:self.k])):
           raise ValueError("retrieved_ids must not have duplicate document IDs")

        dcg = 0.0
        for i, retrieved_id in enumerate(retrieved_ids[:self.k], start=1):    
            rel_value = relevance.get(retrieved_id, 0)
            dcg += (2 ** rel_value - 1) / math.log2(i + 1)

        ranked_dcg = sorted(
            relevance.values(),
            reverse=True,
        )[:self.k]


        ideal_dcg = sum(
            (2 ** rel_value - 1) / math.log2(i + 1)
            for i, rel_value in enumerate(ranked_dcg, start=1)
        )
        return min(1.0, max(0, dcg / ideal_dcg)) if ideal_dcg > 0 else 0
            

