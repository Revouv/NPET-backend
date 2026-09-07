"""
Simula a tabela de credenciais do banco de dados.

Nesta fase não há banco real: os dados moram hardcoded aqui, num único lugar. O Repository é o único componente que enxerga este arquivo. Service e Router não sabem (nem precisam saber) que o "banco" é, por enquanto, uma lista em memória.
Quando o banco entrar de verdade, este arquivo é apagado e o Repository passa a consultar a tabela real, sem que Service/Router mudem uma linha.
"""

FAKE_CREDENTIALS_DB: list[dict[str, str]] = [
    {"email": "admin@npet.org", "password": "npet123"},
]
