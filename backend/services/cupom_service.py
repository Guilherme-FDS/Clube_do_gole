from sqlalchemy.ext.asyncio import AsyncSession
from repositories import cupom_repo


async def validar(db: AsyncSession, codigo: str) -> tuple[bool, str, float]:
    cupom = await cupom_repo.buscar_por_codigo(db, codigo)
    if not cupom:
        return False, "Cupom inválido.", 0.0
    if cupom.status != "ativo":
        return False, "Cupom inativo.", 0.0
    if cupom.usos_restantes <= 0:
        return False, "Cupom esgotado.", 0.0
    return True, f"Cupom aplicado! {float(cupom.desconto_percentual)}% de desconto.", float(cupom.desconto_percentual)