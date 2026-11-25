from abc import ABC, abstractmethod

from model.query import Query

class Ranker(ABC):
    @abstractmethod
    def rank(self, query: Query, top_k: int | None = None) -> list[str]:
        pass