import uuid
from services import carrinho_service
from flask import Blueprint, request, jsonify
from utils.auth import login_required
from services import venda_service
from database.connection import execute as db_execute

carrinho_bp = Blueprint("carrinho", __name__)

def _uid():
    """Retorna (usuario_id_str, is_guest) a partir do token ou guest_id enviado."""
    token_usuario = getattr(request, "usuario", None)
    if token_usuario:
        return str(token_usuario["id"]), False
    guest_id = request.headers.get("X-Guest-Id") or str(uuid.uuid4())
    return f"guest_{guest_id}", True

@carrinho_bp.route("/")
def ver():
    uid, is_guest = _uid()
    return jsonify({"itens": carrinho_service.itens(uid), "total": carrinho_service.total(uid), "is_guest": is_guest})

@carrinho_bp.route("/adicionar", methods=["POST"])
def adicionar():
    uid, is_guest = _uid()
    data = request.get_json() or {}
    produto_id = data.get("produto_id")
    plano = data.get("plano", "mensal")
    quantidade = max(1, int(data.get("quantidade", 1)))
    if not produto_id:
        return jsonify({"error": "produto_id obrigatório"}), 400
    sucesso, mensagem = carrinho_service.adicionar(uid, produto_id, plano, quantidade)
    return jsonify({"success": sucesso, "message": mensagem, "count": carrinho_service.contador(uid)})

@carrinho_bp.route("/remover", methods=["POST"])
def remover():
    uid, _ = _uid()
    data = request.get_json() or {}
    ids = data.get("ids", [])
    if not ids:
        return jsonify({"error": "Nenhum item informado"}), 400
    removidos = carrinho_service.remover_itens(uid, ids)
    return jsonify({"success": removidos > 0, "removidos": removidos, "total": carrinho_service.total(uid)})

@carrinho_bp.route("/quantidade", methods=["POST"])
@login_required
def atualizar_quantidade():
    uid = str(request.usuario["id"])
    data = request.get_json() or {}
    sucesso, msg, novo_valor, total = carrinho_service.atualizar_quantidade(uid, data.get("item_id"), int(data.get("quantidade", 1)))
    return jsonify({"success": sucesso, "message": msg, "novo_total_item": novo_valor, "total_carrinho": total})

@carrinho_bp.route("/contador")
def contador():
    uid, is_guest = _uid()
    return jsonify({"count": carrinho_service.contador(uid), "is_guest": is_guest})

@carrinho_bp.route("/itens_selecionados", methods=["POST"])
@login_required
def itens_selecionados():
    uid = str(request.usuario["id"])
    ids = (request.get_json() or {}).get("ids", [])
    return jsonify({"itens": carrinho_service.itens_selecionados(uid, ids)})

@carrinho_bp.route("/finalizar", methods=["POST"])
@login_required
def finalizar():
    uid = str(request.usuario["id"])
    data = request.get_json() or {}
    ids = data.get("ids", [])
    cupom = data.get("cupom", "").strip().upper()
    desconto = float(data.get("desconto_cupom", 0))

    if not ids:
        return jsonify({"error": "Nenhum item selecionado"}), 400

    itens = carrinho_service.itens_selecionados(uid, ids)
    sucesso, mensagem = venda_service.finalizar_compra(uid, itens, cupom, desconto)

    if sucesso:
        for id_carrinho in ids:
            db_execute("UPDATE carrinho SET status='finalizado' WHERE id_carrinho=%s AND id_usuario=%s", (id_carrinho, uid))

    return jsonify({"success": sucesso, "message": mensagem}), (200 if sucesso else 400)

@carrinho_bp.route("/meus_pedidos")
@login_required
def meus_pedidos():
    uid = str(request.usuario["id"])
    return jsonify(venda_service.pedidos_do_usuario(uid))