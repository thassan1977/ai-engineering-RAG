from rag.model.chunk import Chunk

# a way to save chunk data in memory instead of using a database for the testing


class StorageProvider:
    data: dict[str, list[Chunk]]

    def __init__(self) -> None:
        self.data = {}

    def save_chunk(self, key: str, chunk: Chunk) -> None:
        if not key:
            raise ValueError("Key must be provided")
        if not chunk:
            raise ValueError("Chunk must be provided")

        if key not in self.data:
            self.data[key] = []
        self.data[key].append(chunk)
        # print(f'Saved chunk docID={chunk.document_id}, chunkID= {chunk.chunk_id}, chunkText {chunk.text}')
