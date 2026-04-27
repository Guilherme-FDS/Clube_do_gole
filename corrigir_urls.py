"""
Clube do Gole — Correção de url_for nos templates
Execute na RAIZ do projeto (onde está app.py):
    python corrigir_urls.py
"""
import os
import re

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

SUBSTITUICOES = [
    # auth
    ("routes.login",                      "auth.login"),
    ("routes.logout",                     "auth.logout"),
    ("routes.cadastro",                   "auth.cadastro"),
    # main
    ("routes.index",                      "main.index"),
    ("routes.mixupcode",                  "main.mixupcode"),
    ("routes.produto",                    "main.produto"),
    # admin - painel
    ("routes.usuario_adm",                "admin.painel"),
    # admin - produtos
    ("routes.produtos",                   "admin.produtos"),
    ("routes.adicionar_produto",          "admin.adicionar_produto"),
    ("routes.editar_produto",             "admin.editar_produto"),
    ("routes.deletar_produto",            "admin.deletar_produto"),
    # admin - cupons
    ("routes.cupons",                     "admin.cupons"),
    ("routes.adicionar_cupom",            "admin.adicionar_cupom"),
    ("routes.editar_cupom",               "admin.editar_cupom"),
    ("routes.remover_cupom",              "admin.remover_cupom"),
    ("routes.alterar_status_cupom",       "admin.alterar_status_cupom"),
    # admin - vendas/dashboard
    ("routes.dashboard_vendas",           "admin.dashboard"),
    ("routes.detalhes_venda",             "admin.detalhes_venda"),
    # carrinho
    ("routes.carrinho",                   "carrinho.ver"),
    ("routes.adicionar_carrinho",         "carrinho.adicionar"),
    ("routes.finalizar_compra",           "carrinho.finalizar_compra"),
    ("routes.meus_pedidos",               "carrinho.meus_pedidos"),
    ("routes.checkout",                   "carrinho.checkout"),
    ("routes.comprar_novamente",          "carrinho.comprar_novamente"),
    # configuracoes
    ("routes.configuracoes",              "configuracoes.configuracoes"),
    ("routes.atualizar_perfil",           "configuracoes.atualizar_perfil"),
    ("routes.alterar_senha",              "configuracoes.alterar_senha"),
    ("routes.adicionar_endereco",         "configuracoes.adicionar_endereco"),
    ("routes.editar_endereco",            "configuracoes.editar_endereco"),
    ("routes.excluir_endereco",           "configuracoes.excluir_endereco"),
    ("routes.definir_endereco_principal", "configuracoes.definir_endereco_principal"),
]


def corrigir_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    original = conteudo
    for antigo, novo in SUBSTITUICOES:
        conteudo = conteudo.replace(antigo, novo)
    if conteudo != original:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return True
    return False


def main():
    if not os.path.isdir(TEMPLATES_DIR):
        print(f"❌ Pasta 'templates' não encontrada em: {TEMPLATES_DIR}")
        print("   Execute este script na raiz do projeto (onde está o app.py).")
        return

    alterados = []
    for root, _, files in os.walk(TEMPLATES_DIR):
        for nome in files:
            if nome.endswith(".html"):
                caminho = os.path.join(root, nome)
                if corrigir_arquivo(caminho):
                    alterados.append(caminho.replace(TEMPLATES_DIR + os.sep, "templates/"))

    if alterados:
        print(f"✅ {len(alterados)} arquivo(s) corrigido(s):")
        for a in alterados:
            print(f"   → {a}")
    else:
        print("ℹ️  Nenhum arquivo precisou ser alterado (já estão corretos).")


if __name__ == "__main__":
    main()