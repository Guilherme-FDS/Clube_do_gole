# services/plano_service.py
from decimal import Decimal


_MESES = {"mensal": 1, "semestral": 6, "anual": 12}


def enriquecer_plano(p) -> dict:
    m = _MESES.get(p.recorrencia, 1)
    preco_cheio = Decimal(str(p.preco_base)) * m
    preco_total = round(preco_cheio * (1 - Decimal(str(p.desconto_pct)) / 100), 2)
    economia = round(preco_cheio - preco_total, 2)
    return {
        "id": p.id,
        "id_produto": p.id_produto,
        "recorrencia": p.recorrencia,
        "preco_base": p.preco_base,
        "desconto_pct": p.desconto_pct,
        "preco_total": preco_total,
        "economia": economia,
        "ativo": p.ativo,
        "criado_em": p.criado_em,
        "atualizado_em": p.atualizado_em,
    }