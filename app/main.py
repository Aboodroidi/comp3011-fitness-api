from fastapi import FastAPI

app = FastAPI(
    title="COMP3011 Fitness API",
    version="0.1.0",
    description="Fitness workout logging + analytics API (CRUD + insights).",
)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}