from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    document_id: str
    chunk_id: str
    text: str
    embedding: tuple[float, ...] = ()
