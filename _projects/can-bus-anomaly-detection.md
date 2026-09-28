---
title: "CAN Bus Anomaly Detection"
excerpt: "Planned investigation of deep learning-based intrusion detection for automotive CAN bus networks."
tech_stack:
  - Python
  - LSTM
  - Autoencoder
  - Cybersecurity
thumbnail: /assets/images/projects-can.svg
github_repo:
order: 4
phase: planned
status: "Planned"
last_updated: "September 2026"
---

## Problem Statement

Automotive CAN communication lacks native encryption and authentication, making in-vehicle networks vulnerable to spoofing and injection attacks. This project targets data-driven anomaly detection for early security event identification.

## Planned Methodology

1. Parse CAN frames and engineer time-sequence features.
2. Train sequence models (LSTM and autoencoder baselines).
3. Detect anomalies via reconstruction error and thresholding.
4. Compare precision-recall under simulated attack patterns.

## Proposed System

![CAN anomaly detection overview]({{ '/assets/images/projects-can.svg' | relative_url }})

## Evaluation Plan

- Compare LSTM and autoencoder baselines on the same time-based split.
- Report precision, recall, F1-score, and false-positive rate by attack type.
- Document threshold calibration and performance on previously unseen attack traces.
- Publish code, data provenance, and reproducible experiments when implementation begins.

> This is a project roadmap. No implementation or measured results are published yet.
