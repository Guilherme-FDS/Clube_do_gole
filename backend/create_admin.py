# backend/create_admin.py
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.engine import get_db
from database.models import UsuarioAdm
from sqlalchemy import select
import bcrypt

async def criar_admin(nome: str, email: str, senha: str):
    async for db in get_db():
        existe = await db.scalar(select(UsuarioAdm).where(UsuarioAdm.email == email))
        if existe:
            print(f"Admin com email '{email}' já existe.")
            return

        hash_senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        admin = UsuarioAdm(nome=nome, email=email, senha=hash_senha, tipo="admin")
        db.add(admin)
        await db.commit()
        print(f"Admin '{nome}' criado com sucesso.")

if __name__ == "__main__":
    nome  = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    asyncio.run(criar_admin(nome, email, senha))