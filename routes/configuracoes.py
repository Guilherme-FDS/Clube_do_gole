from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from utils.auth import login_required
from services import auth_service, endereco_service, venda_service

configuracoes_bp = Blueprint("configuracoes", __name__)


@configuracoes_bp.route("/configuracoes")
@login_required
def configuracoes():
    usuario_id = str(session["usuario_id"])
    usuario = auth_service.buscar_cliente_por_id(usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "erro")
        return redirect(url_for("main.index"))

    enderecos = endereco_service.listar_do_usuario(usuario_id)
    endereco_principal = next((e for e in enderecos if e.get("principal") == "sim"), None)
    pedidos = venda_service.pedidos_do_usuario(usuario_id)

    return render_template(
        "configuracoes.html",
        usuario=usuario,
        enderecos=enderecos,
        endereco_principal=endereco_principal,
        pedidos=pedidos,
    )


@configuracoes_bp.route("/atualizar_perfil", methods=["POST"])
@login_required
def atualizar_perfil():
    usuario_id = str(session["usuario_id"])
    nome = request.form.get("nome", "").strip()
    sobrenome = request.form.get("sobrenome", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefone = request.form.get("telefone", "").strip()

    if not nome or not sobrenome or not email or not telefone:
        return jsonify({"success": False, "message": "Preencha todos os campos obrigatórios."})

    clientes_csv = __import__('utils.csv_helper', fromlist=['ler']).ler(__import__('config').Config.USUARIOS_CLIENTE)
    if any(u["id"] != usuario_id and u.get("email") == email for u in clientes_csv):
        return jsonify({"success": False, "message": "Este e-mail já está em uso."})

    sucesso = auth_service.atualizar_cliente(usuario_id, {
        "nome": nome,
        "sobrenome": sobrenome,
        "email": email,
        "telefone": telefone,
        "data_nascimento": request.form.get("data_nascimento", ""),
    })

    if sucesso:
        session["usuario_nome"] = nome
        session["primeiro_nome"] = nome.split()[0]
        return jsonify({"success": True, "message": "Perfil atualizado com sucesso!"})
    return jsonify({"success": False, "message": "Erro ao atualizar perfil."})


@configuracoes_bp.route("/alterar_senha", methods=["POST"])
@login_required
def alterar_senha():
    usuario_id = str(session["usuario_id"])
    senha_atual = request.form.get("senha_atual", "").strip()
    nova_senha = request.form.get("nova_senha", "").strip()
    confirmar = request.form.get("confirmar_senha", "").strip()

    if not senha_atual or not nova_senha or not confirmar:
        return jsonify({"success": False, "message": "Preencha todos os campos."})

    if nova_senha != confirmar:
        return jsonify({"success": False, "message": "As senhas não coincidem."})

    sucesso, mensagem = auth_service.alterar_senha(usuario_id, senha_atual, nova_senha)
    return jsonify({"success": sucesso, "message": mensagem})


@configuracoes_bp.route("/adicionar_endereco", methods=["POST"])
@login_required
def adicionar_endereco():
    usuario_id = str(session["usuario_id"])
    obrigatorios = ["cep", "endereco", "numero", "bairro", "cidade", "estado"]
    for campo in obrigatorios:
        if not request.form.get(campo, "").strip():
            return jsonify({"success": False, "message": f"O campo {campo} é obrigatório."})

    dados = {
        "tipo":         request.form.get("tipo", "residencial"),
        "cep":          request.form.get("cep", "").strip(),
        "endereco":     request.form.get("endereco", "").strip(),
        "numero":       request.form.get("numero", "").strip(),
        "complemento":  request.form.get("complemento", "").strip(),
        "bairro":       request.form.get("bairro", "").strip(),
        "cidade":       request.form.get("cidade", "").strip(),
        "estado":       request.form.get("estado", "").strip(),
        "pais":         request.form.get("pais", "Brasil").strip(),
    }
    definir_principal = bool(request.form.get("endereco_principal"))
    sucesso, mensagem = endereco_service.adicionar(usuario_id, dados, definir_principal)
    return jsonify({"success": sucesso, "message": mensagem})


@configuracoes_bp.route("/editar_endereco/<endereco_id>", methods=["POST"])
@login_required
def editar_endereco(endereco_id):
    usuario_id = str(session["usuario_id"])
    obrigatorios = ["cep", "endereco", "numero", "bairro", "cidade", "estado"]
    for campo in obrigatorios:
        if not request.form.get(campo, "").strip():
            return jsonify({"success": False, "message": f"O campo {campo} é obrigatório."})

    dados = {
        "tipo":         request.form.get("tipo", "residencial"),
        "cep":          request.form.get("cep", "").strip(),
        "endereco":     request.form.get("endereco", "").strip(),
        "numero":       request.form.get("numero", "").strip(),
        "complemento":  request.form.get("complemento", "").strip(),
        "bairro":       request.form.get("bairro", "").strip(),
        "cidade":       request.form.get("cidade", "").strip(),
        "estado":       request.form.get("estado", "").strip(),
        "pais":         request.form.get("pais", "Brasil").strip(),
    }
    definir_principal = bool(request.form.get("endereco_principal"))
    sucesso, mensagem = endereco_service.atualizar(endereco_id, usuario_id, dados, definir_principal)
    return jsonify({"success": sucesso, "message": mensagem})


@configuracoes_bp.route("/excluir_endereco/<endereco_id>", methods=["POST"])
@login_required
def excluir_endereco(endereco_id):
    usuario_id = str(session["usuario_id"])
    sucesso, mensagem = endereco_service.remover(endereco_id, usuario_id)
    return jsonify({"success": sucesso, "message": mensagem})


@configuracoes_bp.route("/definir_endereco_principal/<endereco_id>", methods=["POST"])
@login_required
def definir_endereco_principal(endereco_id):
    usuario_id = str(session["usuario_id"])
    sucesso, mensagem = endereco_service.definir_principal(endereco_id, usuario_id)
    return jsonify({"success": sucesso, "message": mensagem})


@configuracoes_bp.route("/api/enderecos")
@login_required
def api_enderecos():
    usuario_id = str(session["usuario_id"])
    return jsonify({"enderecos": endereco_service.listar_do_usuario(usuario_id)})