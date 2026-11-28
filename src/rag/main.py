import math

import rag.utils.dataset as dataset
from rag.metric.ndcg import NDCG
from rag.metric.precision import Precision
from rag.metric.recall import Recall
from rag.metric.reciprocalrank import ReciprocalRank
from rag.provider.chunk_provider import ChunkProvider
from rag.provider.embedding.sentence_embed_provider import SentenceEmbedProvider
from rag.provider.storage_provider import StorageProvider
from rag.ranker.bm25ranker import Bm25Ranker
from rag.ranker.semanticranker import SemanticRanker
from rag.utils.evaluate import Evaluator

MAX_MEAN_ALLOWED_DROP = 0.01
MAX_QUERY_ALLOWED_DROP = 0.20
EMBEDDING_DIMENSIONS = 10


if __name__ == "__main__":
    # bm25_ranker = Bm25Ranker(documents)

    # print('========================')
    # print(bm25_ranker.rank(queries["Q1"], top_k=3))

    # bm25_runs = {
    #     query_id: bm25_ranker.rank(query, top_k=3)
    #     for query_id, query in queries.items()
    # }
    # print(f' bm25_runs = {bm25_runs}')
    # print('=========================')

    # baseline_rr = evaluate(qrels, baseline_runs, ReciprocalRank(k=3))
    # candidate_rr = evaluate(qrels, bm25_runs, ReciprocalRank(k=3))
    # baseline_recall = evaluate(qrels, baseline_runs, Recall(k=3))
    # candidate_recall = evaluate(qrels, bm25_runs, Recall(k=3))

    # baseline_precision = evaluate(qrels, baseline_runs, Precision(k=3))
    # candidate_precision = evaluate(qrels, bm25_runs, Precision(k=3))

    # print(baseline_rr)
    # print(baseline_recall)
    # print(baseline_precision)
    # print(candidate_rr)
    # print(candidate_recall)
    # print(candidate_precision)

    # recall_report = compare_reports(baseline_recall, candidate_recall)
    # rr_report = compare_reports(baseline_rr, candidate_rr)
    # precision_report = compare_reports(baseline_precision, candidate_precision)

    # print(f'RR report: {rr_report}')
    # print(f'Recall report: {recall_report}')
    # print(f'Precision report: {precision_report}')

    # # reqression
    # rr_regression_report = check_regression(rr_report, max_mean_drop=0.01, max_query_drop=0.25)
    # recall_regression_report = check_regression(recall_report, max_mean_drop=0.01, max_query_drop=0.25)
    # precision_regression_report = check_regression(precision_report, max_mean_drop=0.01, max_query_drop=0.25)
    # print(f'RR regression: {rr_regression_report}')
    # print(f'Recall regression: {recall_regression_report}')
    # print(f'Precision regression: {precision_regression_report}')

    # ndcg = NDCG(k=3)
    # baseline_eval = Evaluator.evaluate(qrels, baseline_runs, ndcg)
    # candidate_eval = Evaluator.evaluate(qrels, candidate_runs, ndcg)
    # print(f' baseline Evaluator NDCG: { baseline_eval}')
    # print(f' candidate Evaluator NDCG: {candidate_eval}')

    # report = Evaluator.compare_reports(baseline_eval, candidate_eval)
    # print(report)

    # regression = Evaluator.check_regression(
    #     report,
    #     max_mean_drop=MAX_MEAN_ALLOWED_DROP,
    #     max_query_drop=MAX_QUERY_ALLOWED_DROP,
    # )
    # print(regression)

    # print ('=============================================')
    # chunkProvider = ChunkProvider(chunk_size=5, chunk_overlap=2)
    # document4 = Document("D1", "a b c d")
    # document5 = Document("D1", "a b c d e")
    # document6 = Document("D1", "a b c d e f")
    # document10 = Document("D1", "a b c d e f g h i j")
    # document11 = Document("D1", "a b c d e f g h i j h")
    # document12 = Document("D1", "a b c d e f g h i j h k")
    # chunks4 = chunkProvider.get_chunks(document4)
    # print(f'Chunk len 4= {chunks4}')
    # chunks5 = chunkProvider.get_chunks(document5)
    # print(f'Chunk len 5= {chunks5}')
    # chunks6 = chunkProvider.get_chunks(document6)
    # print(f'Chunk len 6= {chunks6}')
    # chunks10 = chunkProvider.get_chunks(document10)
    # print(f'Chunk len 10= {chunks10}')
    # chunks11 = chunkProvider.get_chunks(document11)
    # print(f'Chunk len 11= {chunks11}')
    # chunks12 = chunkProvider.get_chunks(document12)
    # print(f'Chunk len 12= {chunks12}')
    # print ('=============================================')

    print("=============================================")
    storageProvider = StorageProvider()
    embeddingProvider = SentenceEmbedProvider()
    chunkProvider = ChunkProvider(chunk_size=50, chunk_overlap=20)
    semanticRanker = SemanticRanker(embeddingProvider, chunkProvider, storageProvider, documents=dataset.documents)
    # semanticRanker.rank(Query("Q1","cats sit on the mat"), top_k=5)
    v1 = embeddingProvider.embed_query("feline behavior")
    v2 = embeddingProvider.embed_query("feline behavior")

    assert len(v1) == embeddingProvider.dimension
    assert len(v2) == embeddingProvider.dimension

    print(f"v1 length = {len(v1)}, v2 length = {len(v2)}, dimension = {embeddingProvider.dimension}")

    assert all(math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-7) for a, b in zip(v1, v2))

    query = embeddingProvider.embed_query("feline behavior and sleeping habits")

    related = embeddingProvider.embed_document("kittens sleep in a warm basket")

    unrelated = embeddingProvider.embed_document("the school bus arrives early")

    print(f"Cosine similarity (query, related) = {semanticRanker.cosine_similarity(query, related)}")
    print(f"Cosine similarity (query, unrelated) = {semanticRanker.cosine_similarity(query, unrelated)}")

    print("=============================================")

    top_k = 5
    metrics = [
        Recall(k=top_k),
        Precision(k=top_k),
        ReciprocalRank(k=top_k),
        NDCG(k=top_k),
    ]

    bm25Ranker = Bm25Ranker(documents=dataset.documents)
    semanticRanker = SemanticRanker(embeddingProvider, chunkProvider, storageProvider, documents=dataset.documents)

    bm25_runs = {query_id: bm25Ranker.rank(query, top_k) for query_id, query in dataset.queries.items()}

    semantic_runs = {query_id: semanticRanker.rank(query, top_k) for query_id, query in dataset.queries.items()}

    for metric in metrics:
        bm25_report = Evaluator.evaluate(
            dataset.qrels,
            bm25_runs,
            metric,
        )

        semantic_report = Evaluator.evaluate(
            dataset.qrels,
            semantic_runs,
            metric,
        )

        print(bm25_report)
        print(semantic_report)
        compare = Evaluator.compare_reports(bm25_report, semantic_report)
        print(Evaluator.check_regression(compare, MAX_MEAN_ALLOWED_DROP, MAX_QUERY_ALLOWED_DROP))
        print("Q5 qrels:", dataset.qrels["Q5"])
        print("Q5 BM25:", bm25_runs["Q5"])
        print("Q5 semantic:", semantic_runs["Q5"])
