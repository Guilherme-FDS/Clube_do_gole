import pytest
from datetime import date, timedelta


async def _token_admin(client):
    from database.engine import AsyncSessionLocal
    from repositories import auth_repo
    from utils.auth import gerar_token
    from config import get_settings
    settings = get_settings()
    async with AsyncSessionLocal() as db:
        adm = await auth_repo.autenticar_admin(db, settings.admin_email_inicial, settings.admin_senha_inicial)
    if not adm:
        return None
    return gerar_token({"id": adm.id, "email": adm.email, "tipo": "admin", "nome": adm.nome})


@pytest.mark.asyncio
async def test_cupom_invalido(client):
    r = await client.post("/api/cupons/validar", json={"codigo": "NAOEXISTE"})
    assert r.status_code == 200
    assert r.json()["valido"] is False


@pytest.mark.asyncio
async def test_cupom_ciclo_completo(client):
    token = await _token_admin(client)
    if not token:
        pytest.skip("Admin não encontrado no banco de teste")

    headers = {"Authorization": f"Bearer {token}"}

    # Criar cupom
    r = await client.post("/api/admin/cupons", json={
        "codigo": "TESTE10",
        "desconto_percentual": 10,
        "usos_maximos": 5,
        "status": "ativo",
    }, headers=headers)
    assert r.status_code == 201

    # Validar cupom
    r = await client.post("/api/cupons/validar", json={"codigo": "TESTE10"})
    assert r.json()["valido"] is True
    assert r.json()["desconto"] == 10
