# NPET Backend — Guia de Construção (passo a passo)

Este documento explica, de forma simples, o que existe hoje no backend do
NPET e por quê.

> **Estado atual:** o único entregável funcional é a **autenticação por login** (e-mail + senha), validada contra uma credencial **hardcoded** que simula o banco de dados. Tudo o mais (cadastro de usuário, ONGs, doações, necessidades) foi deliberadamente deixado de fora até este escopo estar fechado com a entrega.

---

## 1. Arquitetura em 3 camadas:

O fluxo de login atravessa as camadas assim:

```
HTTP → Router (Controller) → Service (regra) → Repository (dados) → "banco" (fake_db.py)
       router.py             service.py        repository.py
```

- **Router** ([app/modules/auth/router.py](app/modules/auth/router.py)): expõe `POST /auth/login`. Só cuida de HTTP. Recebe o DTO já validado, chama o Service, devolve a resposta.

- **Schema** ([app/modules/auth/schemas.py](app/modules/auth/schemas.py)): `LoginRequest` valida o formato das credenciais de entrada (e-mail válido, senha não vazia) antes de qualquer regra de negócio rodar. `LoginResponse` é o formato de saída.

- **Service** ([app/modules/auth/service.py](app/modules/auth/service.py)): a regra de negócio. Pergunta ao Repository se a credencial existe e bate a senha. Não conhece HTTP nem sabe onde os dados estão guardados. Lança `UnauthorizedError` se a autenticação falhar.

- **Repository** ([app/modules/auth/repository.py](app/modules/auth/repository.py)): a única camada que sabe *onde* os dados moram. Hoje consulta uma lista hardcoded; quando o banco entrar, só este arquivo muda.

- **"Banco" fake** ([app/modules/auth/fake_db.py](app/modules/auth/fake_db.py)): um arquivo com uma lista Python simulando a tabela de credenciais. A credencial de teste é `admin@npet.org` / `ablubluble`.

## 2. Estrutura de diretórios:

```
+-------------------------------------------------------------------------------+
¦ NPET-backend/                                                                 ¦
¦ ├── app/                                                                      ¦
¦ │   ├── main.py                  # cria o app FastAPI, CORS, handler de erros ¦
¦ │   ├── core/                                                                 ¦
¦ │   │   ├── config.py            # configuração global (lê o .env)            ¦
¦ │   │   └── exceptions.py        # AppError / UnauthorizedError (401)         ¦
¦ │   ├── api/                                                                  ¦
¦ │   │   └── router.py            # junta os routers (health + auth)           ¦
¦ │   ├── health/                                                               ¦
¦ │   │   └── router.py            # GET /health                                ¦
¦ │   └── modules/                                                              ¦
¦ │       └── auth/                                                             ¦
¦ │           ├── fake_db.py       # credencial hardcoded ("banco" simulado)    ¦
¦ │           ├── repository.py    # consulta o fake_db                         ¦
¦ │           ├── schemas.py       # LoginRequest / LoginResponse               ¦
¦ │           ├── service.py       # regra de autenticação                      ¦
¦ │           └── router.py        # POST /auth/login                           ¦
¦ ├── .env.example                 # modelo de variáveis de ambiente            ¦
¦ ├── .gitignore                                                                ¦
¦ ├── requirements.txt                                                          ¦
¦ ├── RUN.md                       # como rodar (resumido)                      ¦
¦ └── STARTUP.md                   # este arquivo                               ¦
+-------------------------------------------------------------------------------+
```

## 3. Testando o fluxo

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@npet.org\", \"password\": \"npet123\"}"
```

- Credencial certa → `200` com `{"success": true, "message": "Autenticação realizada com sucesso."}`.
- Credencial errada ou e-mail inexistente → `401` com `{"detail": "E-mail ou senha inválidos."}`.
- E-mail mal formatado ou senha vazia → `422` (erro de validação do schema, antes mesmo de chegar no Service).

## 4. Próximos passos:

- Trocar `fake_db.py` por um banco real (ex.: PostgreSQL + SQLAlchemy). Só o `repository.py` muda.
- Hash de senha (bcrypt/argon2) em vez de comparação em texto puro.
- Gerar/validar um token real (JWT) em vez de só devolver uma mensagem de sucesso.
- Introduzir os demais domínios (usuários, instituições, doações, necessidades) quando entrarem no escopo do sprint.
