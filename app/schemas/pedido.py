from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.pedido import StatusPedido


class PedidoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cliente: str = Field(min_length=1, max_length=120)
    produto: str = Field(min_length=1, max_length=120)
    quantidade: int = Field(gt=0)
    valor_unitario: float = Field(gt=0)


class StatusUpdate(BaseModel):
    status: StatusPedido


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    status: StatusPedido
    data_criacao: datetime
