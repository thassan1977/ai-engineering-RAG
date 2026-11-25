from .embed_base import EmbedBase


class SentenceEmbedProvider(EmbedBase):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        super().__init__(model_name=model_name, device=device)

    def embed_document(self, text: str) -> tuple[float, ...]:
        if not text or not text.strip():
            raise ValueError("text must not be empty")
        vector = self.model.encode_document(
            [text],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )[0]

        return tuple(float(value) for value in vector)

    def embed_query(self, text: str) -> tuple[float, ...]:
        if not text or not text.strip():
            raise ValueError("text must not be empty")
        vector = self.model.encode_query(
            [text],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )[0]

        return tuple(float(value) for value in vector)
        