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

O módulo `auth/` tem dois percursos **idênticos**, um por tipo de quem
autentica: `usuarios/` (`POST /auth/login`) e `instituicoes/`
(`POST /institutions/auth/login`). Ambos têm as mesmas camadas:

- **Router** ([usuarios/router.py](app/modules/auth/usuarios/router.py) · [instituicoes/router.py](app/modules/auth/instituicoes/router.py)): expõe o `POST .../login`. Só cuida de HTTP. Recebe o DTO já validado, chama o Service, devolve a resposta.

- **Schema** ([usuarios/schemas.py](app/modules/auth/usuarios/schemas.py) · [instituicoes/schemas.py](app/modules/auth/instituicoes/schemas.py)): `LoginRequest` valida o formato das credenciais de entrada (e-mail válido, senha não vazia) antes de qualquer regra de negócio rodar. `LoginResponse` é o formato de saída.

- **Service** ([usuarios/service.py](app/modules/auth/usuarios/service.py) · [instituicoes/service.py](app/modules/auth/instituicoes/service.py)): a regra de negócio. Pergunta ao Repository se a credencial existe e bate a senha. Não conhece HTTP nem sabe onde os dados estão guardados. Lança `UnauthorizedError` se a autenticação falhar.

- **Repository** ([usuarios/repository.py](app/modules/auth/usuarios/repository.py) · [instituicoes/repository.py](app/modules/auth/instituicoes/repository.py)): a única camada que sabe *onde* os dados moram. Hoje consulta uma lista hardcoded; quando o banco entrar, só este arquivo muda.

- **"Banco" fake** ([usuarios/fake_db.py](app/modules/auth/usuarios/fake_db.py) · [instituicoes/fake_db.py](app/modules/auth/instituicoes/fake_db.py)): um arquivo com uma lista Python simulando a tabela de credenciais. Credenciais de teste: usuário `admin@npet.org` / `npet123`; instituição `contato@ufnpet.edu.br` / `npet123`.

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
¦ │           ├── usuarios/        # POST /auth/login                           ¦
¦ │           │   ├── fake_db.py       # credencial hardcoded (usuário)         ¦
¦ │           │   ├── repository.py    # consulta o fake_db                     ¦
¦ │           │   ├── schemas.py       # LoginRequest / LoginResponse           ¦
¦ │           │   ├── service.py       # regra de autenticação                  ¦
¦ │           │   └── router.py        # rotas HTTP                             ¦
¦ │           └── instituicoes/    # POST /institutions/auth/login              ¦
¦ │               ├── fake_db.py       # credencial hardcoded (instituição)     ¦
¦ │               ├── repository.py    # consulta o fake_db                     ¦
¦ │               ├── schemas.py       # LoginRequest / LoginResponse           ¦
¦ │               ├── service.py       # regra de autenticação                  ¦
¦ │               └── router.py        # rotas HTTP                             ¦
¦ ├── .env.example                 # modelo de variáveis de ambiente            ¦
¦ ├── .gitignore                                                                ¦
¦ ├── requirements.txt                                                          ¦
¦ ├── RUN.md                       # como rodar (resumido)                      ¦
¦ └── STARTUP.md                   # este arquivo                               ¦
+-------------------------------------------------------------------------------+
```

## 3. Testando o fluxo

Como **usuário**:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@npet.org\", \"password\": \"npet123\"}"
```

Como **instituição** (mesmo contrato, outra rota):

```bash
curl -X POST http://localhost:8000/api/v1/institutions/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"contato@email.com.br\", \"password\": \"senha123\"}"
```

- Credencial certa → `200` com `{"success": true, "message": "Autenticação realizada com sucesso."}`.
- Credencial errada ou e-mail inexistente → `401` com `{"detail": "E-mail ou senha inválidos."}`.
- E-mail mal formatado ou senha vazia → `422` (erro de validação do schema, antes mesmo de chegar no Service).

## 4. Próximos passos:

- Trocar `fake_db.py` por um banco real (ex.: PostgreSQL + SQLAlchemy). Só o `repository.py` muda.
- Hash de senha (bcrypt/argon2) em vez de comparação em texto puro.
- Gerar/validar um token real (JWT) em vez de só devolver uma mensagem de sucesso.
- Introduzir os demais domínios (usuários, instituições, doações, necessidades) quando entrarem no escopo do sprint.
