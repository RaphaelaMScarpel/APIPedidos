import enum

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String, func

from app.database import Base


class StatusPedido(str, enum.Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String(120), nullable=False)
    produto = Column(String(120), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(10, 2), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    status = Column(Enum(StatusPedido, native_enum=False), nullable=False, default=StatusPedido.CRIADO)
    data_criacao = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
