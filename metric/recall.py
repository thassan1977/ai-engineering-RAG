

from .metric import Metric
from .types import RelevanceJudgments

class Recall(Metric):

    def score(self, relevance : RelevanceJudgments, retrieved_ids: list[str]) -> float | None:
        relevant_set = set(
            relevance_id 
            for relevance_id, score in relevance.items() if score > 0
        )
        if (len(relevant_set) <= 0):
            return None
        if (len(retrieved_ids) <= 0):
            return 0.0

        k_retrieved_set = set(retrieved_ids[:self.k])
        
        intersection = len(relevant_set & k_retrieved_set)
        recall = intersection / len(relevant_set)
        return recall

