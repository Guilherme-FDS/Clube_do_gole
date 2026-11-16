import html
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
        MAIL_FROM_NAME="Vaultierre",
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
        "sender": {"name": "Vaultierre", "email": remetente},
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


# ===== Identidade Vaultierre (fonte única para todas as notificações) =====
BRAND_NAME = "Vaultierre"
BRAND_TAGLINE = "Destilados raros, com curadoria."
_COR_FUNDO = "#1b1a19"
_COR_CARD = "#242220"
_COR_DOURADO = "#C9A84C"
_COR_TEXTO = "#F2EEE6"
_COR_TEXTO_2 = "#AAAAAA"
_FONTE_TITULO = "'Cormorant Garamond',Georgia,serif"
_FONTE_UI = "'DM Sans','Helvetica Neue',Arial,sans-serif"


def _escape(v) -> str:
    return html.escape(str(v), quote=True)


def _botao(texto: str, url: str) -> str:
    return (
        f'<a href="{_escape(url)}" style="display:inline-block;margin:20px 0;padding:14px 32px;'
        f'background:{_COR_DOURADO};color:{_COR_FUNDO};border-radius:4px;text-decoration:none;'
        f'font-family:{_FONTE_UI};font-size:14px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">'
        f'{_escape(texto)}</a>'
    )


def _layout(titulo: str, corpo: str) -> str:
    """Moldura padrão de todo e-mail Vaultierre: cabeçalho com a marca,
    título, corpo e rodapé. Os templates só montam o `corpo`."""
    return f"""
    <div style="background:{_COR_FUNDO};padding:40px 16px;font-family:{_FONTE_UI};color:{_COR_TEXTO};">
      <div style="max-width:560px;margin:0 auto;background:{_COR_CARD};border-radius:8px;
                  border-top:3px solid {_COR_DOURADO};padding:36px 32px;">
        <p style="margin:0 0 4px;font-family:{_FONTE_TITULO};font-size:26px;letter-spacing:4px;
                  color:{_COR_DOURADO};text-transform:uppercase;">{BRAND_NAME}</p>
        <h2 style="margin:16px 0 20px;font-family:{_FONTE_TITULO};font-weight:400;font-size:24px;
                   color:{_COR_TEXTO};">{titulo}</h2>
        <div style="font-size:15px;line-height:1.6;color:{_COR_TEXTO};">{corpo}</div>
        <hr style="border:none;border-top:1px solid #3a3734;margin:28px 0 16px;"/>
        <p style="margin:0;font-size:12px;color:{_COR_TEXTO_2};">{BRAND_NAME} — {BRAND_TAGLINE}</p>
      </div>
    </div>
    """


def _html_reset(nome: str, url: str, expire: int) -> str:
    corpo = (
        f"<p>Olá, <strong>{_escape(nome)}</strong>.</p>"
        "<p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>"
        f"{_botao('Redefinir senha', url)}"
        f'<p style="font-size:13px;color:{_COR_TEXTO_2};">Este link expira em <strong>{expire} minutos</strong>. '
        "Se você não fez essa solicitação, ignore este e-mail.</p>"
    )
    return _layout("Redefinição de senha", corpo)


def _html_pedido_confirmado(nome: str, venda_id: int, valor_total: float, itens: list[dict]) -> str:
    itens_html = "".join(
        f"<tr><td style='padding:8px 0;border-bottom:1px solid #3a3734'>{_escape(i['nome_produto'])} "
        f"<span style='color:{_COR_TEXTO_2}'>({_escape(i['plano'])})</span></td>"
        f"<td style='padding:8px 0;border-bottom:1px solid #3a3734;text-align:right'>R$ {i['valor_total']:.2f}</td></tr>"
        for i in itens
    )
    corpo = (
        f"<p>Olá, <strong>{_escape(nome)}</strong>. Recebemos o seu pedido.</p>"
        f'<table width="100%" style="border-collapse:collapse;margin:16px 0;color:{_COR_TEXTO};font-size:14px;">{itens_html}</table>'
        f'<p style="font-size:17px;"><strong>Total: R$ {valor_total:.2f}</strong></p>'
        f'<p style="font-size:13px;color:{_COR_TEXTO_2};">Pedido #{venda_id} — aguardando confirmação do pagamento. '
        "Avisaremos assim que for aprovado.</p>"
    )
    return _layout(f"Pedido #{venda_id} recebido", corpo)


def _html_pagamento_aprovado(nome: str, venda_id: int, valor_total: float, plano: str) -> str:
    corpo = (
        f"<p>Olá, <strong>{_escape(nome)}</strong>.</p>"
        f"<p>Seu pagamento de <strong>R$ {valor_total:.2f}</strong> foi aprovado e sua assinatura "
        f"<strong>{_escape(plano)}</strong> está ativa.</p>"
        "<p>Nossa curadoria já está preparando a sua próxima caixa.</p>"
        f'<p style="font-size:13px;color:{_COR_TEXTO_2};">Pedido #{venda_id}</p>'
    )
    return _layout("Bem-vindo ao Vaultierre", corpo)


async def send_pedido_confirmado(recipient_email: str, nome: str, venda_id: int, valor_total: float, itens: list[dict]) -> None:
    await _enviar(
        [recipient_email],
        f"{BRAND_NAME} — Pedido #{venda_id} recebido",
        _html_pedido_confirmado(nome, venda_id, valor_total, itens),
    )


async def send_pagamento_aprovado(recipient_email: str, nome: str, venda_id: int, valor_total: float, plano: str) -> None:
    await _enviar(
        [recipient_email],
        f"{BRAND_NAME} — Pagamento aprovado",
        _html_pagamento_aprovado(nome, venda_id, valor_total, plano),
    )


def _html_contato(nome: str, email: str, assunto: str, mensagem: str) -> str:
    corpo = (
        f"<p><strong>Nome:</strong> {_escape(nome)}<br/>"
        f"<strong>E-mail:</strong> {_escape(email)}<br/>"
        f"<strong>Assunto:</strong> {_escape(assunto)}</p>"
        f'<p style="white-space:pre-wrap;border-left:2px solid {_COR_DOURADO};padding-left:12px;">{_escape(mensagem)}</p>'
        f'<p style="font-size:12px;color:{_COR_TEXTO_2};">Enviado pelo formulário de contato do site.</p>'
    )
    return _layout("Nova mensagem — Central de Relacionamento", corpo)


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
        f"{BRAND_NAME} — Redefinição de senha",
        _html_reset(nome, url, settings.reset_token_expire_minutes),
    )
    if not enviado:
        logger.warning(f"Reset de senha NÃO enviado para {recipient_email} — verifique BREVO_API_KEY.")