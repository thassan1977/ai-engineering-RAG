# RAG Retrieval Engineering Lab

This repository is my practical learning project for building reliable Retrieval-Augmented Generation (RAG) systems.

I am not only calling an embedding API and sending the result to an LLM. I am building and measuring the retrieval layer step by step: tokenization, document ranking, semantic search, hybrid retrieval, evaluation metrics, and regression checks.

The goal is to understand how a RAG system finds the right evidence before an LLM uses it.

> **Roadmap:** see [ROADMAP.md](ROADMAP.md) for the step-by-step checklist taking this lab to a production-level RAG system on real documents (BEIR SciFact and the Kubernetes documentation).

## What this project demonstrates

- Building a reusable ranking interface.
- Implementing BM25 lexical search from first principles.
- Splitting documents into overlapping chunks.
- Creating real semantic embeddings with Sentence Transformers.
- Ranking chunks with cosine similarity and aggregating them back to documents.
- Combining BM25 and semantic results with Reciprocal Rank Fusion (RRF).
- Measuring retrieval quality with Recall@k, Precision@k, Reciprocal Rank@k, and NDCG@k.
- Comparing a baseline retriever with a candidate retriever.
- Detecting mean and per-query regressions with tolerances for floating-point errors.
- Excluding queries without relevance judgments instead of treating them as successful or failed retrievals.
- Keeping ranking deterministic with stable tie-breaking and repeatable evaluation.

## Why I built it

A RAG system can produce a confident answer from the wrong documents. Good retrieval is therefore a measurable engineering problem, not just a model-selection problem.

This project answers questions such as:

- Did the new retriever find more relevant documents?
- Did it place the best documents earlier in the list?
- Did it improve one query while damaging another?
- Is the average improvement hiding a serious per-query regression?
- Can a change be rejected automatically before it reaches production?

## Current retrieval pipeline

```text
Documents
   │
   ├── Lexical tokenizer ──> BM25 ranking
   │
   └── Chunk provider ──────> Sentence embeddings ──> Semantic ranking
                                                        │
BM25 results ───────────────────────────────────────────┤
                                                        ▼
                                                RRF hybrid ranking
                                                        │
                                                        ▼
                                               Top-k documents
                                                        │
                                                        ▼
                                                Metric evaluation
```

## Retrieval methods

### BM25

BM25 finds documents using exact terms from the query. It considers:

- How often a query term appears in a document.
- How common the term is across the collection.
- Document length normalization.
- The configured `k1` and `b` parameters.

This is a strong and explainable baseline for exact names, dates, identifiers, and domain terms.

### Semantic retrieval

Documents are split into overlapping chunks. Each chunk is embedded with:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The query and chunks are compared using cosine similarity. The document score is the highest similarity among its chunks.

The project uses real model embeddings rather than random vectors. The embedding provider separates document encoding from query encoding and normalizes vectors before comparison.

### Hybrid retrieval

BM25 and semantic scores are not directly comparable, so the project combines their ranked lists using Reciprocal Rank Fusion (RRF). This allows exact lexical matches and meaning-based matches to contribute without pretending their raw scores have the same scale.

The current flow retrieves a larger candidate set from both rankers, fuses the rankings, and returns the final top-k documents.

## Evaluation framework

The evaluation framework uses graded relevance judgments, for example:

```python
qrels = {
    "Q5": {
        "D21": 3,
        "D22": 2,
        "D23": 3,
        "D24": 2,
        "D25": 2,
        "D13": 1,
    }
}
```

The metrics are:

| Metric | What it measures |
|---|---|
| Recall@k | How many relevant documents were retrieved in the first k results |
| Precision@k | How many of the first k results are relevant |
| Reciprocal Rank@k | How early the first relevant result appears |
| NDCG@k | Whether highly relevant documents appear near the top |

Queries with empty relevance judgments are excluded from the mean because they do not provide evaluation information.

Every evaluation report includes:

- Score per query.
- Mean score.
- Number of evaluated queries.
- Number of excluded queries.
- Candidate-versus-baseline delta.
- Improved, regressed, unchanged, and excluded queries.

## Regression testing

Retrieval changes are checked against configurable limits:

- Maximum allowed drop in the mean score.
- Maximum allowed drop for an individual query.
- Floating-point tolerance for values such as `0.20000000000000007`.

This prevents a higher average score from hiding a serious regression for one important query.

## Results achieved so far

Using the current synthetic kindergarten-domain evaluation set at `k=5`, the hybrid candidate was compared with the BM25 baseline:

| Metric | BM25 baseline | Hybrid candidate | Change |
|---|---:|---:|---:|
| Recall@5 | 0.5731 | 0.6848 | +0.1117 |
| Precision@5 | 0.6600 | 0.7800 | +0.1200 |
| Reciprocal Rank@5 | 0.9500 | 1.0000 | +0.0500 |
| NDCG@5 | 0.7245 | 0.9086 | +0.1841 |

The regression checks passed for these results. The hybrid retriever also improved the difficult Q5 ranking by moving a highly relevant document to the first position.

These results are from a controlled learning dataset, not a claim of production accuracy. The next step is to evaluate against real anonymized queries and manually reviewed relevance judgments.

## Project design principles

- Use interfaces so ranking methods can be replaced and compared.
- Keep lexical tokenization separate from the model's internal semantic tokenizer.
- Preserve result order because ranking position affects RR and NDCG.
- Preserve duplicate tokens for BM25 term frequency.
- Use stable tie-breaking so repeated runs produce the same order.
- Validate vector dimensions before calculating cosine similarity.
- Cache document chunks and embeddings instead of recomputing them for every query.
- Make evaluation results inspectable instead of reporting only one average number.
- Prefer small, testable components over one large RAG function.

## Run locally

This project uses [uv](https://docs.astral.sh/uv/) for environments and dependencies. The Python version is pinned in `.python-version`, and uv installs it automatically if needed.

Install the runtime and development dependencies (including ruff, mypy, pytest and pre-commit):

```bash
uv sync
```

Install the git hooks (once per clone):

```bash
uv run pre-commit install
```

Run the application or evaluation entry point:

```bash
uv run python -m rag.main
```

Run the quality checks:

```bash
uv run ruff check && uv run ruff format --check && uv run mypy src
```

Run tests:

```bash
uv run pytest
```

The first semantic-search run downloads the configured Sentence Transformers model from Hugging Face.

## What I am learning next

- Add a cross-encoder reranker after BM25 and semantic retrieval.
- Tune RRF parameters on a validation set without touching the final test set.
- Add hard negative examples and larger real-world evaluation datasets.
- Store embeddings in PostgreSQL with pgvector.
- Measure latency, memory use, and throughput in addition to ranking quality.
- Add retrieval tracing so every final result can be explained.
- Connect the retrieval layer to an end-to-end RAG answer evaluation.

## Why this matters for real systems

The same design applies to support assistants, tax systems, education platforms, internal knowledge search, and agentic workflows. Before an AI agent performs an operation, it must retrieve the right policies, records, and context. This project focuses on making that retrieval measurable, testable, and safe to improve.

## Author

Built as part of my transition from senior backend and software architecture work into production AI engineering, with a focus on retrieval systems, evaluation, reliability, and explainable decision-making.
