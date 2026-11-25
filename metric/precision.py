

from metric.types import RelevanceJudgments

from .metric import Metric


class Precision(Metric):
    def score(self, relevance : RelevanceJudgments, retrieved_ids: list[str]) -> float | None:
        relevant_set = set(
            relevance_id 
            for relevance_id, score in relevance.items() if score > 0
        )
        if (len(relevant_set) <= 0):
            return None
        if (len(retrieved_ids) <= 0):
            return 0.0
        retrieved_set = set(retrieved_ids[:self.k])

        hits = len(relevant_set & retrieved_set)
        return hits / self.k 