from services import auth_service, endereco_service
from flask import Blueprint, request, jsonify
from utils.auth import login_required
from services import venda_service

configuracoes_bp = Blueprint("configuracoes", __name__)

@configuracoes_bp.route("/perfil")
@login_required
def perfil():
    uid = str(request.usuario["id"])
    usuario = auth_service.buscar_cliente_por_id(uid)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404
    enderecos = endereco_service.listar_do_usuario(uid)
    pedidos = venda_service.pedidos_do_usuario(uid)
    return jsonify({"usuario": usuario, "enderecos": enderecos, "pedidos": pedidos})

@configuracoes_bp.route("/perfil", methods=["PUT"])
@login_required
def atualizar_perfil():
    uid = str(request.usuario["id"])
    data = request.get_json() or {}
    if not all([data.get("nome"), data.get("sobrenome"), data.get("email"), data.get("telefone")]):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400
    sucesso, msg = auth_service.atualizar_cliente(uid, data)
    return jsonify({"success": sucesso, "message": msg})

@configuracoes_bp.route("/senha", methods=["PUT"])
@login_required
def alterar_senha():
    uid = str(request.usuario["id"])
    data = request.get_json() or {}
    sucesso, msg = auth_service.alterar_senha(uid, data.get("senha_atual",""), data.get("nova_senha",""))
    return jsonify({"success": sucesso, "message": msg})

@configuracoes_bp.route("/enderecos")
@login_required
def enderecos():
    return jsonify(endereco_service.listar_do_usuario(str(request.usuario["id"])))

@configuracoes_bp.route("/enderecos", methods=["POST"])
@login_required
def adicionar_endereco():
    uid = str(request.usuario["id"])
    sucesso, msg = endereco_service.adicionar(uid, request.get_json() or {})
    return jsonify({"success": sucesso, "message": msg}), (201 if sucesso else 400)

@configuracoes_bp.route("/enderecos/<endereco_id>", methods=["PUT"])
@login_required
def editar_endereco(endereco_id):
    uid = str(request.usuario["id"])
    sucesso, msg = endereco_service.editar(uid, endereco_id, request.get_json() or {})
    return jsonify({"success": sucesso, "message": msg})

@configuracoes_bp.route("/enderecos/<endereco_id>", methods=["DELETE"])
@login_required
def excluir_endereco(endereco_id):
    sucesso, msg = endereco_service.excluir(str(request.usuario["id"]), endereco_id)
    return jsonify({"success": sucesso, "message": msg})

@configuracoes_bp.route("/enderecos/<endereco_id>/principal", methods=["PATCH"])
@login_required
def principal_endereco(endereco_id):
    sucesso, msg = endereco_service.definir_principal(str(request.usuario["id"]), endereco_id)
    return jsonify({"success": sucesso, "message": msg})