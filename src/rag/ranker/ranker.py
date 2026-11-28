from abc import ABC, abstractmethod

from rag.model.query import Query


class Ranker(ABC):
    @abstractmethod
    def rank(self, query: Query, top_k: int) -> list[str]:
        pass
