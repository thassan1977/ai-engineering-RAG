# Production Roadmap

This is the step-by-step plan for taking this lab from a toy dataset to a production-level RAG system on real documents.

**Rules**

- Work on one step at a time. Don't start a step until every "done when" box of the previous step is ticked.
- I write the algorithms myself: BM25, chunking, RRF, metrics, reranking orchestration, evaluation.
- I use proven libraries for infrastructure: Postgres, FastAPI, OpenTelemetry, Docker.
- Tuning happens on the **dev** split. Final numbers are reported on the **test** split only.

## Progress

| Phase | Steps | Status |
|---|---|---|
| 0. Foundations | 0.1 – 0.4 | ⬜ Not started |
| 1. Real documents and ingestion | 1.1 – 1.5 | ⬜ Not started |
| 2. Evaluation data | 2.1 – 2.3 | ⬜ Not started |
| 3. Retrieval at scale | 3.1 – 3.6 | ⬜ Not started |
| 4. Generation | 4.1 – 4.4 | ⬜ Not started |
| 5. Service | 5.1 – 5.3 | ⬜ Not started |
| 6. Observability and operations | 6.1 – 6.5 | ⬜ Not started |
| 7. Showcase | 7.1 – 7.3 | ⬜ Not started |

Status key: ⬜ not started · 🟡 in progress · ✅ done

## Corpora

