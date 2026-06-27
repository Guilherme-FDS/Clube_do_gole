# routes/contato.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.email import send_contato

router = APIRouter(prefix="/api/contato", tags=["contato"])
limiter = Limiter(key_func=get_remote_address)


class ContatoIn(BaseModel):
    nome: str
    email: EmailStr
    assunto: str
    mensagem: str

    @field_validator("nome", "assunto", "mensagem")
    @classmethod
    def nao_vazio(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("Campo obrigatório")
        return v


@router.post("")
@limiter.limit("5/minute")
async def enviar_contato(request: Request, body: ContatoIn):
    enviado = await send_contato(body.nome, body.email, body.assunto, body.mensagem)
    if not enviado:
        raise HTTPException(status_code=503, detail="Não foi possível enviar a mensagem agora. Tente novamente.")
    return {"ok": True}
