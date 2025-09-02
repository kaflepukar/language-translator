from fastapi import FastAPI

app = FastAPI(title="Language-Converter")


@app.get("/health", tags=["Health"])
async def health():
    return "okey"
