# EconoCausal: Dynamic Pricing via Double Machine Learning

EconoCausal is a project intended to estimate the effects of dynamic-pricing interventions using causal machine learning, validate causal assumptions, and support budget allocation decisions.

## Planned technology stack
- Python
- EconML
- DoWhy
- SciPy
- FastAPI
- React
- Plotly
- Pytest

## Repository structure
- `backend/` — FastAPI backend
- `causal_inference/` — causal-effect estimation
- `optimization/` — budget optimization
- `frontend/` — React/Plotly dashboard
- `tests/` — automated tests
- `docs/` — architecture and project documentation

## Initial setup
Create and activate a Python virtual environment, then install the backend dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the initial backend dependencies:

```bash
python -m pip install fastapi "uvicorn[standard]"
```

Run the API from the repository root:

```bash
uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to view the interactive API documentation.

## Current status
The repository contains the initial project structure and a minimal FastAPI health-check application. The causal inference, validation, optimization, and frontend modules are planned but not yet implemented.
