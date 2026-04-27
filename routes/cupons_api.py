from flask import Blueprint, request, jsonify
from services import cupom_service

cupons_api_bp = Blueprint("cupons_api", __name__, url_prefix="/api/cupons")


@cupons_api_bp.route("/validar", methods=["POST"])
def validar():
    try:
        dados = request.get_json()
        codigo = dados.get("codigo", "").strip().upper()
        if not codigo:
            return jsonify({"valido": False, "mensagem": "Código não informado."})

        valido, mensagem, desconto = cupom_service.validar(codigo)
        cupom = cupom_service.buscar_por_codigo(codigo) if valido else None

        return jsonify({
            "valido": valido,
            "mensagem": mensagem,
            "desconto": desconto,
            "id_cupom": cupom.get("id") if cupom else None,
        })
    except Exception as e:
        return jsonify({"valido": False, "mensagem": "Erro ao validar cupom."})


@cupons_api_bp.route("/aplicar", methods=["POST"])
def aplicar():
    try:
        dados = request.get_json()
        codigo = dados.get("codigo", "").strip().upper()
        if not codigo:
            return jsonify({"sucesso": False, "mensagem": "Código não informado."})

        sucesso = cupom_service.consumir(codigo)
        if sucesso:
            return jsonify({"sucesso": True, "mensagem": "Cupom aplicado com sucesso!"})
        return jsonify({"sucesso": False, "mensagem": "Cupom inválido ou esgotado."})
    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": "Erro ao aplicar cupom."})