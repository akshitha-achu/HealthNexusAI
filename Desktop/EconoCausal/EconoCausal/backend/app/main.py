from fastapi import FastAPI

app = FastAPI(
    title="EconoCausal API",
    description="Backend for causal effect estimation and dynamic pricing budget optimization",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "project": "EconoCausal",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
