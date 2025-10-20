from fastapi import FastAPI
from src.core.config import settings
from src.api.routes import ocr

app = FastAPI(title=settings.app_name)

# Incluir routers
app.include_router(ocr.router)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}"}


@app.get("/health")
async def health():
    return {"status": "ok"}