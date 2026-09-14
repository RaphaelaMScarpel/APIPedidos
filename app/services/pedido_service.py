from decimal import ROUND_HALF_UP, Decimal

from app.models.pedido import Pedido, StatusPedido
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate

CENTAVOS = Decimal("0.01")


class PedidoNaoEncontrado(Exception):
    pass


class PedidoService:
    def __init__(self, repository: PedidoRepository):
        self.repository = repository

    def criar_pedido(self, dados: PedidoCreate) -> Pedido:
        # Decimal evita erro de arredondamento do float (ex: 0.1 * 3)
        valor_unitario = Decimal(str(dados.valor_unitario)).quantize(CENTAVOS, ROUND_HALF_UP)
        valor_total = (valor_unitario * dados.quantidade).quantize(CENTAVOS, ROUND_HALF_UP)

        pedido = Pedido(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            status=StatusPedido.CRIADO,
        )
        return self.repository.salvar(pedido)

    def buscar_pedido(self, pedido_id: int) -> Pedido:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontrado(pedido_id)
        return pedido

    def listar_pedidos(self) -> list[Pedido]:
        return self.repository.listar()

    def alterar_status(self, pedido_id: int, novo_status: StatusPedido) -> Pedido:
        pedido = self.buscar_pedido(pedido_id)
        pedido.status = novo_status
        return self.repository.salvar(pedido)