| | Benchmark corpus | Domain corpus (the real system) |
|---|---|---|
| Dataset | **BEIR SciFact**: about 5k scientific abstracts, 300 test queries with official relevance judgments | **Kubernetes documentation**: [`kubernetes/website`](https://github.com/kubernetes/website), `content/en/docs/` |
| Purpose | Prove the algorithms are correct by comparing against published baselines | Real multi-page documents for every tuning decision and the final demo |
| Relevance judgments | Included with the dataset | Hand-reviewed golden set (step 2.2) |
| License | Check the dataset card (typically non-commercial) | CC BY 4.0, attributed in the README |

### Kubernetes corpus scope

Start small, then grow:

- [ ] **A:** `concepts/`. Mostly explanation, a few hundred pages.
- [ ] **B:** add `tasks/`, `tutorials/` and `setup/`. Procedural how-to content.
- [ ] **C:** add `reference/kubectl` and `reference/glossary`. Exact-term queries.
- Skipped for now: the generated API reference (huge generated tables).

Pin the source commit SHA in the dataset manifest. Re-ingesting a newer commit later is a real-world test of step 1.5.

---

## Phase 0: Foundations

Goal: make the existing code trustworthy.

### 0.1 Project structure and tooling

- [ ] Move to a `src/` layout with `pyproject.toml`
- [ ] Manage environments with `uv`
- [ ] Add `ruff` (lint and format), `mypy` and `pre-commit`
- [ ] Fix `.gitignore` (add `.DS_Store`) and remove the committed `.DS_Store`
- **Done when:**
  - [ ] `uv sync && ruff check && mypy src` all pass

### 0.2 Tests for everything that exists

- [ ] Hand-computed test cases for Recall, Precision, RR and NDCG
- [ ] BM25 on a 3-document corpus
- [ ] Chunk boundary cases
- [ ] Evaluator, `compare_reports` and `check_regression`
- [ ] RRF with fake rankers
- [ ] Fix the RRF bug (the semantic loop runs twice)
- [ ] Make NDCG and the other metrics agree on all-zero judgments (`0` vs `None`)
- **Done when:**
  - [ ] The RRF test failed on the old code and passes after the fix
  - [ ] Coverage on core modules is 85% or higher

### 0.3 Configuration

- [ ] Experiment configs in YAML: model, chunk size, k1/b, RRF k and weights, candidate_k, top_k
- [ ] Load them with `pydantic-settings`
- [ ] Remove hard-coded constants (for example `candidate_k` in RRF)
- **Done when:**
  - [ ] Changing any parameter needs no code edit

### 0.4 CI

- [ ] GitHub Actions running lint, type checks and tests on every PR
- **Done when:**
  - [ ] The CI badge is green in the README

---

## Phase 1: Real documents and ingestion

### 1.1 Data model v2

- [ ] `Document`: id, source, title, url, metadata, content hash, ingested_at
- [ ] `Chunk`: id, doc_id, text, section path (for example `Concepts > Pods > Lifecycle`), character offsets, token count
- **Done when:**
  - [ ] Every chunk traces back to an exact location in its source

### 1.2 Loaders

- [ ] SciFact loader for the corpus, queries and judgment files
- [ ] Kubernetes loader: parse Markdown and front matter (`title`, `content_type`, `weight`)
- [ ] Derive the public URL from the file path and keep heading anchors
- [ ] Shortcode handling:
  - [ ] `glossary_tooltip` → keep the visible text only
  - [ ] `note` / `caution` / `warning` → keep the content, prefixed with "Note:", "Caution:" or "Warning:"
  - [ ] `feature-state` → keep as text and store as version metadata
  - [ ] `code_sample` → inline the YAML from `content/en/examples/`
  - [ ] Tabs, includes and partials → flatten
  - [ ] Unknown shortcodes → log them, never drop them silently
- **Done when:**
  - [ ] Both corpora load into the models
  - [ ] A stats report shows document count, length distribution and empty or broken pages

### 1.3 Separate text pipelines

- [ ] BM25 gets the lexical tokenizer (lowercase, punctuation removed; optionally stopwords and stemming)
- [ ] Embeddings get the **original** text
- **Done when:**
  - [ ] A test proves the embedding input keeps its casing and punctuation

### 1.4 Chunking v2

- [ ] Split on `##` / `###` headings first, then on paragraphs
- [ ] Measure size with the embedding model's own tokenizer, staying under its max sequence length
- [ ] Overlap between chunks
- [ ] Prefix each chunk with `Title > Section > Subsection`
- [ ] Never split inside a code block
- [ ] Flag `_index.md` pages that are only lists of links
- **Done when:**
  - [ ] A chunk-size histogram and a manual review of 20 sample chunks look right

### 1.5 Idempotent ingestion

- [ ] Re-ingest based on content hashes, so only changed documents are re-processed
- [ ] Dataset manifest: corpus commit SHA, document count, hash
- **Done when:**
  - [ ] Running ingestion twice changes nothing
  - [ ] Editing one file re-processes only that file

---

## Phase 2: Evaluation data

This is the most important phase: every later change is measured against it.

### 2.1 SciFact sanity check

- [ ] Run BM25 and semantic retrieval on SciFact
- **Done when:**
  - [ ] BM25 NDCG@10 is close to the published BEIR BM25 figure (about 0.66–0.69). If it isn't, there's a bug.

### 2.2 Kubernetes golden set

- [ ] 150–200 questions, split into **dev** and **test**
- [ ] Question mix:
  - [ ] Factual (20%), for example "What is the default restart policy for a Pod?"
  - [ ] How-to (20%), for example "How do I safely drain a node before maintenance?"
  - [ ] Exact-term (15%), for example "What does `kubectl apply --dry-run=server` do?"
  - [ ] Paraphrased, with no shared keywords (15%), for example "How do I stop a container eating all the memory on a machine?"
  - [ ] Comparison / multi-hop (15%), for example "When should I use a StatefulSet instead of a Deployment?"
  - [ ] Unanswerable (15%), for example "How do I configure Docker Swarm overlay networks?"
- [ ] Each question records:
  - [ ] the question and its type
  - [ ] graded evidence spans (3 = directly answers, 2 = partly, 1 = related)
  - [ ] a 1–3 sentence reference answer
  - [ ] whether it's answerable
- [ ] Label **evidence spans** (document path + heading anchor, or character range), **not chunks**. A chunk counts as relevant if it overlaps a labelled span, so the labels survive re-chunking.
- [ ] Process:
  - [ ] Have an LLM draft questions from sampled sections
  - [ ] Review and rewrite every draft by hand
  - [ ] Write the paraphrased and unanswerable questions entirely by hand
- **Done when:**
  - [ ] The golden set is versioned in the repo
  - [ ] A dataset README explains how it was built

### 2.3 Experiment runner and results store

- [ ] One command runs a config against a dataset
- [ ] Each run is saved as JSON with git SHA, config hash and dataset version
- [ ] Results tables are auto-generated in Markdown
- [ ] Bootstrap confidence intervals
- **Done when:**
  - [ ] `python -m ragkit.eval --config configs/hybrid.yaml` reproduces a committed results table

---

## Phase 3: Retrieval at scale

### 3.1 BM25 with an inverted index

- [ ] Precomputed term frequencies and postings lists, replacing the per-document `.count()` scans
- **Done when:**
  - [ ] SciFact query latency is a few milliseconds
  - [ ] A regression test proves the scores match the old implementation exactly

### 3.2 Embeddings done properly

- [ ] Batched encoding
- [ ] Embedding cache keyed by (model, chunk hash)
- [ ] Compare `all-MiniLM-L6-v2`, `bge-small-en-v1.5` and `e5-small-v2` (some need query/passage prefixes)
- **Done when:**
  - [ ] A results table shows quality, index time and vector size per model
  - [ ] The model choice is justified

### 3.3 Postgres and pgvector

- [ ] Docker Compose with Postgres and pgvector
- [ ] Schema: documents, chunks, embeddings
- [ ] Alembic migrations
- [ ] HNSW index
- [ ] Measure ANN recall against exact search
- [ ] Optional: compare BM25 with Postgres full-text search
- **Done when:**
  - [ ] Retrieval runs from the database
  - [ ] ANN recall@50 is 0.95 or higher against exact search

### 3.4 Hybrid RRF, tuned honestly

- [ ] Tune the RRF k, weights and candidate_k on dev
- [ ] Report on test
- **Done when:**
  - [ ] A results table shows BM25 vs semantic vs hybrid on both corpora, with confidence intervals

### 3.5 Cross-encoder reranking

- [ ] A `Reranker` abstraction, separate from `Ranker`, with access to document text
- [ ] `RerankingRanker(Ranker)` composing first stage → candidate_k → reranker → top_k
- [ ] Chunk-level scoring with max aggregation
- [ ] Model: `cross-encoder/ms-marco-MiniLM-L-6-v2` (optionally compare `BAAI/bge-reranker-base`), with a pinned revision
- [ ] A latency budget written down **before** measuring
- [ ] Separate stage timings, with model load excluded and warm-up runs; report p50 and p95
- [ ] A four-stage table: BM25 / Semantic / RRF / RRF + rerank, with NDCG@5, RR@5, P@5, R@5, latency and candidates reranked
- [ ] Recall@candidate_k as the ceiling diagnostic
- [ ] candidate_k sweep over {10, 20, 30, 50}, plotted as NDCG@5 against p95 latency
- [ ] Regression gate with RRF as baseline and RRF + rerank as candidate
- [ ] Tests with a fake cross-encoder
- **Done when:**
  - [ ] "Does reranking pay for its latency?" is answered with numbers

### 3.6 Filters and diversity

- [ ] Metadata filters (section, Kubernetes version)
- [ ] Near-duplicate removal
- [ ] A cap on chunks per document in the top results
- **Done when:**
  - [ ] Dev metrics show no regression
  - [ ] The top 5 contains no duplicate content

---

## Phase 4: Generation

### 4.1 LLM provider abstraction

- [ ] One interface with a real provider implementation and a fake for tests
- [ ] Timeouts, retries and token counting
- **Done when:**
  - [ ] The whole pipeline runs in tests with no network

### 4.2 Prompt construction and citations

- [ ] Fit the retrieved chunks into a token budget
- [ ] Number the sources in the prompt
- [ ] Require inline citations (`[2]`) that map to chunk IDs and URLs
- [ ] Treat document text as untrusted data, not instructions
- **Done when:**
  - [ ] Every answer's citations resolve to real chunks

### 4.3 Abstention

- [ ] Below a reranker-score threshold tuned on dev, answer "not found in the documentation"
- **Done when:**
  - [ ] Unanswerable questions are refused at a measured rate without hurting answerable ones

### 4.4 Answer evaluation

- [ ] Correctness against the reference answer
- [ ] Groundedness: every claim is supported by the cited text
- [ ] Citation precision and recall
- [ ] Abstention accuracy
- [ ] An LLM judge, calibrated against 50 hand-labelled answers (report the agreement rate)
- **Done when:**
  - [ ] An end-to-end results table exists for generation

---

## Phase 5: Service

### 5.1 API

- [ ] FastAPI with `/ingest`, `/search` and `/ask`
- [ ] Pydantic request/response schemas and consistent error responses
- **Done when:**
  - [ ] The OpenAPI docs work
  - [ ] Integration tests run against a test database

### 5.2 Packaging

- [ ] Multi-stage Dockerfile and Docker Compose (API + Postgres)
- [ ] Health and readiness endpoints
- [ ] Models loaded once at startup
- **Done when:**
  - [ ] `docker compose up` gives a working system from a clean clone

### 5.3 Security basics

- [ ] API-key authentication
- [ ] Rate limiting
- [ ] Input size limits
- [ ] Secrets from environment variables, never committed
- [ ] A test where a document contains injected instructions and the system ignores them
- **Done when:**
  - [ ] The README has a security section

---

## Phase 6: Observability and operations

### 6.1 Tracing and logs

- [ ] Structured JSON logs with request IDs
- [ ] OpenTelemetry spans per stage: BM25, vector, fusion, rerank, LLM
- **Done when:**
  - [ ] One request's trace shows a per-stage time breakdown

### 6.2 Metrics and cost

- [ ] Prometheus metrics: p50/p95 per stage, tokens and cost per request, abstention rate, error rate
- [ ] A Grafana dashboard
- **Done when:**
  - [ ] There's a dashboard screenshot in the README

### 6.3 Load testing

- [ ] Run `k6` or Locust against `/ask` with a stated latency budget
- **Done when:**
  - [ ] The throughput at which p95 breaks the budget is documented

### 6.4 Resilience

- [ ] Query-embedding and answer caches
- [ ] Timeouts at every stage
- [ ] Fallbacks: reranker down → RRF only; LLM down → return search results
- **Done when:**
  - [ ] Tests that kill each dependency show the system degrades without failing

### 6.5 Quality gate in CI

- [ ] Run the retrieval evaluation on dev for every PR, using `check_regression`
- **Done when:**
  - [ ] A PR that lowers NDCG@5 beyond tolerance fails CI

---

## Phase 7: Showcase

### 7.1 Documentation

- [ ] Architecture diagram
- [ ] Results tables for every stage
- [ ] Short design-decision records: RRF, chunk size, embedding model, reranker cutoff

### 7.2 Demo

- [ ] A Streamlit UI or CLI showing the answer, its citations and the per-stage timings

### 7.3 Write-up

- [ ] A blog post, "What actually moved NDCG on real docs, and what didn't", linked from the README and resume
