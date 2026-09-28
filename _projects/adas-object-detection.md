---
title: "ADAS Object Detection with YOLOv8"
excerpt: "Planned study of real-time object detection for driving scenarios, connecting radar experience with deep learning."
tech_stack:
  - Python
  - YOLOv8
  - OpenCV
  - Computer Vision
thumbnail: /assets/images/projects-yolo.svg
github_repo:
order: 3
phase: planned
status: "Planned"
last_updated: "September 2026"
---

## Problem Statement

Modern ADAS stacks require reliable object detection under changing weather, lighting, and traffic density. This project explores real-time detection tuned for driving contexts and links classic automotive perception constraints with deep learning workflows.

## Planned Methodology

1. Curate and preprocess automotive image/video datasets.
2. Fine-tune YOLOv8 variants for latency-accuracy tradeoffs.
3. Evaluate on precision, recall, mAP, and inference FPS.
4. Integrate OpenCV visualization and performance logging.

## Proposed System

![ADAS object detection overview]({{ '/assets/images/projects-yolo.svg' | relative_url }})

## Evaluation Plan

- Report mAP@0.5, mAP@0.5:0.95, inference latency, and FPS.
- Compare at least one pretrained baseline with a fine-tuned model.
- Break down results across urban daytime and low-light subsets.
- Publish code, environment details, and representative failure cases when the implementation is ready.

> This is a project roadmap. No implementation or measured results are published yet.
