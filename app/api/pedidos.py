from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate, PedidoResponse, StatusUpdate
from app.services.pedido_service import PedidoNaoEncontrado, PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


def get_service(db: Session = Depends(get_db)) -> PedidoService:
    return PedidoService(PedidoRepository(db))


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate, service: PedidoService = Depends(get_service)):
    return service.criar_pedido(dados)


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(service: PedidoService = Depends(get_service)):
    return service.listar_pedidos()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(pedido_id: int, service: PedidoService = Depends(get_service)):
    try:
        return service.buscar_pedido(pedido_id)
    except PedidoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status(pedido_id: int, dados: StatusUpdate, service: PedidoService = Depends(get_service)):
    try:
        return service.alterar_status(pedido_id, dados.status)
    except PedidoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
