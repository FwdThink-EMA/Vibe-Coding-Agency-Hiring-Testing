# Cloud Test

This test focuses on your ability to design a secure, scalable cloud architecture capable of enabling retrieval‑augmented generation (RAG) for enterprise knowledge access.

The scenario is described in **Cloud Architect Problem.docx**. Refer to it for full context. fileciteturn1file0

---

## Objective

Design a **cloud-based RAG system** that:
- Ingests and indexes 10+ years of organizational documents.
- Allows employees to query using natural language.
- Returns relevant responses with **source citations**.
- Maintains strong access control and data protection.
- Meets cost, performance, and uptime constraints.

---

## What Your Submission Must Include

Submit a **single PDF** named:

```
submission/cloud-test.pdf
```

Your PDF must contain the following clearly labeled sections:

### 1. Assumptions
List any assumptions about:
- Document volume
- Update frequency
- User access patterns
- Tech stack familiarity

### 2. High-Level Architecture (Required Diagram)
Show end‑to‑end data flow:
- Document ingestion → preprocessing → embedding → vector store
- Query → retrieval → context → generation → user interface

A simple, readable diagram is preferred over a complex one.

### 3. Ingestion and Indexing Pipeline
Describe how documents are:
- Collected
- Converted (OCR if applicable)
- Chunked and embedded
- Stored in vector search

### 4. RAG Retrieval + Response Logic
Explain your retrieval strategy:
- Embedding model choice
- Vector DB choice
- k‑value selection
- Re‑ranking or filtering rules
- How citations are attached

### 5. User Interface + Application Layer
Briefly describe:
- Front-end experience (chat interaction model)
- Backend services
- API gateway or routing layer

### 6. Security Architecture (Required Diagram)
Address:
- Authentication (employee-only access)
- Authorization (document-level permissions)
- Encryption and key storage
- Audit logging and monitoring
- Network segmentation / private endpoints

### 7. Scaling Strategy
How to support:
- Growth in document volume
- 500+ concurrent users
- Performance under load

### 8. Cost Strategy 
Provide a cost‑conscious breakdown:
- Where to reserve capacity
- Where to auto‑scale
- Where to use managed services vs. shared compute

### 9. Risks, Tradeoffs, and Alternatives
Call out:
- What your design optimizes for
- What you intentionally deprioritized and why
- Future improvements

---

## Submission Requirements

- Deliverable must be **one PDF**, not multiple files.
- **All diagrams must be embedded** directly in the PDF.
- No external links to Lucidchart, Figma, Google Drive, etc.
- Keep wording clear and concise.

---

## Evaluation Criteria

| Category | Weight | Description |
|---------|--------|-------------|
| Architecture Clarity | High | Logical, understandable end‑to‑end design |
| Security & Access Control | High | Protect data and enforce permissions correctly |
| RAG Retrieval Quality | Medium | Clear, justified retrieval + citation strategy |
| Scalability & Reliability | Medium | Meets concurrency and growth requirements |
| Cost Awareness | Medium | Realistic monthly estimate + cost controls |
| Communication Quality | Medium | Organized, readable, and professional explanation |

---

Clarity and reasoning matter more than complexity.

