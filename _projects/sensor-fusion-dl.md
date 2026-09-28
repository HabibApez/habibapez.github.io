---
title: "Sensor Fusion with Deep Learning"
excerpt: "Planned study of multimodal radar-camera fusion using deep learning for ADAS applications."
tech_stack:
  - Python
  - PyTorch
  - Radar
  - Camera Fusion
thumbnail: /assets/images/projects-fusion.svg
github_repo:
order: 1
phase: planned
status: "Planned"
last_updated: "September 2026"
---

## Problem Statement

Single-sensor perception pipelines can fail in corner cases. This project studies radar-camera fusion to improve robustness for object understanding in adverse environments.

## Planned Methodology

1. Align radar and camera streams with timestamp synchronization.
2. Encode each modality with dedicated neural backbones.
3. Fuse feature maps using attention or concatenation baselines.
4. Evaluate detection quality under weather and low-light subsets.

## Proposed System

![Sensor fusion overview]({{ '/assets/images/projects-fusion.svg' | relative_url }})

## Evaluation Plan

- Compare camera-only, radar-only, and fused baselines on identical splits.
- Report mAP, precision and recall by environmental condition, and per-frame latency.
- Include ablation studies and representative synchronization or sensor-failure cases.
- Publish code, data provenance, and reproducible experiments when implementation begins.

> This is a project roadmap. No implementation or measured results are published yet.
