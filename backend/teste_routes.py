# test_routes.py — coloque na pasta backend/ e rode: python test_routes.py
import requests, sys

BASE = "http://127.0.0.1:8000"
OK = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
erros = []

def check(label, method, url, expected, **kwargs):
    try:
        r = getattr(requests, method)(f"{BASE}{url}", timeout=5, **kwargs)
        status = OK if r.status_code == expected else FAIL
        if r.status_code != expected:
            erros.append(f"{label}: esperado {expected}, recebido {r.status_code} — {r.text[:80]}")
        print(f"  {status} [{r.status_code}] {label}")
    except Exception as e:
        print(f"  {FAIL} {label} — ERRO: {e}")
        erros.append(label)

print("\n── Auth ──────────────────────────────────────────")
# Cadastro
check("POST /api/auth/cadastro", "post", "/api/auth/cadastro", 201, json={
    "cpf": "12345678901", "nome": "Teste", "sobrenome": "Script",
    "data_nascimento": "1990-01-01", "email": "teste_script@teste.com",
    "senha": "123456", "telefone": "11999999999"
})

# Login cliente
r = requests.post(f"{BASE}/api/auth/login", json={"email": "teste_script@teste.com", "senha": "123456"})
token_cliente = r.json().get("token", "")
check("POST /api/auth/login (cliente)", "post", "/api/auth/login", 200,
      json={"email": "teste_script@teste.com", "senha": "123456"})

# Login admin (usa credenciais do .env — ajuste se necessário)
r_adm = requests.post(f"{BASE}/api/auth/login", json={"email": "admin@clubedogole.com", "senha": "troque-esta-senha-admin"})
token_admin = r_adm.json().get("token", "")

H_cli = {"Authorization": f"Bearer {token_cliente}"}
H_adm = {"Authorization": f"Bearer {token_admin}"}

check("GET  /api/auth/me", "get", "/api/auth/me", 200, headers=H_cli)
check("POST /api/auth/esqueceu-senha", "post", "/api/auth/esqueceu-senha", 200,
      json={"email": "teste_script@teste.com"})
check("POST /api/auth/redefinir-senha (token inválido → 400)", "post", "/api/auth/redefinir-senha", 400,
      json={"token": "invalido", "nova_senha": "novaSenha123"})

print("\n── Produtos (público) ────────────────────────────")
check("GET  /api/produtos/",       "get", "/api/produtos/", 200)
check("GET  /api/produtos/gold",   "get", "/api/produtos/gold", 200)
check("GET  /api/produtos/premium","get", "/api/produtos/premium", 200)
check("GET  /api/produtos/999 (→ 404)", "get", "/api/produtos/999", 404)

print("\n── Cupons ────────────────────────────────────────")
check("POST /api/cupons/validar (inválido)", "post", "/api/cupons/validar", 200,
      json={"codigo": "INEXISTENTE"})

print("\n── Admin ─────────────────────────────────────────")
check("GET  /api/admin/dashboard",  "get", "/api/admin/dashboard", 200, headers=H_adm)
check("GET  /api/admin/clientes",   "get", "/api/admin/clientes", 200, headers=H_adm)
check("GET  /api/admin/clientes/1", "get", "/api/admin/clientes/1", 200, headers=H_adm)
check("GET  /api/admin/produtos",   "get", "/api/admin/produtos", 200, headers=H_adm)
check("GET  /api/admin/cupons",     "get", "/api/admin/cupons", 200, headers=H_adm)
check("GET  /api/admin/clientes (sem token → 401)", "get", "/api/admin/clientes", 401)
check("GET  /api/admin/clientes (token cliente → 403)", "get", "/api/admin/clientes", 403, headers=H_cli)

print("\n── Configurações ─────────────────────────────────")
check("GET  /api/configuracoes/perfil",    "get", "/api/configuracoes/perfil", 200, headers=H_cli)
check("GET  /api/configuracoes/enderecos", "get", "/api/configuracoes/enderecos", 200, headers=H_cli)
check("GET  /api/configuracoes/perfil (sem token → 401)", "get", "/api/configuracoes/perfil", 401)

print("\n── Carrinho ──────────────────────────────────────")
check("GET  /api/carrinho/ (sem token → 401)", "get", "/api/carrinho/", 401)
check("GET  /api/carrinho/", "get", "/api/carrinho/", 200, headers=H_cli)

print("\n─────────────────────────────────────────────────")
if erros:
    print(f"\n{FAIL} {len(erros)} erro(s):")
    for e in erros: print(f"   • {e}")
    sys.exit(1)
else:
    print(f"\n{OK} Todas as rotas OK!")