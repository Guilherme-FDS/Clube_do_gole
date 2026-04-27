from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import auth_service, carrinho_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()

        if not email or not senha:
            flash("Preencha todos os campos!", "erro")
            return redirect(url_for("auth.login"))

        admin = auth_service.autenticar_admin(email, senha)
        if admin:
            session["usuario_id"] = admin.get("id")
            session["email"] = admin.get("email")
            session["tipo"] = "admin"
            session["usuario_nome"] = admin.get("nome")
            flash("Login de administrador realizado!", "sucesso")
            return redirect(url_for("admin.painel"))

        cliente = auth_service.autenticar_cliente(email, senha)
        if cliente:
            usuario_id = cliente.get("id")
            guest_id = session.get("guest_id")
            itens_migrados = 0
            if guest_id:
                itens_migrados = carrinho_service.migrar_guest(guest_id, usuario_id)
                session.pop("guest_id", None)

            session["usuario_id"] = usuario_id
            session["email"] = cliente.get("email")
            session["tipo"] = "cliente"
            session["usuario_nome"] = cliente.get("nome")
            session["primeiro_nome"] = cliente.get("nome", "").split()[0]

            redirect_to = request.args.get("redirect")

            if itens_migrados > 0:
                flash(f"Login realizado! {itens_migrados} item(ns) do carrinho recuperados.", "sucesso")
                return redirect(url_for("carrinho.ver"))

            if carrinho_service.contador(usuario_id) > 0:
                flash("Login realizado! Seu carrinho foi mantido.", "sucesso")
                return redirect(url_for("carrinho.ver"))

            flash("Login realizado com sucesso!", "sucesso")
            if redirect_to == "checkout":
                return redirect(url_for("carrinho.ver"))
            return redirect(url_for("main.index"))

        flash("E-mail ou senha inválidos!", "erro")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    usuario_id = session.get("usuario_id")
    if usuario_id:
        carrinho_service.limpar_usuario(str(usuario_id))
    session.clear()
    flash("Você saiu da sua conta. Seu carrinho foi limpo.", "sucesso")
    return redirect(url_for("main.index"))


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        campos = {
            "cpf":              request.form.get("cpf", "").strip(),
            "nome":             request.form.get("nome", "").strip(),
            "sobrenome":        request.form.get("sobrenome", "").strip(),
            "data_nascimento":  request.form.get("data_nascimento", "").strip(),
            "email":            request.form.get("email", "").strip().lower(),
            "senha":            request.form.get("senha", "").strip(),
            "telefone":         request.form.get("telefone", "").strip(),
        }

        obrigatorios = ["cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"]
        if any(not campos[c] for c in obrigatorios):
            flash("Preencha todos os campos obrigatórios!", "erro")
            return redirect(url_for("auth.cadastro"))

        if auth_service.email_ja_cadastrado(campos["email"]):
            flash("E-mail já cadastrado!", "erro")
            return redirect(url_for("auth.cadastro"))

        if auth_service.cpf_ja_cadastrado(campos["cpf"]):
            flash("CPF já cadastrado!", "erro")
            return redirect(url_for("auth.cadastro"))

        auth_service.cadastrar_cliente(campos)
        flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
        return redirect(url_for("auth.login"))

    return render_template("cadastro.html")