# EconoCausal Project Architecture

## Project goal
EconoCausal aims to estimate the effects of dynamic-pricing interventions using causal machine learning, validate causal assumptions, and support budget allocation decisions.

## Planned flow
1. React/Plotly frontend collects inputs and displays results.
2. FastAPI backend validates requests and coordinates services.
3. Data preparation validates and prepares the dataset.
4. EconML estimates treatment effects using Double Machine Learning.
5. DoWhy supports causal validation and robustness/refutation checks.
6. SciPy optimizes budget allocation subject to defined constraints.
7. The backend returns structured results to the dashboard.

## Technology stack
- Python
- EconML
- DoWhy
- SciPy
- FastAPI
- React
- Plotly
- Pytest
- Git and GitHub

## Status
This document describes the proposed architecture. Individual modules are not yet implemented.
