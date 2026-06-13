import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from database.engine import create_tables
from config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("clube_do_gole")

settings = get_settings()

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    from services.scheduler import iniciar_scheduler
    await create_tables()
    iniciar_scheduler()
    if not settings.admin_senha_segura:
        logger.warning("⚠️  ADMIN_SENHA_INICIAL ainda é o valor padrão inseguro. Troque em backend/.env antes de ir para produção.")
    if not settings.mp_configured:
        logger.info("ℹ️  Mercado Pago não configurado — pagamentos aprovados automaticamente (modo dev).")
    yield

app = FastAPI(title="Clube do Gole API", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.produtos import router as produtos_router
from routes.carrinho import router as carrinho_router
from routes.cupons import router as cupons_router
from routes.configuracoes import router as configuracoes_router
from routes.assinaturas import router as assinaturas_router
from routes.pagamentos import router as pagamentos_router
from routes.estoque import router as estoque_router

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(produtos_router)
app.include_router(carrinho_router)
app.include_router(cupons_router)
app.include_router(configuracoes_router)
app.include_router(assinaturas_router)
app.include_router(pagamentos_router)
app.include_router(estoque_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=settings.host, port=settings.port, reload=True)