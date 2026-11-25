from abc import ABC, abstractmethod
from .types import RelevanceJudgments


class Metric(ABC): 
    k: int

    def __init__(self, k: int):
        if k <= 0:
            raise ValueError("k must be a positive integer")
        if not isinstance(k, int):
            raise TypeError("k must be an integer")
    
        self.k = k

    @abstractmethod
    def score(self, relevance: RelevanceJudgments, retrieved_ids: list[str]) -> float | None:
        pass

    @staticmethod
    def mean(scores: list[float | None]) -> float | None:
        relevant_list = [ score for score in scores if score is not None]
        relevant_list_length = len(relevant_list)
        if (relevant_list_length <= 0):
            return None
        return sum(relevant_list) / relevant_list_length
