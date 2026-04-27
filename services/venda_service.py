import uuid
from datetime import datetime
from config import Config
from utils import csv_helper as csv
from services import produto_service, cupom_service

CAMPOS = [
    "id_compra", "id_usuario", "id_produto", "quantidade",
    "valor_original", "valor_desconto", "valor_total", "data",
    "plano", "desconto_aplicado", "cupom_aplicado",
]

def finalizar_compra(usuario_id, itens, codigo_cupom="", desconto_cupom=0.0):
    if not itens:
        return False, "Nenhum item para finalizar."

    usuario_id = str(usuario_id)
    vendas = csv.ler(Config.VENDAS_FILE)

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

        vendas.append({
            "id_compra": str(uuid.uuid4()),
            "id_usuario": usuario_id,
            "id_produto": item["id_produto"],
            "quantidade": str(quantidade),
            "valor_original": round(valor_original, 2),
            "valor_desconto": round(valor_original - valor_final, 2),
            "valor_total": round(valor_final, 2),
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "plano": plano,
            "desconto_aplicado": round(desconto_total, 2),
            "cupom_aplicado": codigo_cupom,
        })

        produto_service.decrementar_estoque(item["id_produto"], quantidade)

    csv.salvar(Config.VENDAS_FILE, vendas, CAMPOS)

    if codigo_cupom:
        cupom_service.consumir(codigo_cupom)

    return True, f"{len(itens)} item(ns) finalizado(s) com sucesso!"

def pedidos_do_usuario(usuario_id):
    usuario_id = str(usuario_id)
    vendas = csv.ler(Config.VENDAS_FILE)
    produtos = produto_service.listar_todos()
    meus_pedidos = []

    for venda in vendas:
        if venda["id_usuario"] != usuario_id:
            continue
        produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
        valor_original = float(venda.get("valor_original", 0))
        valor_total = float(venda.get("valor_total", 0))
        desconto_aplicado = float(venda.get("desconto_aplicado", 0))

        if valor_original == 0 and valor_total > 0:
            valor_original = (valor_total / (1 - desconto_aplicado / 100)) if desconto_aplicado > 0 else valor_total

        plano = venda.get("plano", "mensal")
        meus_pedidos.append({
            "id_compra": venda.get("id_compra", ""),
            "id_produto": venda.get("id_produto", ""),
            "nome_produto": produto.get("nome", "Produto não encontrado"),
            "quantidade": venda.get("quantidade", "1"),
            "plano": plano,
            "data": venda.get("data", ""),
            "imagem_produto": produto.get("imagem", ""),
            "valor_total": valor_total,
            "valor_sem_desconto": valor_original,
            "valor_com_desconto": valor_total,
            "desconto_aplicado": desconto_aplicado,
            "desconto_recorrencia": Config.DESCONTOS_PLANO.get(plano, 0) * 100,
            "cupom_aplicado": venda.get("cupom_aplicado", ""),
            "economia": max(0, valor_original - valor_total),
        })

    meus_pedidos.sort(key=lambda x: x.get("data", ""), reverse=True)
    return meus_pedidos

def dados_dashboard():
    vendas = csv.ler(Config.VENDAS_FILE)
    produtos = produto_service.listar_todos()

    for venda in vendas:
        venda["valor_total"] = float(venda.get("valor_total", 0))
        venda["quantidade"] = int(venda.get("quantidade", 1))

    faturamento_total = sum(v["valor_total"] for v in vendas)
    clientes_unicos = len(set(v["id_usuario"] for v in vendas))

    produtos_vendidos = {}
    for venda in vendas:
        produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
        nome = produto.get("nome", f"Produto {venda['id_produto']}")
        if nome not in produtos_vendidos:
            produtos_vendidos[nome] = {"quantidade": 0, "faturamento": 0, "id": venda["id_produto"]}
        produtos_vendidos[nome]["quantidade"] += venda["quantidade"]
        produtos_vendidos[nome]["faturamento"] += venda["valor_total"]

    mais_vendidos = sorted(produtos_vendidos.items(), key=lambda x: x[1]["quantidade"], reverse=True)[:10]

    vendas_por_mes = {}
    for venda in vendas:
        mes_ano = (venda.get("data") or "")[:7]
        if not mes_ano:
            continue
        if mes_ano not in vendas_por_mes:
            vendas_por_mes[mes_ano] = {"quantidade": 0, "faturamento": 0, "vendas": 0}
        vendas_por_mes[mes_ano]["quantidade"] += venda["quantidade"]
        vendas_por_mes[mes_ano]["faturamento"] += venda["valor_total"]
        vendas_por_mes[mes_ano]["vendas"] += 1

    ultimas = sorted(vendas, key=lambda x: x.get("data", ""), reverse=True)[:10]
    for venda in ultimas:
        produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
        venda["nome_produto"] = produto.get("nome", f"Produto {venda['id_produto']}")
        venda["tipo_produto"] = produto.get("tipo", "N/A")

    return {
        "total_vendas": len(vendas),
        "faturamento_total": faturamento_total,
        "clientes_unicos": clientes_unicos,
        "produtos_mais_vendidos": mais_vendidos,
        "vendas_por_mes": vendas_por_mes,
        "ultimas_vendas": ultimas,
    }

def buscar_venda(venda_id):
    vendas = csv.ler(Config.VENDAS_FILE)
    produtos = produto_service.listar_todos()
    clientes = csv.ler(Config.USUARIOS_CLIENTE)

    venda = next((v for v in vendas if v["id_compra"] == venda_id), None)
    if not venda:
        return None

    produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
    usuario = next((u for u in clientes if u["id"] == venda["id_usuario"]), {})

    venda["nome_produto"] = produto.get("nome", f"Produto {venda['id_produto']}")
    venda["tipo_produto"] = produto.get("tipo", "N/A")
    venda["nome_usuario"] = usuario.get("nome", "Cliente")
    venda["email_usuario"] = usuario.get("email", "N/A")

    try:
        venda["preco_unitario"] = float(venda["valor_total"]) / int(venda["quantidade"])
    except (ValueError, ZeroDivisionError):
        venda["preco_unitario"] = 0

    return venda