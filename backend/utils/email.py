import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import get_settings

logger = logging.getLogger("uvicorn")


def _get_mail_config():
    settings = get_settings()
    if not settings.gmail_user or not settings.gmail_app_password:
        return None
    return ConnectionConfig(
        MAIL_USERNAME=settings.gmail_user,
        MAIL_PASSWORD=settings.gmail_app_password,
        MAIL_FROM=settings.gmail_user,
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_FROM_NAME="Clube do Golê",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
    )


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


async def send_reset_password_email(recipient_email: str, nome: str, token: str) -> None:
    settings = get_settings()
    conf = _get_mail_config()
    if not conf:
        logger.warning("Email não configurado — reset de senha desabilitado.")
        return
    url = f"{settings.frontend_url}/reset-password?token={token}"
    try:
        message = MessageSchema(
            subject="Clube do Golê — Redefinição de senha",
            recipients=[recipient_email],
            body=_html_reset(nome, url, settings.reset_token_expire_minutes),
            subtype=MessageType.html,
        )
        await FastMail(conf).send_message(message)
    except Exception as e:
        logger.error(f"Erro ao enviar email de reset para {recipient_email}: {e}")