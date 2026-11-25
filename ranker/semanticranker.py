from model.chunk import Chunk
from model.document import Document
from provider.chunk_provider import ChunkProvider
from provider.embedding.embed_base import EmbedBase
from ranker.ranker import Ranker
from model.query import Query
from provider.embedding.sentence_embed_provider import SentenceEmbedProvider
from provider.storage_provider import StorageProvider
import math
from dataclasses import replace

class SemanticRanker(Ranker):
    MAX_CHUNK_SIZE = 5  # Maximum chunk size tokens normal 200 -> 500
    MAX_OVERLAP_SIZE = 2  # Maximum overlap size tokens normal 20 -> 50 (10% of chunk size)

    documents: list[Document]
    # providers for embedding, chunking, and storage
    embedding_provider: EmbedBase
    chunk_provider: ChunkProvider
    storage_provider: StorageProvider
    
    doc_embeddings: dict[str, list[Chunk]]


    # semantic ranker use chuncks of dcument not whole document
    # and use cosine similarity to compare the chunks with the query embedding
    # and return the top k docs where document score is the maximum similarity among its chunks


    def __init__(self, embedding_provider: EmbedBase, chunk_provider: ChunkProvider, 
                 storage_provider: StorageProvider, documents: list[Document]):
        self.documents = documents
        self.embedding_provider = embedding_provider
        self.chunk_provider = chunk_provider
        self.storage_provider = storage_provider
        # prepare embedding for all docs in the corpus
        self.embed_documents()  

    def embed_documents(self):
        self.doc_embeddings = {}
        for document in self.documents:
            chunks = self.chunk_provider.get_chunks(document)
            embedded_chunks = []

            for chunk in chunks:
                embedded_chunk = replace(
                    chunk,
                    embedding = tuple(self.embedding_provider.embed_document(chunk.text))
                )
                embedded_chunks.append(embedded_chunk)
                self.storage_provider.save_chunk(document.id, embedded_chunk)

            self.doc_embeddings[document.id] = embedded_chunks
            
    def cosine_similarity(self, vec1: tuple[float,...], vec2: tuple[float, ...]) -> float:
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have the same length")
        
        # cosine sim = A.B / (||A|| * ||B||)
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)
    
    def rank(self, query: Query, top_k: int) -> list[str]:
        if query is None or not query.text or not query.text.strip():
            raise ValueError("query must not be empty")

        if top_k <= 0:
            raise ValueError("top_k must be positive")
    
        # embed query
        query_embedding = self.embedding_provider.embed_query(query.text)

        # cosine similarity between query embedding and document embeddings
        similarities = []
        for document_id, chunks in self.doc_embeddings.items():
            doc_score = -math.inf

            for chunk in chunks:
                similarity = self.cosine_similarity(query_embedding, chunk.embedding)
                doc_score = max(doc_score, similarity)
            # doc score is the maximum similarity among its chunks
            similarities.append((document_id, doc_score))

        # sort by similarity descending
        similarities.sort(key=lambda item: (-item[1], item[0]))

        # return top k document ids, removing duplicates while preserving order
        return [document_id for document_id, _ in similarities[:top_k]]

