import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.engine import create_tables
from config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(title="Clube do Gole API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.produtos import router as produtos_router
from routes.carrinho import router as carrinho_router
from routes.cupons import router as cupons_router
from routes.configuracoes import router as configuracoes_router

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(produtos_router)
app.include_router(carrinho_router)
app.include_router(cupons_router)
app.include_router(configuracoes_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=settings.host, port=settings.port, reload=True)