from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth import admin_required
from services import produto_service, cupom_service, venda_service
from utils import csv_helper as csv
from config import Config

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def painel():
    return render_template(
        "usuario_adm.html",
        cupons=cupom_service.listar_todos(),
        produtos=produto_service.listar_todos(),
    )


# ── Produtos ──────────────────────────────────────────────────────────────────

@admin_bp.route("/produtos")
@admin_required
def produtos():
    return render_template("produtos.html", produtos=produto_service.listar_todos())


@admin_bp.route("/produtos/adicionar", methods=["POST"])
@admin_required
def adicionar_produto():
    imagem = request.form.get("imagem_base64", "").strip() or request.form.get("imagem", "").strip()
    produto_service.adicionar({
        "nome":      request.form.get("nome"),
        "tipo":      request.form.get("tipo"),
        "descricao": request.form.get("descricao"),
        "preco":     request.form.get("preco"),
        "imagem":    imagem,
        "estoque":   request.form.get("estoque", "0"),
    })
    flash("Produto adicionado!", "sucesso")
    return redirect(url_for("admin.produtos"))


@admin_bp.route("/produtos/editar/<produto_id>", methods=["GET", "POST"])
@admin_required
def editar_produto(produto_id):
    produto = produto_service.buscar_por_id(produto_id)
    if not produto:
        flash("Produto não encontrado!", "erro")
        return redirect(url_for("admin.produtos"))

    if request.method == "POST":
        imagem = (
            request.form.get("imagem_base64", "").strip()
            or request.form.get("imagem", "").strip()
            or produto.get("imagem", "")
        )
        produto_service.atualizar(produto_id, {
            "nome":      request.form.get("nome"),
            "tipo":      request.form.get("tipo"),
            "descricao": request.form.get("descricao"),
            "preco":     request.form.get("preco"),
            "imagem":    imagem,
            "estoque":   request.form.get("estoque", "0"),
        })
        flash("Produto atualizado!", "sucesso")
        return redirect(url_for("admin.produtos"))

    return render_template("editar_produto.html", produto=produto)


@admin_bp.route("/produtos/deletar/<produto_id>")
@admin_required
def deletar_produto(produto_id):
    produto_service.remover(produto_id)
    flash("Produto deletado!", "sucesso")
    return redirect(url_for("admin.produtos"))


# ── Cupons ────────────────────────────────────────────────────────────────────

@admin_bp.route("/cupons")
@admin_required
def cupons():
    return render_template("cupons.html", cupons=cupom_service.listar_todos())


@admin_bp.route("/cupons/adicionar", methods=["POST"])
@admin_required
def adicionar_cupom():
    usos = request.form.get("usos_maximos", "1").strip()
    cupom_service.adicionar({
        "codigo":               request.form.get("codigo", "").strip().upper(),
        "desconto_percentual":  request.form.get("desconto_percentual", "0").strip(),
        "usos_maximos":         usos,
        "usos_restantes":       usos,
        "status":               request.form.get("status", "ativo"),
    })
    flash("Cupom adicionado com sucesso!", "sucesso")
    return redirect(url_for("admin.cupons"))


@admin_bp.route("/cupons/editar/<cupom_id>", methods=["GET", "POST"])
@admin_required
def editar_cupom(cupom_id):
    cupom = cupom_service.buscar_por_id(cupom_id)
    if not cupom:
        flash("Cupom não encontrado.", "erro")
        return redirect(url_for("admin.cupons"))

    if request.method == "POST":
        novos_maximos = request.form.get("usos_maximos", cupom.get("usos_maximos", "1")).strip()
        usos_atuais = int(cupom.get("usos_maximos", 1)) - int(cupom.get("usos_restantes", 1))
        usos_restantes = str(max(0, int(novos_maximos) - usos_atuais))

        cupom_service.atualizar(cupom_id, {
            "codigo":               request.form.get("codigo", "").strip().upper(),
            "desconto_percentual":  request.form.get("desconto_percentual", "0").strip(),
            "usos_maximos":         novos_maximos,
            "usos_restantes":       usos_restantes,
            "status":               request.form.get("status", "ativo"),
        })
        flash("Cupom atualizado com sucesso!", "sucesso")
        return redirect(url_for("admin.cupons"))

    return render_template("editar_cupom.html", cupom=cupom)


@admin_bp.route("/cupons/remover/<cupom_id>")
@admin_required
def remover_cupom(cupom_id):
    cupom_service.remover(cupom_id)
    flash("Cupom removido.", "sucesso")
    return redirect(url_for("admin.cupons"))


@admin_bp.route("/cupons/status/<cupom_id>/<novo_status>")
@admin_required
def alterar_status_cupom(cupom_id, novo_status):
    cupom_service.alterar_status(cupom_id, novo_status)
    flash(f"Cupom {novo_status} com sucesso!", "sucesso")
    return redirect(url_for("admin.cupons"))


# ── Dashboard / Vendas ────────────────────────────────────────────────────────

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return render_template("dashboard_vendas.html", **venda_service.dados_dashboard())


@admin_bp.route("/vendas/<venda_id>")
@admin_required
def detalhes_venda(venda_id):
    venda = venda_service.buscar_venda(venda_id)
    if not venda:
        flash("Venda não encontrada.", "erro")
        return redirect(url_for("admin.dashboard"))
    return render_template("detalhes_venda.html", venda=venda)