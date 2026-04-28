from backend.services import auth_service
from flask import Blueprint, request, jsonify
from backend.services import carrinho_service
from backend.utils.auth import gerar_token, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    senha = data.get("senha", "").strip()
    guest_id = data.get("guest_id")

    if not email or not senha:
        return jsonify({"error": "Preencha todos os campos"}), 400

    admin = auth_service.autenticar_admin(email, senha)
    if admin:
        token = gerar_token({"id": admin["id"], "email": admin["email"], "tipo": "admin", "nome": admin["nome"]})
        return jsonify({"token": token, "tipo": "admin", "nome": admin["nome"]})

    cliente = auth_service.autenticar_cliente(email, senha)
    if cliente:
        uid = str(cliente["id"])
        itens_migrados = 0
        if guest_id:
            itens_migrados = carrinho_service.migrar_guest(f"guest_{guest_id}", uid)
        token = gerar_token({"id": cliente["id"], "email": cliente["email"], "tipo": "cliente", "nome": cliente["nome"]})
        return jsonify({"token": token, "tipo": "cliente", "nome": cliente["nome"], "itens_migrados": itens_migrados})

    return jsonify({"error": "E-mail ou senha inválidos"}), 401

@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json() or {}
    obrigatorios = ["cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"]
    if any(not data.get(c, "").strip() for c in obrigatorios):
        return jsonify({"error": "Preencha todos os campos obrigatórios"}), 400

    if auth_service.email_ja_cadastrado(data["email"].lower()):
        return jsonify({"error": "E-mail já cadastrado"}), 409
    if auth_service.cpf_ja_cadastrado(data["cpf"]):
        return jsonify({"error": "CPF já cadastrado"}), 409

    auth_service.cadastrar_cliente(data)
    return jsonify({"message": "Cadastro realizado com sucesso"}), 201

@auth_bp.route("/me")
@login_required
def me():
    return jsonify(request.usuario)

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    uid = str(request.usuario["id"])
    carrinho_service.limpar_usuario(uid)
    return jsonify({"message": "Logout realizado"})