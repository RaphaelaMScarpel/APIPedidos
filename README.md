# API de Pedidos

Trabalho 1 da disciplina de Desenvolvimento de Sistemas Distribuídos.

API REST para registro e consulta de pedidos, feita com FastAPI e PostgreSQL, executando em containers separados com Docker Compose.

## Integrante

| Nome completo | Turma | RA |
|---|---|---|
| Raphaela Mendes Scarpel | CC8Q13 | G8009A0 |

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Docker e Docker Compose

## Arquitetura

```
Cliente --HTTP/JSON--> pedidos (FastAPI) --protocolo PostgreSQL--> postgres
```

A aplicação é dividida em três camadas, todas no mesmo container:

- **API** (`app/api`): recebe as requisições HTTP e devolve as respostas.
- **Service** (`app/services`): regras de negócio, como o cálculo do `valor_total` e a definição do status inicial.
- **Repository** (`app/repositories`): acesso ao banco de dados.

O PostgreSQL roda em outro container, com volume persistente. Os dois se comunicam por uma rede interna do Docker e só a porta da API (8000) é publicada.

## Estrutura

```
app/
├── main.py
├── config.py
├── database.py
├── api/
│   ├── health.py
│   └── pedidos.py
├── services/
│   └── pedido_service.py
├── repositories/
│   └── pedido_repository.py
├── models/
│   └── pedido.py
└── schemas/
    └── pedido.py
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## Como executar

Pré-requisito: Docker com o plugin Docker Compose.

```bash
git clone https://github.com/RaphaelaMScarpel/APIPedidos.git
cd APIPedidos
git checkout APIPedidos-1-final
docker compose up -d --build
```

A API fica disponível em http://localhost:8000 e a documentação interativa em http://localhost:8000/docs.

A tabela é criada automaticamente quando a aplicação sobe. Não é preciso criar o arquivo `.env`: o `docker-compose.yml` já tem valores padrão. Para usar outras credenciais, copie `.env.example` para `.env` e altere os valores.

Para parar:

```bash
docker compose down
```

Para parar e apagar os dados do banco:

```bash
docker compose down -v
```

## Configuração

A conexão com o banco é lida da variável de ambiente `DATABASE_URL`, nada fica fixo no código.

| Variável | Padrão |
|---|---|
| `POSTGRES_USER` | `pedidos` |
| `POSTGRES_PASSWORD` | `pedidos` |
| `POSTGRES_DB` | `pedidos` |
| `DATABASE_URL` | `postgresql+psycopg2://pedidos:pedidos@postgres:5432/pedidos` |

## Modelo de Pedido

| Campo | Descrição |
|---|---|
| `id` | identificador do pedido |
| `cliente` | nome do cliente |
| `produto` | nome do produto |
| `quantidade` | quantidade solicitada (maior que zero) |
| `valor_unitario` | preço de uma unidade (maior que zero) |
| `valor_total` | `quantidade * valor_unitario`, calculado pela aplicação |
| `status` | `CRIADO`, `CONFIRMADO` ou `CANCELADO` |
| `data_criacao` | data e hora do registro |

## Endpoints

| Método | Rota | Descrição | Respostas |
|---|---|---|---|
| POST | `/pedidos` | cria um pedido | 201, 422 |
| GET | `/pedidos` | lista os pedidos | 200 |
| GET | `/pedidos/{id}` | consulta um pedido | 200, 404 |
| PATCH | `/pedidos/{id}/status` | altera o status | 200, 404, 422 |
| GET | `/health` | saúde da aplicação | 200 |

### Exemplos

Criar pedido:

```bash
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente": "Maria", "produto": "Teclado", "quantidade": 2, "valor_unitario": 150.00}'
```

```json
{
  "id": 1,
  "cliente": "Maria",
  "produto": "Teclado",
  "quantidade": 2,
  "valor_unitario": 150.0,
  "valor_total": 300.0,
  "status": "CRIADO",
  "data_criacao": "2026-09-15T14:00:00.000000Z"
}
```

Consultar pedido:

```bash
curl http://localhost:8000/pedidos/1
```

Listar pedidos:

```bash
curl http://localhost:8000/pedidos
```

Alterar status:

```bash
curl -X PATCH http://localhost:8000/pedidos/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "CONFIRMADO"}'
```

Health check:

```bash
curl http://localhost:8000/health
```

```json
{"status": "ok"}
```

## Persistência

Para testar que os pedidos continuam salvos depois de reiniciar a aplicação:

```bash
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente": "João", "produto": "Mouse", "quantidade": 1, "valor_unitario": 50}'

docker compose restart pedidos

curl http://localhost:8000/pedidos/1
```

O pedido continua lá porque ele não fica guardado na aplicação, e sim no PostgreSQL, que é outro container. Reiniciar o container `pedidos` não afeta o banco, e os arquivos do banco ficam no volume `postgres_data`, que só é apagado com `docker compose down -v`.
