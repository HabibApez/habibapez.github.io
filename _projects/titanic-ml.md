---
title: "Titanic Survival Prediction with Classical ML"
excerpt: "End-to-end Titanic dataset workflow: EDA, feature engineering, and baseline model benchmarking in Python."
tech_stack:
  - Python
  - pandas
  - scikit-learn
  - seaborn
  - matplotlib
  - Logistic Regression
  - Naive Bayes
thumbnail: /assets/images/projects-titanic.png
github_repo: https://github.com/HabibApez/titanic-ml
order: 2
phase: completed

status: "Baseline Complete"
last_updated: "September 2026"
---

## Problem Statement

This project explores binary classification for passenger survival prediction on the Titanic dataset. The goal is to build a clear and reproducible ML baseline covering data understanding, preprocessing, and side-by-side model comparison.

## Methodology and Approach

1. Load and inspect dataset structure and class balance.
2. Perform exploratory visual analysis for class, family features, age, and fare distributions.
3. Preprocess features by dropping low-value columns, imputing missing age values, and encoding categorical sex data.
4. Train and compare multiple classical models on the same train/test split.

## System Overview

- Dataset: `titanic.csv`
- Train/test split: 80/20 (`random_state=10`)
- Features: `Pclass`, `Age`, `SibSp`, `Parch`, `Fare`, `IsMale`
- Target: `Survived`
- Models: `LogisticRegression`, `GaussianNB`, `MultinomialNB`

## Results and Metrics

- Implemented confusion matrix, classification report, and accuracy scoring for each model.
- Added automatic best-model selection based on test accuracy.
- Outcome: a complete, interpretable baseline suitable for future extensions such as cross-validation, ROC-AUC, and model persistence.

![Confusion matrices comparing the Titanic classification models]({{ '/assets/images/projects-titanic.png' | relative_url }})

## Code Snippet

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
```

## Repository

- GitHub: [Titanic ML](https://github.com/HabibApez/titanic-ml)
- Note: This implementation is intentionally single-script and learning-focused, with a roadmap for modularization and stronger evaluation.
