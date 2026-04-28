import jwt, os, datetime
from functools import wraps
from flask import request, jsonify, current_app

def _get_token():
    h = request.headers.get("Authorization", "")
    return h[7:] if h.startswith("Bearer ") else None

def _decode(token):
    try:
        return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
    except:
        return None

def gerar_token(payload: dict) -> str:
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    return jwt.encode(payload, os.getenv("JWT_SECRET", "dev-secret"), algorithm="HS256")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = _decode(_get_token() or "")
        if not payload:
            return jsonify({"error": "Token inválido ou ausente"}), 401
        request.usuario = payload
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = _decode(_get_token() or "")
        if not payload:
            return jsonify({"error": "Token ausente"}), 401
        if payload.get("tipo") != "admin":
            return jsonify({"error": "Acesso negado"}), 403
        request.usuario = payload
        return f(*args, **kwargs)
    return decorated