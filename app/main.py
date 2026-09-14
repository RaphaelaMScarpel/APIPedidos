from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health, pedidos
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # cria a tabela no primeiro start, se ainda nao existir
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de Pedidos", lifespan=lifespan)

app.include_router(health.router)
app.include_router(pedidos.router)
