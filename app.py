from flask import Flask
import os
from dotenv import load_dotenv
from routes.views import routes

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurações seguras
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))

    # Registrar rotas
    app.register_blueprint(routes)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway usa essa porta
    app.run(host="0.0.0.0", port=port, debug=True)