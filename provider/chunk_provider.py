from model.document import Document
from model.chunk import Chunk
from utils.tokenizer import Tokenizer

CHUNK_SIZE = 50
CHUNK_OVERLAP = 20
class ChunkProvider:

    chunk_size: int
    chunk_overlap: int
    tokenizer: Tokenizer
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP, tokenizer: Tokenizer | None = None):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be non-negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")

        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tokenizer or Tokenizer()  # Use default tokenizer if null

    
    def get_chunks(self, document: Document) -> list[Chunk]:
        if document is None:
            raise ValueError("Document cannot be null")


        if document.text is None or document.text.strip() == "":
            raise ValueError("Document text cannot be None or empty")
        
        tokens = self.tokenizer.tokenize(document.text)
        if not tokens:
            raise ValueError("document has no tokens after tokenization")
        
        step = self.chunk_size - self.chunk_overlap
        chunks = []

        for start in range(0, len(tokens), step):
            chunk_tokens = tokens[start:start + self.chunk_size]

            if not chunk_tokens:
                break

            chunk_id = f"{document.id}_{len(chunks)}"
            chunks.append(Chunk(document.id, chunk_id, " ".join(chunk_tokens)))

            if start + self.chunk_size >= len(tokens):
                break
        return chunks
        