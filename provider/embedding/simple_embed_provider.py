
from hashlib import sha256
from random import Random

# simple embedding provider for testing the ranker only, no coherent embedding results just for testing
class SimpleEmbedProvider:
    dimension: int

    def __init__(self, dimension: int):
        if dimension <= 0:
            raise ValueError("dimension must be non-negative")
        self.dimension = dimension

    def get_embedding(self, text: str) -> tuple[float, ...]:
        if not text or not text.strip():
            raise ValueError("text must not be empty")

        digest = sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(digest[:8], byteorder="big")

        random = Random(seed)

        return tuple(
            random.uniform(-1.0, 1.0)
            for _ in range(self.dimension)
        )
    