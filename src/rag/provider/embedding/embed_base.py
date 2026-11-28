from abc import ABC, abstractmethod

from sentence_transformers import SentenceTransformer


class EmbedBase(ABC):
    def __init__(self, model_name: str, device: str | None = None):
        if not model_name:
            raise ValueError("model_name must be provided")

        self.model_name = model_name
        self.device = device

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )

        self.dimension = self.model.get_sentence_embedding_dimension()

    @abstractmethod
    def embed_document(self, text: str) -> tuple[float, ...]:
        pass

    @abstractmethod
    def embed_query(self, text: str) -> tuple[float, ...]:
        pass
