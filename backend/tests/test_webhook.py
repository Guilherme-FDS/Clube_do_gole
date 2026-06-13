import pytest


@pytest.mark.asyncio
async def test_webhook_sem_mp_configurado(client):
    """Sem credenciais MP, webhook retorna ok:false sem crashar."""
    r = await client.post("/api/pagamentos/webhook", json={
        "type": "payment", "data": {"id": "123"}
    })
    assert r.status_code == 200
    assert r.json() == {"ok": False}


@pytest.mark.asyncio
async def test_webhook_evento_ignorado(client, monkeypatch):
    """Eventos que não são 'payment' são ignorados silenciosamente."""
    from config import get_settings
    monkeypatch.setattr(get_settings(), "mp_access_token", "TEST-fake")
    r = await client.post("/api/pagamentos/webhook?topic=merchant_order&id=99")
    assert r.status_code == 200
