import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    PORT = int(os.getenv("PORT", 5000))

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    DATA_DIR = os.path.join(STATIC_DIR, "data")

    USUARIOS_ADM      = os.path.join(DATA_DIR, "usuarios_adm.csv")
    USUARIOS_CLIENTE  = os.path.join(DATA_DIR, "usuarios_clientes.csv")
    CUPONS_FILE       = os.path.join(DATA_DIR, "cupons.csv")
    PRODUTOS_FILE     = os.path.join(DATA_DIR, "produtos.csv")
    CARRINHO_FILE     = os.path.join(DATA_DIR, "carrinho.csv")
    VENDAS_FILE       = os.path.join(DATA_DIR, "vendas.csv")
    DESCONTO_FILE     = os.path.join(DATA_DIR, "descontos.csv")
    ENDERECOS_FILE    = os.path.join(DATA_DIR, "enderecos.csv")

    DESCONTOS_PLANO = {"mensal": 0.00, "semestral": 0.05, "anual": 0.10}
    MULTIPLICADORES_PLANO = {"mensal": 1, "semestral": 6, "anual": 12}