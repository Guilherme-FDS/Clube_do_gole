from flask import Blueprint, request, jsonify
from backend.services import cupom_service

cupons_bp = Blueprint("cupons", __name__)

@cupons_bp.route("/validar", methods=["POST"])
def validar():
    codigo = (request.get_json() or {}).get("codigo", "").strip().upper()
    resultado = cupom_service.validar(codigo)
    return jsonify(resultado)

@cupons_bp.route("/aplicar", methods=["POST"])
def aplicar():
    codigo = (request.get_json() or {}).get("codigo", "").strip().upper()
    resultado = cupom_service.aplicar(codigo)
    return jsonify(resultado)