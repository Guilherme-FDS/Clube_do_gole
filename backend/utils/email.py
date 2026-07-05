import logging
import httpx
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import get_settings

logger = logging.getLogger("uvicorn")

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _get_mail_config():
    settings = get_settings()
    if not settings.gmail_user or not settings.gmail_app_password:
        return None
    return ConnectionConfig(
        MAIL_USERNAME=settings.gmail_user,
        MAIL_PASSWORD=settings.gmail_app_password,
        MAIL_FROM=settings.gmail_user,
        MAIL_PORT=465,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_FROM_NAME="Clube do Golê",
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
        TIMEOUT=15,
    )


async def _enviar_brevo(destinatarios: list[str], assunto: str, html: str, reply_to: str | None = None) -> bool:
    settings = get_settings()
    remetente = settings.email_remetente or settings.gmail_user
    payload = {
        "sender": {"name": "Clube do Golê", "email": remetente},
        "to": [{"email": e} for e in destinatarios],
        "subject": assunto,
        "htmlContent": html,
    }
    if reply_to:
        payload["replyTo"] = {"email": reply_to}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            BREVO_API_URL,
            json=payload,
            headers={"api-key": settings.brevo_api_key, "accept": "application/json"},
        )
    if resp.status_code in (200, 201):
        return True
    logger.error(f"Brevo recusou envio ({resp.status_code}): {resp.text[:300]}")
    return False


async def _enviar_smtp(destinatarios: list[str], assunto: str, html: str, reply_to: str | None = None) -> bool:
    conf = _get_mail_config()
    if not conf:
        logger.warning("Email não configurado (sem BREVO_API_KEY nem credenciais Gmail).")
        return False
    message = MessageSchema(
        subject=assunto,
        recipients=destinatarios,
        reply_to=[reply_to] if reply_to else [],
        body=html,
        subtype=MessageType.html,
    )
    await FastMail(conf).send_message(message)
    return True


async def _enviar(destinatarios: list[str], assunto: str, html: str, reply_to: str | None = None) -> bool:
    """Canal único de envio. Brevo (API HTTP) tem prioridade — SMTP outbound é
    bloqueado no Render, então o fallback Gmail só serve para dev local."""
    settings = get_settings()
    try:
        if settings.brevo_api_key:
            return await _enviar_brevo(destinatarios, assunto, html, reply_to)
        return await _enviar_smtp(destinatarios, assunto, html, reply_to)
    except Exception as e:
        logger.error(f"Erro ao enviar email '{assunto}' para {destinatarios}: {e}")
        return False


def _html_reset(nome: str, url: str, expire: int) -> str:
    return f"""
    <div style="font-family:Arial,sans-serif;background:#f5f5f5;padding:40px;">
      <div style="max-width:520px;margin:0 auto;background:#fff;border-radius:8px;padding:32px;">
        <h2 style="color:#b5860d;">Clube do Golê 🍺</h2>
        <p>Olá, <strong>{nome}</strong>!</p>
        <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>
        <a href="{url}" style="display:inline-block;margin:16px 0;padding:12px 28px;
           background:#b5860d;color:#fff;border-radius:6px;text-decoration:none;font-size:16px;">
          Redefinir senha
        </a>
        <p style="color:#e05c5c;font-size:13px;">⚠️ Este link expira em <strong>{expire} minutos</strong>.</p>
        <hr style="border:1px solid #eee;margin:24px 0;"/>
        <p style="font-size:12px;color:#999;">Se você não solicitou isso, ignore este email.</p>
      </div>
    </div>
    """


def _html_pedido_confirmado(nome: str, venda_id: int, valor_total: float, itens: list[dict]) -> str:
    itens_html = "".join(
        f"<tr><td style='padding:6px 0'>{i['nome_produto']} ({i['plano']})</td>"
        f"<td style='padding:6px 0;text-align:right'>R$ {i['valor_total']:.2f}</td></tr>"
        for i in itens
    )
    return f"""
    <div style="font-family:Arial,sans-serif;background:#f5f5f5;padding:40px;">
      <div style="max-width:520px;margin:0 auto;background:#fff;border-radius:8px;padding:32px;">
        <h2 style="color:#b5860d;">Clube do Golê 🍾</h2>
        <p>Olá, <strong>{nome}</strong>! Seu pedido foi recebido.</p>
        <table width="100%" style="border-collapse:collapse;margin:16px 0;">{itens_html}</table>
        <p style="font-size:16px;font-weight:bold;">Total: R$ {valor_total:.2f}</p>
        <p style="color:#666;font-size:13px;">Pedido #{venda_id} — aguardando confirmação de pagamento.</p>
        <hr style="border:1px solid #eee;margin:24px 0;"/>
        <p style="font-size:12px;color:#999;">Clube do Golê — bebidas com curadoria.</p>
      </div>
    </div>
    """


