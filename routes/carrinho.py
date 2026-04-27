import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from utils.auth import login_required
from services import carrinho_service, venda_service

carrinho_bp = Blueprint("carrinho", __name__)


def _get_usuario_id():
    """Retorna usuario_id ou cria sessão guest."""
    if "usuario_id" in session:
        return str(session["usuario_id"]), False
    if "guest_id" not in session:
        session["guest_id"] = str(uuid.uuid4())
    return f"guest_{session['guest_id']}", True


@carrinho_bp.route("/carrinho")
def ver():
    usuario_id, is_guest = _get_usuario_id()
    itens = carrinho_service.itens(usuario_id)
    return render_template(
        "carrinho.html",
        itens_carrinho=itens,
        total=carrinho_service.total(usuario_id),
        is_guest=is_guest,
    )


@carrinho_bp.route("/adicionar_carrinho", methods=["POST"])
def adicionar():
    usuario_id, is_guest = _get_usuario_id()

    produto_id = request.form.get("id_produto")
    plano = request.form.get("plano", "mensal")
    try:
        quantidade = max(1, int(request.form.get("quantidade", 1)))
    except (ValueError, TypeError):
        quantidade = 1

    if not produto_id:
        return jsonify({"success": False, "message": "ID do produto não informado."})

    sucesso, mensagem = carrinho_service.adicionar(usuario_id, produto_id, plano, quantidade)
    count = carrinho_service.contador(usuario_id)
    return jsonify({"success": sucesso, "message": mensagem, "count": count, "is_guest": is_guest})


@carrinho_bp.route("/excluir_item_carrinho", methods=["POST"])
def excluir_item():
    usuario_id, is_guest = _get_usuario_id()

    ids = request.form.getlist("selecionar_item")
    if not ids:
        item_id = request.form.get("item_id")
        if item_id:
            ids = [item_id]

    if not ids:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "message": "Nenhum item selecionado."})
        flash("Nenhum item selecionado.", "erro")
        return redirect(url_for("carrinho.ver"))

    removidos = carrinho_service.remover_itens(usuario_id, ids)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        itens_restantes = carrinho_service.itens(usuario_id)
        total = carrinho_service.total(usuario_id)
        return jsonify({
            "success": removidos > 0,
            "message": f"{removidos} item(ns) removido(s)!",
            "total_carrinho": f"R$ {total:.2f}",
            "itens_restantes": len(itens_restantes),
        })

    if removidos > 0:
        flash(f"{removidos} item(ns) removido(s)!", "sucesso")
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/carrinho/contador")
def contador():
    usuario_id, is_guest = _get_usuario_id()
    return jsonify({"count": carrinho_service.contador(usuario_id), "is_guest": is_guest})


@carrinho_bp.route("/atualizar_quantidade", methods=["POST"])
@login_required
def atualizar_quantidade():
    usuario_id = str(session["usuario_id"])
    item_id = request.form.get("item_id")
    try:
        nova_quantidade = int(request.form.get("quantidade", 1))
    except (ValueError, TypeError):
        nova_quantidade = 1

    sucesso, mensagem, novo_valor, total_geral = carrinho_service.atualizar_quantidade(
        usuario_id, item_id, nova_quantidade
    )
    return jsonify({
        "success": sucesso,
        "message": mensagem,
        "novo_total_item": f"R$ {novo_valor:.2f}",
        "total_carrinho": f"R$ {total_geral:.2f}",
    })


@carrinho_bp.route("/checkout")
@login_required
def checkout():
    return render_template("checkout.html")


@carrinho_bp.route("/api/carrinho/itens_selecionados", methods=["POST"])
@login_required
def api_itens_selecionados():
    usuario_id = str(session["usuario_id"])
    dados = request.get_json()
    ids = dados.get("itens_selecionados", [])
    itens = carrinho_service.itens_selecionados(usuario_id, ids)
    return jsonify({"itens": itens})


@carrinho_bp.route("/finalizar_compra", methods=["POST"])
@login_required
def finalizar_compra():
    usuario_id = str(session["usuario_id"])
    ids_selecionados = request.form.getlist("selecionar_item")
    codigo_cupom = request.form.get("cupom_aplicado", "").strip().upper()

    try:
        desconto_cupom = float(request.form.get("desconto_cupom", "0"))
    except (ValueError, TypeError):
        desconto_cupom = 0.0

    if not ids_selecionados:
        flash("Nenhum item selecionado.", "erro")
        return redirect(url_for("carrinho.ver"))

    itens = carrinho_service.itens_selecionados(usuario_id, ids_selecionados)

    sucesso, mensagem = venda_service.finalizar_compra(usuario_id, itens, codigo_cupom, desconto_cupom)

    if sucesso:
        # marcar itens como finalizados no carrinho
        from config import Config
        from utils import csv_helper as csv
        from services.carrinho_service import CAMPOS as CARRINHO_CAMPOS
        carrinho = csv.ler(Config.CARRINHO_FILE)
        for item in carrinho:
            if item["id_usuario"] == usuario_id and item["id_carrinho"] in ids_selecionados:
                item["status"] = "finalizado"
        csv.salvar(Config.CARRINHO_FILE, carrinho, CARRINHO_CAMPOS)
        flash(mensagem, "sucesso")
    else:
        flash(mensagem, "erro")

    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/comprar_novamente/<produto_id>")
@login_required
def comprar_novamente(produto_id):
    return redirect(url_for("main.produto", produto_id=produto_id))


@carrinho_bp.route("/meus_pedidos")
@login_required
def meus_pedidos():
    usuario_id = str(session["usuario_id"])
    vendas = venda_service.pedidos_do_usuario(usuario_id)
    return render_template("meus_pedidos.html", vendas=vendas)