import uuid
from datetime import datetime
from config import Config
from database.connection import fetchall, fetchone, execute
from services import produto_service, cupom_service


def finalizar_compra(usuario_id, itens, codigo_cupom="", desconto_cupom=0.0):
    if not itens:
        return False, "Nenhum item para finalizar."

    for item in itens:
        valor_unitario = float(item["valor_unitario"])
        quantidade = int(item["quantidade"])
        plano = item["plano"]

        mult = Config.MULTIPLICADORES_PLANO.get(plano, 1)
        desc_plano = Config.DESCONTOS_PLANO.get(plano, 0)

        valor_original = valor_unitario * mult * quantidade
        valor_apos_plano = valor_original * (1 - desc_plano)
        valor_final = max(0, valor_apos_plano * (1 - (desconto_cupom / 100)))
        desconto_total = ((valor_original - valor_final) / valor_original * 100) if valor_original else 0

        execute("""
            INSERT INTO vendas (
                id_compra, id_usuario, id_produto, quantidade,
                valor_original, valor_desconto, valor_total,
                plano, desconto_aplicado, cupom_aplicado, data
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()),
            int(usuario_id),
            int(item["id_produto"]),
            quantidade,
            round(valor_original, 2),
            round(valor_original - valor_final, 2),
            round(valor_final, 2),
            plano,
            round(desconto_total, 2),
            codigo_cupom,
            datetime.now(),
        ))

        produto_service.decrementar_estoque(item["id_produto"], quantidade)

    if codigo_cupom:
        cupom_service.consumir(codigo_cupom)

    return True, f"{len(itens)} item(ns) finalizado(s) com sucesso!"


def pedidos_do_usuario(usuario_id):
    rows = fetchall("""
        SELECT v.*, p.nome AS nome_produto, p.imagem AS imagem_produto,
               p.descricao AS descricao_produto
        FROM vendas v
        LEFT JOIN produtos p ON p.id = v.id_produto
        WHERE v.id_usuario = %s
        ORDER BY v.data DESC
    """, (int(usuario_id),))

    pedidos = []
    for v in rows:
        valor_original = float(v.get("valor_original") or 0)
        valor_total = float(v.get("valor_total") or 0)
        desconto_aplicado = float(v.get("desconto_aplicado") or 0)
        plano = v.get("plano", "mensal")

        pedidos.append({
            "id_compra": str(v.get("id_compra", "")),
            "id_produto": v.get("id_produto"),
            "nome_produto": v.get("nome_produto", "Produto não encontrado"),
            "quantidade": v.get("quantidade", 1),
            "plano": plano,
            "data": str(v.get("data", "")),
            "imagem_produto": v.get("imagem_produto", ""),
            "valor_total": valor_total,
            "valor_sem_desconto": valor_original,
            "valor_com_desconto": valor_total,
            "desconto_aplicado": desconto_aplicado,
            "desconto_recorrencia": Config.DESCONTOS_PLANO.get(plano, 0) * 100,
            "cupom_aplicado": v.get("cupom_aplicado", ""),
            "economia": max(0, valor_original - valor_total),
        })

    return pedidos


def dados_dashboard():
    vendas = fetchall("""
        SELECT v.*, p.nome AS nome_produto, p.tipo AS tipo_produto
        FROM vendas v
        LEFT JOIN produtos p ON p.id = v.id_produto
        ORDER BY v.data DESC
    """)

    for v in vendas:
        v["valor_total"] = float(v.get("valor_total") or 0)
        v["quantidade"] = int(v.get("quantidade") or 1)

    faturamento_total = sum(v["valor_total"] for v in vendas)
    clientes_unicos = len(set(v["id_usuario"] for v in vendas))

    produtos_vendidos = {}
    for v in vendas:
        nome = v.get("nome_produto") or f"Produto {v['id_produto']}"
        if nome not in produtos_vendidos:
            produtos_vendidos[nome] = {"quantidade": 0, "faturamento": 0, "id": v["id_produto"]}
        produtos_vendidos[nome]["quantidade"] += v["quantidade"]
        produtos_vendidos[nome]["faturamento"] += v["valor_total"]

    mais_vendidos = sorted(produtos_vendidos.items(), key=lambda x: x[1]["quantidade"], reverse=True)[:10]

    vendas_por_mes = {}
    for v in vendas:
        mes_ano = str(v.get("data") or "")[:7]
        if not mes_ano:
            continue
        if mes_ano not in vendas_por_mes:
            vendas_por_mes[mes_ano] = {"quantidade": 0, "faturamento": 0, "vendas": 0}
        vendas_por_mes[mes_ano]["quantidade"] += v["quantidade"]
        vendas_por_mes[mes_ano]["faturamento"] += v["valor_total"]
        vendas_por_mes[mes_ano]["vendas"] += 1

    ultimas = vendas[:10]

    return {
        "total_vendas": len(vendas),
        "faturamento_total": faturamento_total,
        "clientes_unicos": clientes_unicos,
        "produtos_mais_vendidos": mais_vendidos,
        "vendas_por_mes": vendas_por_mes,
        "ultimas_vendas": ultimas,
    }


def buscar_venda(venda_id):
    venda = fetchone("""
        SELECT v.*, p.nome AS nome_produto, p.tipo AS tipo_produto,
               u.nome AS nome_usuario, u.email AS email_usuario
        FROM vendas v
        LEFT JOIN produtos p ON p.id = v.id_produto
        LEFT JOIN usuarios_clientes u ON u.id = v.id_usuario
        WHERE v.id_compra = %s
    """, (venda_id,))

    if not venda:
        return None

    try:
        venda["preco_unitario"] = float(venda["valor_total"]) / int(venda["quantidade"])
    except (TypeError, ZeroDivisionError):
        venda["preco_unitario"] = 0

    return venda