import sys, os

# Garante que backend/ está no path — resolve os imports 'from services/utils/routes'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', app.config['SECRET_KEY'])

    CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGIN", "http://localhost:5173")}})

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.produtos import produtos_bp
    from routes.carrinho import carrinho_bp
    from routes.cupons import cupons_bp
    from routes.configuracoes import configuracoes_bp

    app.register_blueprint(auth_bp,          url_prefix="/api/auth")
    app.register_blueprint(admin_bp,         url_prefix="/api/admin")
    app.register_blueprint(produtos_bp,      url_prefix="/api/produtos")
    app.register_blueprint(carrinho_bp,      url_prefix="/api/carrinho")
    app.register_blueprint(cupons_bp,        url_prefix="/api/cupons")
    app.register_blueprint(configuracoes_bp, url_prefix="/api/configuracoes")

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)