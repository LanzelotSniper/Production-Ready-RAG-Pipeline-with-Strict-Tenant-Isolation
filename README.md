# Production-Ready RAG Pipeline with Strict Tenant Isolation

> Enterprise-grade Retrieval-Augmented Generation architecture with physical per-tenant isolation — built for compliance-sensitive industries (Legal, Biopharma, Finance).

![Metrics Dashboard](docs/visuals/metrics_dashboard.png)

---

## What This Project Demonstrates

This repository is a clean, abstracted reference implementation of a production RAG architecture I design and build for real enterprise clients. It covers the full stack from secure document ingestion to grounded LLM inference — with a focus on **strict data isolation**, regulatory compliance, and operational reliability.

> **IP Notice:** To protect GDPR compliance, client confidentiality, and proprietary business logic of active startup projects, this repo uses public mock data (e.g., Wikipedia articles) and simplified local deployments. The architecture patterns, design decisions, and infrastructure blueprints are production-equivalent.

---

## Architecture Highlights

- **Physical tenant isolation** — dedicated VPC, S3 bucket, Aurora cluster, and Vector DB instance per customer. No shared runtime. No cross-tenant query risk.
- **Compliance-by-design** — meets GDPR Art. 32, data residency requirements, and professional secrecy standards (e.g., Art. 203 StGB for legal clients).
- **Full RAG pipeline** — token-aware chunking, embedding generation (SentenceTransformers / E5), HNSW vector search (Qdrant / Weaviate), RBAC-enforced retrieval via Aurora PostgreSQL.
- **Production deployment target** — AWS (eu-central-1), EC2 GPU/CPU inference, KMS-encrypted storage, ALB / API Gateway ingress.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud | AWS (VPC, EC2, S3, Aurora PostgreSQL, KMS, ALB) |
| Vector DB | Qdrant / Weaviate (HNSW, cosine similarity) |
| Embeddings | SentenceTransformers, E5 models |
| Metadata / RBAC | Amazon Aurora PostgreSQL |
| Ingestion | Python async worker (Docker on EC2) |
| Chunking | Token-aware (256–1024 tokens, 10–20% overlap) |
| CI/CD | GitLab pipelines (per-customer infra, deterministic) |

---

## Documentation

| Document | Description |
|---|---|
| [Architecture: Dedicated RAG per Customer](docs/architecture-dedicated-rag.md) | Full architecture narrative, component breakdown, security model, and Mermaid infrastructure diagram |
| [AI-Assisted Development Workflow](docs/ai-assisted-development-workflow.md) | The systematic methodology behind this build — TDD, Plan Mode, context isolation, and competitive benchmark data |
| [AI Development Metrics](docs/ai_dev_metrics.md) | Raw session metrics, output velocity benchmarks, and cost-efficiency analysis with visual charts |

---

## Development Approach

This project was built using a **human-in-the-loop, serially orchestrated AI workflow** — not vibe-coded, not copy-pasted. Every line was reviewed, understood, and committed intentionally.

![Competitive Benchmark](docs/visuals/competitive_benchmark.png)

| Metric | Value |
|---|---|
| Active development time | 20.9 hours |
| Total tokens processed | 153,525,739 |
| Output velocity | ~2,512 LOC / hour (Top 0.01% globally) |
| Code retention rate | ~99% (production-ready on first pass) |
| AI compute cost | ~$60 / month |
| Extrapolated monthly output | ~231,000 LOC / month |

The methodology — TDD-first, Plan Mode architecture, 1 chat per phase, deliberate tool routing — is documented in full in the [AI-Assisted Development Workflow](docs/ai-assisted-development-workflow.md).

---

## Why Physical Isolation Over Logical Multi-Tenancy

Most RAG SaaS products use logical isolation: shared infrastructure, row-level filtering, namespace prefixes. This is fast to build and cheap to operate — but it fails the threat model of regulated industries:

- A single query bug can leak embeddings across tenants
- Shared vector indexes make timing-based inference attacks feasible
- Compliance auditors cannot verify isolation without inspecting application code

This architecture eliminates the entire class of cross-tenant risk by making it physically impossible — each customer is a fully independent system boundary.
