from flask import Blueprint, jsonify
from backend.services import produto_service

produtos_bp = Blueprint("produtos", __name__)

@produtos_bp.route("/")
def listar():
    return jsonify(produto_service.listar_todos())

@produtos_bp.route("/gold")
def gold():
    return jsonify(produto_service.listar_por_tipo("gold"))

@produtos_bp.route("/premium")
def premium():
    return jsonify(produto_service.listar_por_tipo("premium"))

@produtos_bp.route("/<produto_id>")
def detalhe(produto_id):
    p = produto_service.buscar_por_id(produto_id)
    if not p:
        return jsonify({"error": "Produto não encontrado"}), 404
    return jsonify(p)