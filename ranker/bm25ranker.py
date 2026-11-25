
from model.document import Document
from model.query import Query
from ranker.ranker import Ranker
from utils.tokenizer  import Tokenizer
from math import log

class Bm25Ranker(Ranker):
    k1: float
    b: float
    doc_tokens: dict[str, list[str]]
    doc_lengths: dict[str, int]
    doc_frequency: dict[str, int]
    avg_doc_length: float

    documents: list[Document]

    def __init__(self, documents: list[Document], k1: float = 1.5, b: float = 0.75):
        if (k1 < 0):
            raise ValueError("k1 must be non-negative")
        if (b < 0 or b > 1):
            raise ValueError("b must be between 0 and 1")
        
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.doc_tokens = {}
        self.doc_lengths = {}
        self.doc_frequency = {}
        self.avg_doc_length = 0.0

        for doc in self.documents:
            # reject duplicate document IDs
            if doc.id in self.doc_tokens:
                raise ValueError(f"Duplicate document ID: {doc.id}")

            self.doc_tokens[doc.id] = Tokenizer.tokenize(doc.text)
            self.doc_lengths[doc.id] = len(self.doc_tokens[doc.id])
            for token in set(self.doc_tokens[doc.id]):
                self.doc_frequency[token] = self.doc_frequency.get(token, 0) + 1

        self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0.0

    def _idf(self, N: int, document_frequency: int):
        return log(1 + (N - document_frequency + 0.5)/(document_frequency + 0.5))
    
    def _score_document(
        self,
        query_tokens: list[str],
        document_id: str,
    ) -> float:
        N = len(self.doc_tokens)

        score = 0.0
        for query_token in set(query_tokens):
            tf = self.doc_tokens[document_id].count(query_token)
            if tf == 0:
                continue

            document_frequency = self.doc_frequency.get(query_token,0)
            if document_frequency == 0:
                continue

            idf = self._idf(N, document_frequency)
            normalization = 1 - self.b + self.b * self.doc_lengths[document_id] / self.avg_doc_length
            score += idf * (tf * (self.k1 + 1) ) / ( tf + self.k1 * normalization)
        return score

    
    def rank(self, query: Query, top_k: int) -> list[str]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        if not self.documents:
            return []
        
        query_tokens = Tokenizer.tokenize(query.text)
        if not query_tokens:
            raise ValueError("query must contain at least one token")

        scores : dict[str, float] = {}

        for doc in self.documents:
            scores[doc.id] = self._score_document(query_tokens, doc.id)
             
 
        ranked = sorted(
        scores.items(),
            key=lambda item: (-item[1], item[0])
        )

        return [
            document_id
            for document_id, score in ranked
            if score > 0
        ][:top_k]
        
