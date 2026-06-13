import pytest


@pytest.mark.asyncio
async def test_cadastro_e_login(client):
    # Cadastro
    r = await client.post("/api/auth/cadastro", json={
        "nome": "Teste", "sobrenome": "User",
        "email": "teste@clubedogole.com",
        "senha": "senha123456",
        "cpf": None, "telefone": None, "data_nascimento": None,
    })
    assert r.status_code == 201, r.text
    data = r.json()
    assert "token" in data

    # Login correto
    r = await client.post("/api/auth/login", json={
        "email": "teste@clubedogole.com", "senha": "senha123456"
    })
    assert r.status_code == 200
    assert "token" in r.json()

    # Login senha errada
    r = await client.post("/api/auth/login", json={
        "email": "teste@clubedogole.com", "senha": "errada"
    })
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_login_admin_invalido(client):
    r = await client.post("/api/auth/login", json={
        "email": "admin@clubedogole.com", "senha": "invalida"
    })
    assert r.status_code == 401
