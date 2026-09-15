from fastapi import FastAPI

app = FastAPI(title="MoonInsight", version="0.1.0")


@app.get("/api/hello")
def hello() -> dict[str, str]:
    return {"message": "Hello from MoonInsight backend"}
