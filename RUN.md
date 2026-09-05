# Como rodar o backend NPET (modo desenvolvimento)

Pré-requisito: **Python 3.10+** (testado com 3.11.9).

## 1. Criar e ativar o ambiente virtual:

```bash
# criar
python -m venv .venv

# ativar (Windows - PowerShell)
.venv\Scripts\Activate.ps1

# ativar (Windows - CMD)
.venv\Scripts\activate.bat

# ativar (Linux / Mac)
source .venv/bin/activate
```

> Se o PowerShell recusar rodar `Activate.ps1` (erro de "execution policy"),
> use o `activate.bat` pelo CMD, ou simplesmente chame os executáveis de
> dentro de `.venv\Scripts\` diretamente, sem ativar (ex.:
> `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`).

## 2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

## 3. Configurar variáveis de ambiente:

```bash
# Windows
copy .env.example .env
```

## 4. Rodar a aplicação com hot-reload:

```bash
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`.

## 5. Acessar a documentação automática (Swagger):

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Healthcheck: http://localhost:8000/api/v1/health

## 6. Testar o login:

Credencial hardcoded (ver [app/modules/auth/fake_db.py](app/modules/auth/fake_db.py)):

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@npet.org\", \"password\": \"npet123\"}"
```
