from collections.abc import Sequence

from .metric import Metric
from .types import RelevanceJudgments


class ReciprocalRank(Metric):
    def score(self, relevance: RelevanceJudgments, retrieved_ids: Sequence[str]) -> float | None:
        relevant_set = set(relevance_id for relevance_id, score in relevance.items() if score > 0)
        if len(relevant_set) == 0:
            return None
        if len(retrieved_ids) == 0:
            return 0.0

        for i, doc_id in enumerate(retrieved_ids[: self.k], start=1):
            if doc_id in relevant_set:
                return 1.0 / i
        return 0.0