def _html_pagamento_aprovado(nome: str, venda_id: int, valor_total: float, plano: str) -> str:
    return f"""
    <div style="font-family:Arial,sans-serif;background:#f5f5f5;padding:40px;">
      <div style="max-width:520px;margin:0 auto;background:#fff;border-radius:8px;padding:32px;">
        <h2 style="color:#2e8b57;">✅ Pagamento Aprovado — Clube do Golê</h2>
        <p>Olá, <strong>{nome}</strong>!</p>
        <p>Seu pagamento de <strong>R$ {valor_total:.2f}</strong> foi aprovado.</p>
        <p>Sua assinatura <strong>{plano}</strong> já está ativa. Em breve sua caixa chega.</p>
        <p style="color:#666;font-size:13px;">Pedido #{venda_id}</p>
        <hr style="border:1px solid #eee;margin:24px 0;"/>
        <p style="font-size:12px;color:#999;">Clube do Golê — bebidas com curadoria.</p>
      </div>
    </div>
    """


async def send_pedido_confirmado(recipient_email: str, nome: str, venda_id: int, valor_total: float, itens: list[dict]) -> None:
    await _enviar(
        [recipient_email],
        f"Clube do Golê — Pedido #{venda_id} recebido!",
        _html_pedido_confirmado(nome, venda_id, valor_total, itens),
    )


async def send_pagamento_aprovado(recipient_email: str, nome: str, venda_id: int, valor_total: float, plano: str) -> None:
    await _enviar(
        [recipient_email],
        "Clube do Golê — Pagamento aprovado! 🎉",
        _html_pagamento_aprovado(nome, venda_id, valor_total, plano),
    )


def _html_contato(nome: str, email: str, assunto: str, mensagem: str) -> str:
    return f"""
    <div style="font-family:Arial,sans-serif;background:#f5f5f5;padding:40px;">
      <div style="max-width:520px;margin:0 auto;background:#fff;border-radius:8px;padding:32px;">
        <h2 style="color:#b5860d;">📬 Nova mensagem — Central de Relacionamento</h2>
        <p><strong>Nome:</strong> {nome}</p>
        <p><strong>E-mail:</strong> {email}</p>
        <p><strong>Assunto:</strong> {assunto}</p>
        <hr style="border:1px solid #eee;margin:16px 0;"/>
        <p style="white-space:pre-wrap;">{mensagem}</p>
        <hr style="border:1px solid #eee;margin:24px 0;"/>
        <p style="font-size:12px;color:#999;">Enviado pelo formulário de contato do site.</p>
      </div>
    </div>
    """


async def send_contato(nome: str, email: str, assunto: str, mensagem: str) -> bool:
    """Envia a mensagem do formulário de contato para o e-mail da empresa.
    Retorna True se enviou, False se e-mail não configurado ou falhou."""
    settings = get_settings()
    destino = settings.email_remetente or settings.gmail_user
    if not destino:
        logger.warning("Email não configurado — formulário de contato desabilitado.")
        return False
    return await _enviar(
        [destino],
        f"[Contato] {assunto} — {nome}",
        _html_contato(nome, email, assunto, mensagem),
        reply_to=email,
    )


async def send_reset_password_email(recipient_email: str, nome: str, token: str) -> None:
    settings = get_settings()
    url = f"{settings.frontend_url}/reset-password?token={token}"
    enviado = await _enviar(
        [recipient_email],
        "Clube do Golê — Redefinição de senha",
        _html_reset(nome, url, settings.reset_token_expire_minutes),
    )
    if not enviado:
        logger.warning(f"Reset de senha NÃO enviado para {recipient_email} — verifique BREVO_API_KEY.")