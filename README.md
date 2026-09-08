# NPET-backend

Backend da aplicação **NPET** — plataforma que conecta doadores a ONGs e instituições de proteção animal.

> **Estado atual:** o único entregável funcional é a **autenticação por login** (e-mail + senha), validada contra credenciais hardcoded que simulam o banco de dados. Cadastro de usuário, ONGs, doações e necessidades ainda não foram implementados.

## Stack

- **Python 3.10+** (testado com 3.11.9)
- **FastAPI** `0.115.6`
- **Uvicorn** `0.34.0` (servidor ASGI, com hot-reload)
- **Pydantic** `2.10.4` / **Pydantic Settings** `2.7.1`
- **python-dotenv** `1.0.1`
- **email-validator** `2.2.0`

## Arquitetura

O fluxo de requisição atravessa três camadas:

```
HTTP → Router (Controller) → Service (regra) → Repository (dados) → "banco" (fake_db.py)
```

- **Router**: expõe os endpoints HTTP. Recebe o DTO já validado e chama o Service.
- **Schema**: `LoginRequest`/`LoginResponse` — valida entrada e formata saída.
- **Service**: regra de negócio (autenticação). Não conhece HTTP nem onde os dados estão.
- **Repository**: única camada que sabe onde os dados moram. Hoje consulta uma lista hardcoded; quando o banco real entrar, só este arquivo muda.
- **Fake DB**: lista Python simulando a tabela de credenciais.

O módulo `auth/` tem dois fluxos idênticos, um por tipo de autenticação:

| Tipo | Rota | Camadas |
|---|---|---|
| Usuário (doador) | `POST /api/v1/auth/login` | `app/modules/auth/usuarios/` |
| Instituição | `POST /api/v1/institutions/auth/login` | `app/modules/auth/instituicoes/` |

## Estrutura de diretórios

```
NPET-backend/
├── app/
│   ├── main.py                  # cria o app FastAPI, CORS, handler de erros
│   ├── core/
│   │   ├── config.py            # configuração global (lê o .env)
│   │   └── exceptions.py        # AppError / UnauthorizedError (401)
│   ├── api/
│   │   └── router.py            # junta os routers (health + auth)
│   ├── health/
│   │   └── router.py            # GET /health
│   └── modules/
│       └── auth/
│           ├── usuarios/        # POST /auth/login
│           │   ├── fake_db.py       # credencial hardcoded (usuário)
│           │   ├── repository.py    # consulta o fake_db
│           │   ├── schemas.py       # LoginRequest / LoginResponse
│           │   ├── service.py       # regra de autenticação
│           │   └── router.py        # rotas HTTP
│           └── instituicoes/    # POST /institutions/auth/login
│               ├── fake_db.py
│               ├── repository.py
│               ├── schemas.py
│               ├── service.py
│               └── router.py
├── .env.example                 # modelo de variáveis de ambiente
├── .gitignore
├── requirements.txt
├── RUN.md                       # como rodar (resumido)
└── STARTUP.md                   # guia de construção detalhado
```

## Como rodar (modo desenvolvimento)

Pré-requisito: **Python 3.10+**.

**1. Criar e ativar o ambiente virtual**

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat
```

> Se o PowerShell recusar rodar `Activate.ps1` (erro de "execution policy"), use o `activate.bat` pelo CMD, ou chame os executáveis de dentro de `.venv\Scripts\` diretamente, sem ativar (ex.: `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`).

**2. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**3. Configurar variáveis de ambiente**

```bash
copy .env.example .env
```

**4. Rodar a aplicação com hot-reload**

```bash
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`.

## Documentação automática

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Healthcheck: `http://localhost:8000/api/v1/health`

## Testando o login

**Credenciais de teste** (ver `fake_db.py` de cada módulo):

- Usuário: `admin@npet.org` / `npet123`
- Instituição: `contato@ufnpet.edu.br` / `npet123`

**Como usuário:**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"doador@email.com.br\", \"password\": \"senha123\"}"
```

**Como instituição:**

```bash
curl -X POST http://localhost:8000/api/v1/institutions/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"instituicao@email.com.br\", \"password\": \"senha123\"}"
```

**Respostas:**

- Credencial certa → `200` com `{"success": true, "message": "Autenticação realizada com sucesso."}`
- Credencial errada ou e-mail inexistente → `401` com `{"detail": "E-mail ou senha inválidos."}`
- E-mail mal formatado ou senha vazia → `422` (erro de validação do schema)

## Próximos passos

- Trocar `fake_db.py` por um banco real (ex.: PostgreSQL + SQLAlchemy). Só o `repository.py` muda.
- Hash de senha (bcrypt/argon2) em vez de comparação em texto puro.
- Gerar/validar um token real (JWT) em vez de só devolver mensagem de sucesso.
- Introduzir os demais domínios (usuários, instituições, doações, necessidades).

## Documentação adicional

- [RUN.md](./RUN.md) — guia rápido de execução
- [STARTUP.md](./STARTUP.md) — guia detalhado da arquitetura atual
