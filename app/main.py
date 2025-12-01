from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.database import engine, Base

from app.routers import auth, mock, admin


app = FastAPI(title="Система аккаунтов", 
              description="Система авторизации и аутентификации", 
              docs_url=None,
              redoc_url=None,
              openapi_url=None
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Документация")

@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

app.include_router(auth.router)
app.include_router(mock.router)
app.include_router(admin.router)

# health-check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}