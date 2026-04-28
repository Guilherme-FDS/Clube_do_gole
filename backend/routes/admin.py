from backend.services import cupom_service, produto_service
from flask import Blueprint, request, jsonify
from backend.utils.auth import admin_required
from backend.services import venda_service

admin_bp = Blueprint("admin", __name__)

# ── Produtos ──────────────────────────────────────────────────────────────────

@admin_bp.route("/produtos")
@admin_required
def listar_produtos():
    return jsonify(produto_service.listar_todos())

@admin_bp.route("/produtos", methods=["POST"])
@admin_required
def adicionar_produto():
    data = request.get_json() or {}
    produto_service.adicionar(data)
    return jsonify({"message": "Produto adicionado"}), 201

@admin_bp.route("/produtos/<produto_id>", methods=["GET"])
@admin_required
def get_produto(produto_id):
    p = produto_service.buscar_por_id(produto_id)
    if not p:
        return jsonify({"error": "Não encontrado"}), 404
    return jsonify(p)

@admin_bp.route("/produtos/<produto_id>", methods=["PUT"])
@admin_required
def editar_produto(produto_id):
    produto_service.atualizar(produto_id, request.get_json() or {})
    return jsonify({"message": "Produto atualizado"})

@admin_bp.route("/produtos/<produto_id>", methods=["DELETE"])
@admin_required
def deletar_produto(produto_id):
    produto_service.remover(produto_id)
    return jsonify({"message": "Produto removido"})

# ── Cupons ────────────────────────────────────────────────────────────────────

@admin_bp.route("/cupons")
@admin_required
def listar_cupons():
    return jsonify(cupom_service.listar_todos())

@admin_bp.route("/cupons", methods=["POST"])
@admin_required
def adicionar_cupom():
    data = request.get_json() or {}
    usos = data.get("usos_maximos", 1)
    cupom_service.adicionar({**data, "usos_restantes": usos, "codigo": data.get("codigo","").upper()})
    return jsonify({"message": "Cupom adicionado"}), 201

@admin_bp.route("/cupons/<cupom_id>", methods=["GET"])
@admin_required
def get_cupom(cupom_id):
    c = cupom_service.buscar_por_id(cupom_id)
    if not c:
        return jsonify({"error": "Não encontrado"}), 404
    return jsonify(c)

@admin_bp.route("/cupons/<cupom_id>", methods=["PUT"])
@admin_required
def editar_cupom(cupom_id):
    data = request.get_json() or {}
    cupom = cupom_service.buscar_por_id(cupom_id)
    usos_usados = int(cupom.get("usos_maximos",1)) - int(cupom.get("usos_restantes",1))
    novos_max = int(data.get("usos_maximos", cupom["usos_maximos"]))
    data["usos_restantes"] = max(0, novos_max - usos_usados)
    data["codigo"] = data.get("codigo","").upper()
    cupom_service.atualizar(cupom_id, data)
    return jsonify({"message": "Cupom atualizado"})

@admin_bp.route("/cupons/<cupom_id>", methods=["DELETE"])
@admin_required
def remover_cupom(cupom_id):
    cupom_service.remover(cupom_id)
    return jsonify({"message": "Cupom removido"})

@admin_bp.route("/cupons/<cupom_id>/status", methods=["PATCH"])
@admin_required
def status_cupom(cupom_id):
    novo_status = (request.get_json() or {}).get("status")
    cupom_service.alterar_status(cupom_id, novo_status)
    return jsonify({"message": f"Status atualizado para {novo_status}"})

# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return jsonify(venda_service.dados_dashboard())

@admin_bp.route("/vendas/<venda_id>")
@admin_required
def detalhes_venda(venda_id):
    venda = venda_service.buscar_venda(venda_id)
    if not venda:
        return jsonify({"error": "Venda não encontrada"}), 404
    return jsonify(venda)