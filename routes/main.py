from flask import Blueprint, render_template, flash, redirect, url_for
from services import produto_service

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template(
        "index.html",
        produtos_gold=produto_service.listar_por_tipo("gold"),
        produtos_premium=produto_service.listar_por_tipo("premium"),
    )

@main_bp.route("/produto/<produto_id>")
def produto(produto_id):
    p = produto_service.buscar_por_id(produto_id)
    if not p:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("main.index"))
    return render_template("produto_generico.html", produto=p)

@main_bp.route("/mixupcode")
def mixupcode():
    return render_template("mixupcode.html")