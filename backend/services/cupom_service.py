from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import cupom_repo


async def validar(db: AsyncSession, codigo: str) -> tuple[bool, str, float, str, float | None]:
    """Retorna (valido, mensagem, desconto_pct, tipo_desconto, desconto_fixo)."""
    cupom = await cupom_repo.buscar_por_codigo(db, codigo)
    if not cupom:
        return False, "Cupom inválido.", 0.0, "percentual", None
    if cupom.status != "ativo":
        return False, "Cupom inativo.", 0.0, "percentual", None
    if cupom.usos_restantes is not None and cupom.usos_restantes <= 0:
        return False, "Cupom esgotado.", 0.0, "percentual", None
    if cupom.valido_ate and cupom.valido_ate < date.today():
        return False, "Cupom expirado.", 0.0, "percentual", None

    if cupom.tipo_desconto == "fixo":
        return True, f"Cupom aplicado! R$ {float(cupom.desconto_fixo):.2f} de desconto.", 0.0, "fixo", float(cupom.desconto_fixo)

    pct = float(cupom.desconto_percentual)
    return True, f"Cupom aplicado! {pct}% de desconto.", pct, "percentual", None
