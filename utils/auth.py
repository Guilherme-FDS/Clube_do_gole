from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Você precisa estar logado.", "erro")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("tipo") != "admin":
            flash("Acesso restrito a administradores.", "erro")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated