---
title: "LLM Agent for Automotive Compliance (Expedition 26)"
excerpt: "Planned LangChain-based assistant for traceable automotive compliance queries involving ISO 26262 and ISO 21434."
tech_stack:
  - Python
  - LangChain
  - LLMs
  - RAG
thumbnail: /assets/images/projects-llm.svg
github_repo:
order: 2
phase: planned
status: "Planned"
last_updated: "September 2026"
---

## Problem Statement

Engineering teams spend significant time navigating lengthy safety and cybersecurity standards. This project explores an LLM retrieval workflow to answer compliance queries with traceable references.

## Planned Methodology

1. Ingest ISO-related documentation and chunk semantically.
2. Build vector index and retrieval pipeline.
3. Use prompt templates for constrained, citation-first outputs.
4. Evaluate relevance, factual grounding, and response latency.

## Proposed System

![LLM compliance workflow overview]({{ '/assets/images/projects-llm.svg' | relative_url }})

## Evaluation Plan

- Build an expert-reviewed evaluation set that does not redistribute protected standards text.
- Measure grounded-answer rate, citation coverage, retrieval relevance, and response latency.
- Record unsupported-answer and abstention behavior rather than relying on demonstration examples alone.
- Publish code and a legally shareable sample corpus when implementation begins.

> This is a project roadmap. No implementation or measured results are published yet.
