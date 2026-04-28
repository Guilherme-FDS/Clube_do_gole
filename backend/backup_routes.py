from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import csv
import os
import uuid
import sys
from datetime import datetime

# ==============================
# SOLUÇÃO PARA ERRO CSV TAMANHO DE IMAGEM NO ADICIONAR PRODUTOS
# ==============================
csv.field_size_limit(10 * 1024 * 1024)  # Aumenta limite para 10MB

routes = Blueprint("routes", __name__)

# ==============================
# Caminhos dos arquivos CSV
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # pasta /routes
PROJECT_ROOT = os.path.dirname(BASE_DIR)                # sobe 1 nível (raiz do projeto)
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")
DATA_DIR = os.path.join(STATIC_DIR, "data")

USUARIOS_ADM = os.path.join(DATA_DIR, "usuarios_adm.csv")
USUARIOS_CLIENTE = os.path.join(DATA_DIR, "usuarios_clientes.csv")
CUPONS_FILE = os.path.join(DATA_DIR, "cupons.csv")
PRODUTOS_FILE = os.path.join(DATA_DIR, "produtos.csv")
CARRINHO_FILE = os.path.join(DATA_DIR, "carrinho.csv")
VENDAS_FILE = os.path.join(DATA_DIR, "vendas.csv")
DESCONTO_FILE = os.path.join(DATA_DIR, "descontos.csv")
ENDERECOS_FILE = os.path.join(DATA_DIR, "enderecos.csv")

# ==============================
# Funções utilitárias
# ==============================
def garantir_arquivo_com_cabecalho(path, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def carregar_csv_seguro(caminho):
    """Carrega CSV com tratamento de erros para campos grandes (Base64)"""
    if not os.path.exists(caminho):
        return []
    
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return []
            
            lines = content.splitlines()
            if not lines:
                return []
            
            headers = [h.strip('"') for h in lines[0].split(',')]
            dados = []
            
            for line in lines[1:]:
                if not line.strip():
                    continue
                
                values = []
                current_value = []
                in_quotes = False
                
                for char in line:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        values.append(''.join(current_value).strip('"'))
                        current_value = []
                    else:
                        current_value.append(char)
                
                values.append(''.join(current_value).strip('"'))
                
                if len(values) == len(headers):
                    row = dict(zip(headers, values))
                    dados.append(row)
            
            return dados
            
    except Exception as e:
        print(f"❌ ERRO ao ler CSV {caminho}: {e}")
        try:
            with open(caminho, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except:
            return []

def salvar_csv_seguro(caminho, dados, campos):
    """Salva CSV com campos grandes de forma segura"""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(','.join(f'"{campo}"' for campo in campos) + '\n')
            
            for linha in dados:
                valores = []
                for campo in campos:
                    valor = str(linha.get(campo, ''))
                    if ',' in valor or '\n' in valor or '"' in valor:
                        valor = valor.replace('"', '""')
                        valor = f'"{valor}"'
                    valores.append(valor)
                f.write(','.join(valores) + '\n')
                
    except Exception as e:
        print(f"❌ ERRO ao salvar CSV {caminho}: {e}")
        try:
            with open(caminho, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                for linha in dados:
                    linha_filtrada = {campo: linha.get(campo, '') for campo in campos}
                    writer.writerow(linha_filtrada)
        except Exception as e2:
            print(f"❌ ERRO CRÍTICO ao salvar CSV: {e2}")

def carregar_csv(caminho):
    return carregar_csv_seguro(caminho)

def salvar_csv(caminho, dados, campos):
    salvar_csv_seguro(caminho, dados, campos)

def gerar_id_auto(dados, campo="id"):
    """Gera próximo id numérico para o campo informado"""
    if not dados:
        return "1"
    try:
        ids = []
        for d in dados:
            v = d.get(campo)
            if v is None:
                continue
            if isinstance(v, str) and v.isdigit():
                ids.append(int(v))
            elif isinstance(v, int):
                ids.append(v)
        return str(max(ids) + 1) if ids else "1"
    except Exception:
        return str(len(dados) + 1)

# ==============================
# Garantir arquivos
# ==============================
garantir_arquivo_com_cabecalho(USUARIOS_ADM, ["id", "nome", "email", "senha", "tipo"])
garantir_arquivo_com_cabecalho(USUARIOS_CLIENTE, ["id", "cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"])
garantir_arquivo_com_cabecalho(CUPONS_FILE, ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"])
garantir_arquivo_com_cabecalho(PRODUTOS_FILE, ["id", "nome", "tipo", "descricao", "preco", "imagem", "estoque"])
garantir_arquivo_com_cabecalho(CARRINHO_FILE, ["id_carrinho","id_usuario","id_produto","nome_produto","descricao","plano","quantidade","valor_unitario","valor_total","status"])
garantir_arquivo_com_cabecalho(VENDAS_FILE, [ "id_compra", "id_usuario", "id_produto", "quantidade","valor_original", "valor_desconto", "valor_total", "data","plano", "desconto_aplicado", "cupom_aplicado"])
garantir_arquivo_com_cabecalho(DESCONTO_FILE, ["id","plano","descontos"])
garantir_arquivo_com_cabecalho(ENDERECOS_FILE, ["id", "id_cliente", "tipo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "pais", "principal"])

# ==============================
# CONSTANTES E CAMPOS FIXOS
# ==============================
CARRINHO_FIELDS = [
    "id_carrinho", "id_usuario", "id_produto", "nome_produto",
    "descricao", "plano", "quantidade", "valor_unitario",
    "valor_total", "status"
]

# ==============================
# INDEX
# ==============================
@routes.route("/")
def index():
    produtos_gold = []
    produtos_premium = []

    produtos_csv = os.path.join(STATIC_DIR, "data", "produtos.csv")

    if os.path.exists(produtos_csv):
        try:
            produtos = carregar_csv_seguro(produtos_csv)
            for linha in produtos:
                if linha.get("tipo", "").strip().lower() == "gold":
                    produtos_gold.append(linha)
                elif linha.get("tipo", "").strip().lower() == "premium":
                    produtos_premium.append(linha)
        except Exception as e:
            print(f"❌ ERRO ao carregar produtos para index: {e}")

    return render_template(
        "index.html",
        produtos_gold=produtos_gold,
        produtos_premium=produtos_premium
    )

# ==============================
# FUNÇÕES PARA MIGRAÇÃO DO CARRINHO GUEST
# ==============================
def migrar_carrinho_guest_para_usuario(usuario_id):
    """Migra itens do carrinho guest para o usuário logado"""
    if "guest_id" in session:
        guest_id = f"guest_{session['guest_id']}"
        carrinho = carregar_csv(CARRINHO_FILE)
        
        itens_migrados = 0
        for item in carrinho:
            if item["id_usuario"] == guest_id and item["status"] == "em processo":
                item["id_usuario"] = usuario_id
                itens_migrados += 1
        
        if itens_migrados > 0:
            salvar_csv(CARRINHO_FILE, carrinho, CARRINHO_FIELDS)
            print(f"🔄 Migrados {itens_migrados} itens do carrinho guest para usuário {usuario_id}")
        
        # Remove a sessão guest
        session.pop("guest_id", None)
        return itens_migrados
    return 0

def usuario_tem_itens_no_carrinho(usuario_id):
    """Verifica se o usuário tem itens no carrinho"""
    carrinho = carregar_csv(CARRINHO_FILE)
    itens_usuario = [
        item for item in carrinho 
        if item["id_usuario"] == usuario_id and item["status"] == "em processo"
    ]
    return len(itens_usuario) > 0

# ==============================
# LOGIN / LOGOUT / CADASTRO
# ==============================
@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()

        if not email or not senha:
            flash("Preencha todos os campos!", "erro")
            return redirect(url_for("routes.login"))

        admins = carregar_csv(USUARIOS_ADM)
        for adm in admins:
            if adm.get("email") == email and adm.get("senha") == senha:
                session["usuario_id"] = adm.get("id")
                session["email"] = adm.get("email")
                session["tipo"] = "admin"
                session["usuario_nome"] = adm.get("nome")
                flash("Login de administrador realizado!", "sucesso")
                return redirect(url_for("routes.usuario_adm"))

        clientes = carregar_csv(USUARIOS_CLIENTE)
        for c in clientes:
            if c.get("email") == email and c.get("senha") == senha:
                usuario_id = c.get("id")
                
                # MIGRAR CARRINHO ANTES DE SETAR A SESSÃO
                itens_migrados = migrar_carrinho_guest_para_usuario(usuario_id)
                
                # Configurar sessão do usuário
                session["usuario_id"] = usuario_id
                session["email"] = c.get("email")
                session["tipo"] = "cliente"
                session["usuario_nome"] = c.get("nome")
                session["primeiro_nome"] = c.get("nome").split()[0]
                
                # VERIFICAR REDIRECT PARAM E ITENS NO CARRINHO
                redirect_to = request.args.get('redirect')
                tem_itens_carrinho = usuario_tem_itens_no_carrinho(usuario_id)
                
                # LÓGICA DE REDIRECIONAMENTO INTELIGENTE
                if itens_migrados > 0:
                    flash(f"Login realizado com sucesso! {itens_migrados} item(ns) do seu carrinho foram recuperados.", "sucesso")
                    
                    # Prioridade 1: Se veio do checkout ou carrinho, vai para carrinho
                    if redirect_to in ['checkout', 'carrinho']:
                        return redirect(url_for("routes.carrinho"))
                    # Prioridade 2: Se tem itens migrados, vai para carrinho
                    return redirect(url_for("routes.carrinho"))
                
                elif tem_itens_carrinho:
                    flash("Login realizado com sucesso! Seu carrinho foi mantido.", "sucesso")
                    
                    # Se tem itens no carrinho (de login anterior), vai para carrinho
                    if redirect_to in ['checkout', 'carrinho']:
                        return redirect(url_for("routes.carrinho"))
                    return redirect(url_for("routes.carrinho"))
                
                else:
                    flash("Login realizado com sucesso!", "sucesso")
                    
                    # Se veio do checkout sem itens, vai para carrinho
                    if redirect_to == 'checkout':
                        return redirect(url_for("routes.carrinho"))
                    # Se não tem itens, vai para index
                    return redirect(url_for("routes.index"))

        flash("E-mail ou senha inválidos!", "erro")
        return redirect(url_for("routes.login"))

    return render_template("login.html")

@routes.route("/logout")
def logout():
    # Limpa apenas os itens do usuário logado, não dos guests
    if "usuario_id" in session:
        usuario_id = str(session["usuario_id"])
        carrinho = carregar_csv(CARRINHO_FILE)
        
        # Remove apenas os itens deste usuário
        carrinho_atualizado = [
            item for item in carrinho 
            if item["id_usuario"] != usuario_id or item["status"] != "em processo"
        ]
        
        itens_removidos = len(carrinho) - len(carrinho_atualizado)
        if itens_removidos > 0:
            salvar_csv(CARRINHO_FILE, carrinho_atualizado, CARRINHO_FIELDS)
            print(f"🗑️ {itens_removidos} itens removidos do carrinho do usuário {usuario_id}")
    
    session.clear()
    flash("Você saiu da sua conta. Seu carrinho foi limpo.", "sucesso")
    return redirect(url_for("routes.index"))

@routes.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        campos = {
            "cpf": request.form.get("cpf", "").strip(),
            "nome": request.form.get("nome", "").strip(),
            "sobrenome": request.form.get("sobrenome", "").strip(),
            "data_nascimento": request.form.get("data_nascimento", "").strip(),
            "email": request.form.get("email", "").strip().lower(),
            "senha": request.form.get("senha", "").strip(),
            "telefone": request.form.get("telefone", "").strip(),
        }
        
        campos_obrigatorios = ["cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"]
        campos_faltantes = [campo for campo in campos_obrigatorios if not campos[campo]]
        
        if campos_faltantes:
            flash(f"Preencha todos os campos obrigatórios!", "erro")
            return redirect(url_for("routes.cadastro"))

        clientes = carregar_csv(USUARIOS_CLIENTE)
        if any(u.get("email") == campos["email"] for u in clientes):
            flash("E-mail já cadastrado!", "erro")
            return redirect(url_for("routes.cadastro"))

        if any(u.get("cpf") == campos["cpf"] for u in clientes):
            flash("CPF já cadastrado!", "erro")
            return redirect(url_for("routes.cadastro"))

        campos["id"] = gerar_id_auto(clientes)
        clientes.append(campos)
        
        fieldnames = ["id", "cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"]
        
        salvar_csv(USUARIOS_CLIENTE, clientes, fieldnames)
        flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
        return redirect(url_for("routes.login"))
    
    return render_template("cadastro.html")

# ==============================
# ADMINISTRADOR
# ==============================
@routes.route("/usuario_adm")
def usuario_adm():
    if session.get("tipo") != "admin":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("routes.index"))

    cupons = carregar_csv(CUPONS_FILE)
    produtos = carregar_csv(PRODUTOS_FILE)
    return render_template("usuario_adm.html", cupons=cupons, produtos=produtos)

# ==============================
# CUPONS - CRUD
# ==============================
@routes.route("/cupons")
def cupons():
    if session.get("tipo") != "admin":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("routes.index"))

    cupons = carregar_csv(CUPONS_FILE)
    for cupom in cupons:
        try:
            cupom["usos_restantes"] = int(cupom.get("usos_restantes", 0))
            cupom["desconto_percentual"] = float(cupom.get("desconto_percentual", 0))
        except (ValueError, TypeError):
            cupom["usos_restantes"] = 0
            cupom["desconto_percentual"] = 0

    return render_template("cupons.html", cupons=cupons)

@routes.route("/cupons/adicionar", methods=["POST"])
def adicionar_cupom():
    if session.get("tipo") != "admin":
        flash("Acesso negado.", "erro")
        return redirect(url_for("routes.index"))

    dados = carregar_csv(CUPONS_FILE)
    novo = {
        "id": gerar_id_auto(dados),
        "codigo": request.form.get("codigo", "").strip().upper(),
        "desconto_percentual": request.form.get("desconto_percentual", "0").strip(),
        "usos_maximos": request.form.get("usos_maximos", "1").strip(),
        "usos_restantes": request.form.get("usos_maximos", "1").strip(),
        "status": request.form.get("status", "ativo")
    }
    dados.append(novo)
    salvar_csv(CUPONS_FILE, dados, ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"])
    flash("Cupom adicionado com sucesso!", "sucesso")
    return redirect(url_for("routes.cupons"))

@routes.route("/cupons/remover/<cupom_id>")
def remover_cupom(cupom_id):
    if session.get("tipo") != "admin":
        flash("Acesso negado.", "erro")
        return redirect(url_for("routes.index"))

    dados = carregar_csv(CUPONS_FILE)
    dados = [d for d in dados if d.get("id") != cupom_id]
    salvar_csv(CUPONS_FILE, dados, ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"])
    flash("Cupom removido.", "sucesso")
    return redirect(url_for("routes.cupons"))

@routes.route("/cupons/editar/<cupom_id>", methods=["GET", "POST"])
def editar_cupom(cupom_id):
    if session.get("tipo") != "admin":
        flash("Acesso negado.", "erro")
        return redirect(url_for("routes.index"))

    dados = carregar_csv(CUPONS_FILE)
    cupom = next((d for d in dados if d["id"] == cupom_id), None)
    if not cupom:
        flash("Cupom não encontrado.", "erro")
        return redirect(url_for("routes.cupons"))

    if request.method == "POST":
        cupom["codigo"] = request.form.get("codigo", cupom.get("codigo", "")).strip().upper()
        cupom["desconto_percentual"] = request.form.get("desconto_percentual", cupom.get("desconto_percentual", "0")).strip()
        
        novos_usos_maximos = request.form.get("usos_maximos", cupom.get("usos_maximos", "1")).strip()
        cupom["usos_maximos"] = novos_usos_maximos
        
        usos_atuais = int(cupom.get("usos_maximos", "1")) - int(cupom.get("usos_restantes", "1"))
        cupom["usos_restantes"] = str(max(0, int(novos_usos_maximos) - usos_atuais))
        
        cupom["status"] = request.form.get("status", cupom.get("status", "ativo"))

        salvar_csv(CUPONS_FILE, dados, ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"])
        flash("Cupom atualizado com sucesso!", "sucesso")
        return redirect(url_for("routes.cupons"))

    return render_template("editar_cupom.html", cupom=cupom)

@routes.route("/cupons/alterar_status/<cupom_id>/<novo_status>")
def alterar_status_cupom(cupom_id, novo_status):
    if session.get("tipo") != "admin":
        flash("Acesso negado.", "erro")
        return redirect(url_for("routes.index"))

    try:
        cupons = carregar_csv(CUPONS_FILE)
        cupom = next((c for c in cupons if c["id"] == cupom_id), None)
        
        if not cupom:
            flash("Cupom não encontrado.", "erro")
            return redirect(url_for("routes.cupons"))
        
        cupom["status"] = novo_status
        salvar_csv(CUPONS_FILE, cupons, ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"])
        
        flash(f"Cupom {novo_status} com sucesso!", "sucesso")
        return redirect(url_for("routes.cupons"))
        
    except Exception as e:
        print(f"❌ ERRO em alterar_status_cupom: {str(e)}")
        flash("Erro ao alterar status do cupom.", "erro")
        return redirect(url_for("routes.cupons"))

# ==============================
# API PARA VALIDAR CUPOM NO CHECKOUT
# ==============================
@routes.route("/api/cupons/validar", methods=["POST"])
def validar_cupom():
    try:
        dados = request.get_json()
        codigo_cupom = dados.get("codigo", "").strip().upper()
        
        if not codigo_cupom:
            return jsonify({"valido": False, "mensagem": "Código do cupom não informado."})
        
        cupons = carregar_csv(CUPONS_FILE)
        cupom = next((c for c in cupons if c.get("codigo") == codigo_cupom), None)
        
        if not cupom:
            return jsonify({"valido": False, "mensagem": "Cupom inválido."})
        
        if cupom.get("status") != "ativo":
            return jsonify({"valido": False, "mensagem": "Cupom inativo."})
        
        usos_restantes = int(cupom.get("usos_restantes", 0))
        if usos_restantes <= 0:
            return jsonify({"valido": False, "mensagem": "Cupom esgotado."})
        
        desconto = float(cupom.get("desconto_percentual", 0))
        return jsonify({
            "valido": True, 
            "mensagem": f"Cupom aplicado! {desconto}% de desconto.",
            "desconto": desconto,
            "id_cupom": cupom.get("id")
        })
        
    except Exception as e:
        print(f"❌ ERRO em validar_cupom: {str(e)}")
        return jsonify({"valido": False, "mensagem": "Erro ao validar cupom."})

@routes.route("/api/cupons/aplicar", methods=["POST"])
def aplicar_cupom():
    try:
        dados = request.get_json()
        id_cupom = dados.get("id_cupom")
        
        if not id_cupom:
            return jsonify({"sucesso": False, "mensagem": "ID do cupom não informado."})
        
        cupons = carregar_csv(CUPONS_FILE)
        cupom = next((c for c in cupons if c.get("id") == id_cupom), None)
        
        if not cupom:
            return jsonify({"sucesso": False, "mensagem": "Cupom não encontrado."})
        
        usos_restantes = int(cupom.get("usos_restantes", 1))
        if usos_restantes > 0:
            cupom["usos_restantes"] = str(usos_restantes - 1)
            salvar_csv(CUPONS_FILE, cupons, ["id", "codigo", "desconto_percentual", "usos_maximos", "usos_restantes", "status"])
            return jsonify({"sucesso": True, "mensagem": "Cupom aplicado com sucesso!"})
        else:
            return jsonify({"sucesso": False, "mensagem": "Cupom esgotado."})
            
    except Exception as e:
        print(f"❌ ERRO em aplicar_cupom: {str(e)}")
        return jsonify({"sucesso": False, "mensagem": "Erro ao aplicar cupom."})

# ==============================
# PRODUTOS - CRUD
# ==============================
@routes.route("/produtos")
def produtos():
    if session.get("tipo") != "admin":
        flash("Acesso negado.", "erro")
        return redirect(url_for("routes.index"))
    dados = carregar_csv(PRODUTOS_FILE)
    return render_template("produtos.html", produtos=dados)

@routes.route("/adicionar_produto", methods=["POST"])
def adicionar_produto():
    dados = carregar_csv(PRODUTOS_FILE)
    
    imagem_base64 = request.form.get("imagem_base64", "").strip()
    imagem_url = request.form.get("imagem", "").strip()
    
    if imagem_base64:
        imagem_final = imagem_base64
    elif imagem_url:
        imagem_final = imagem_url
    else:
        imagem_final = ""
    
    novo = {
        "id": gerar_id_auto(dados),
        "nome": request.form.get("nome"),
        "tipo": request.form.get("tipo"),
        "descricao": request.form.get("descricao"),
        "preco": request.form.get("preco"),
        "imagem": imagem_final,
        "estoque": request.form.get("estoque", "0")
    }

    dados.append(novo)
    salvar_csv(PRODUTOS_FILE, dados, ["id","nome","tipo","descricao","preco","imagem","estoque"])
    flash("Produto adicionado!", "sucesso")
    return redirect(url_for("routes.produtos"))

@routes.route("/editar_produto/<id>", methods=["GET", "POST"])
def editar_produto(id):
    dados = carregar_csv(PRODUTOS_FILE)

    produto = None
    for item in dados:
        if item["id"] == id:
            produto = item
            break

    if not produto:
        flash("Produto não encontrado!", "erro")
        return redirect(url_for("routes.produtos"))

    if request.method == "POST":
        imagem_base64 = request.form.get("imagem_base64", "").strip()
        imagem_url = request.form.get("imagem", "").strip()
        
        if imagem_base64:
            imagem_final = imagem_base64
        elif imagem_url:
            imagem_final = imagem_url
        else:
            imagem_final = produto.get("imagem", "")
        
        produto.update({
            "nome": request.form.get("nome"),
            "tipo": request.form.get("tipo"),
            "descricao": request.form.get("descricao"),
            "preco": request.form.get("preco"),
            "imagem": imagem_final,
            "estoque": request.form.get("estoque", "0")
        })
        salvar_csv(PRODUTOS_FILE, dados, ["id", "nome", "tipo", "descricao", "preco", "imagem", "estoque"])
        flash("Produto atualizado!", "sucesso")
        return redirect(url_for("routes.produtos"))

    return render_template("editar_produto.html", produto=produto)

@routes.route("/deletar_produto/<id>")
def deletar_produto(id):
    dados = [i for i in carregar_csv(PRODUTOS_FILE) if i["id"] != id]
    salvar_csv(PRODUTOS_FILE, dados, ["id", "nome", "tipo", "descricao", "preco", "imagem","estoque"])
    flash("Produto deletado!", "sucesso")
    return redirect(url_for("routes.produtos"))

# ==============================
# PRODUTO GENÉRICO
# ==============================
@routes.route("/produto/<produto_id>")
def produto(produto_id):
    produtos = carregar_csv(PRODUTOS_FILE)
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("routes.index"))
    return render_template("produto_generico.html", produto=produto)

# ==============================
# ADICIONAR PRODUTO AO CARRINHO
# ==============================

@routes.route("/adicionar_carrinho", methods=["POST"])
def adicionar_carrinho():
    try:
        # GERAR ID DE SESSÃO PARA USUÁRIOS NÃO LOGADOS
        if "usuario_id" not in session:
            if "guest_id" not in session:
                session["guest_id"] = str(uuid.uuid4())
            usuario_id = f"guest_{session['guest_id']}"
        else:
            usuario_id = str(session["usuario_id"])

        produto_id = request.form.get("id_produto")
        plano = request.form.get("plano", "mensal")

        print(f"🔍 DEBUG - Usuário ID: {usuario_id}")
        print(f"🔍 DEBUG - Produto ID: {produto_id}")
        print(f"🔍 DEBUG - Plano: {plano}")

        if not produto_id:
            return jsonify({"success": False, "message": "ID do produto não informado."})

        try:
            quantidade = int(request.form.get("quantidade", 1))
            if quantidade < 1:
                quantidade = 1
        except (ValueError, TypeError):
            quantidade = 1

        produtos = carregar_csv(PRODUTOS_FILE)
        
        produto = None
        for p in produtos:
            if str(p.get("id")).strip() == str(produto_id).strip():
                produto = p
                break

        if not produto:
            return jsonify({"success": False, "message": "Produto não encontrado no sistema."})

        print(f"✅ DEBUG - Produto encontrado: {produto['nome']}")

        # VERIFICAÇÃO DE ESTOQUE (mantida igual)
        estoque_disponivel = 0
        try:
            estoque_str = produto.get("estoque", "0")
            if estoque_str and estoque_str.strip():
                estoque_disponivel = int(estoque_str)
            else:
                estoque_disponivel = 0
        except (ValueError, TypeError) as e:
            print(f"⚠️ AVISO - Erro ao ler estoque: {e}")
            estoque_disponivel = 0

        if estoque_disponivel <= 0:
            tipo_produto = produto.get("tipo", "").lower()
            if tipo_produto == "premium":
                print(f"ℹ️ INFO - Produto Premium '{produto['nome']}' com estoque {estoque_disponivel}, permitindo venda")
            else:
                print(f"❌ DEBUG - Produto fora de estoque: {produto['nome']}")
                return jsonify({"success": False, "message": "Produto fora de estoque."})
        else:
            if quantidade > estoque_disponivel:
                return jsonify({
                    "success": False, 
                    "message": f"Quantidade indisponível. Estoque disponível: {estoque_disponivel}"
                })

        try:
            valor_unitario = float(produto.get("preco", 0))
        except (ValueError, TypeError):
            valor_unitario = 0

        if valor_unitario <= 0:
            return jsonify({"success": False, "message": "Preço do produto inválido."})

        # CÁLCULO DO VALOR (apenas desconto da recorrência)
        multiplicador = {"mensal": 1, "semestral": 6, "anual": 12}.get(plano, 1)
        descontos = {"mensal": 0, "semestral": 0.05, "anual": 0.10}
        desconto = descontos.get(plano, 0)
        valor_total = round((valor_unitario * multiplicador * quantidade) * (1 - desconto), 2)

        carrinho = carregar_csv(CARRINHO_FILE)

        # VERIFICAR SE ITEM JÁ EXISTE NO CARRINHO
        for item in carrinho:
            item_usuario_ok = item["id_usuario"] == usuario_id
            item_produto_ok = str(item["id_produto"]).strip() == str(produto_id).strip()
            item_plano_ok = item["plano"] == plano
            item_status_ok = item["status"] == "em processo"
            
            if item_usuario_ok and item_produto_ok and item_plano_ok and item_status_ok:
                nova_quantidade = int(item["quantidade"]) + quantidade
                
                if estoque_disponivel > 0 and nova_quantidade > estoque_disponivel:
                    return jsonify({
                        "success": False, 
                        "message": f"Quantidade indisponível. Estoque disponível: {estoque_disponivel}"
                    })
                
                # Atualizar quantidade e valor
                item["quantidade"] = str(nova_quantidade)
                item["valor_total"] = str(round(valor_unitario * multiplicador * nova_quantidade * (1 - desconto), 2))
                
                salvar_csv(CARRINHO_FILE, carrinho, CARRINHO_FIELDS)
                
                # Contar itens do usuário (guest ou logado)
                itens_count = len([i for i in carrinho if i["id_usuario"] == usuario_id and i["status"] == "em processo"])
                
                return jsonify({
                    "success": True, 
                    "message": f"Quantidade de {produto['nome']} atualizada para {nova_quantidade}!",
                    "count": itens_count,
                    "is_guest": usuario_id.startswith("guest_")
                })

        # ADICIONAR NOVO ITEM
        novo_item = {
            "id_carrinho": str(uuid.uuid4()),
            "id_usuario": usuario_id,
            "id_produto": produto_id,
            "nome_produto": produto.get("nome", ""),
            "descricao": produto.get("descricao", ""),
            "plano": plano,
            "quantidade": str(quantidade),
            "valor_unitario": str(valor_unitario),
            "valor_total": str(valor_total),
            "status": "em processo"
        }

        carrinho.append(novo_item)
        salvar_csv(CARRINHO_FILE, carrinho, CARRINHO_FIELDS)

        # Contar itens do usuário
        itens_count = len([i for i in carrinho if i["id_usuario"] == usuario_id and i["status"] == "em processo"])

        print(f"✅ PRODUTO ADICIONADO: {produto['nome']} para usuário {usuario_id}")

        return jsonify({
            "success": True, 
            "message": f"{produto['nome']} adicionado ao carrinho com sucesso!",
            "count": itens_count,
            "is_guest": usuario_id.startswith("guest_")
        })

    except Exception as e:
        print(f"❌ ERRO em adicionar_carrinho: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Erro interno no servidor."})

# ==============================
# PÁGINA DO CARRINHO
# ==============================

@routes.route("/carrinho")
def carrinho():
    try:
        # VERIFICAR SE É USUÁRIO LOGADO OU GUEST
        if "usuario_id" in session:
            usuario_id = str(session["usuario_id"])
            is_guest = False
        elif "guest_id" in session:
            usuario_id = f"guest_{session['guest_id']}"
            is_guest = True
        else:
            # Se não tem nem usuário nem guest, criar sessão guest
            session["guest_id"] = str(uuid.uuid4())
            usuario_id = f"guest_{session['guest_id']}"
            is_guest = True
            print(f"🆕 Sessão guest criada: {usuario_id}")

        carrinho = carregar_csv(CARRINHO_FILE)

        itens_usuario = [
            item for item in carrinho 
            if item["id_usuario"] == usuario_id and item["status"] == "em processo"
        ]

        total_geral = 0.0
        for item in itens_usuario:
            try:
                total_geral += float(item["valor_total"])
            except (ValueError, TypeError):
                continue

        print(f"📦 Carrinho carregado: {len(itens_usuario)} itens para {usuario_id}")
        
        return render_template("carrinho.html", 
                             itens_carrinho=itens_usuario, 
                             total=round(total_geral, 2),
                             is_guest=is_guest)

    except Exception as e:
        print(f"❌ ERRO em carrinho: {str(e)}")
        flash("Erro ao carregar carrinho.", "erro")
        return redirect(url_for("routes.index"))

# ==============================
# EXCLUIR ITEM DO CARRINHO
# ==============================
@routes.route("/excluir_item_carrinho", methods=["POST"])
def excluir_item_carrinho():
    try:
        # VERIFICAR SE É USUÁRIO LOGADO OU GUEST
        if "usuario_id" in session:
            usuario_id = str(session["usuario_id"])
        elif "guest_id" in session:
            usuario_id = f"guest_{session['guest_id']}"
        else:
            # Se for requisição AJAX, retorna JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "message": "Sessão não encontrada."})
            flash("Faça login para gerenciar o carrinho.", "erro")
            return redirect(url_for("routes.login"))

        itens_selecionados = request.form.getlist("selecionar_item")
        
        # Se não vier da lista, verifica se veio como item_individual
        if not itens_selecionados:
            item_individual = request.form.get("item_id")
            if item_individual:
                itens_selecionados = [item_individual]

        if not itens_selecionados:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "message": "Nenhum item selecionado para exclusão."})
            flash("Nenhum item selecionado para exclusão.", "erro")
            return redirect(url_for("routes.carrinho"))

        carrinho = carregar_csv(CARRINHO_FILE)
        
        carrinho_atualizado = [
            item for item in carrinho 
            if not (item["id_usuario"] == usuario_id and item["id_carrinho"] in itens_selecionados)
        ]
        
        itens_removidos = len(carrinho) - len(carrinho_atualizado)
        
        if itens_removidos > 0:
            salvar_csv(CARRINHO_FILE, carrinho_atualizado, CARRINHO_FIELDS)
            
            # Calcular novo total para resposta AJAX
            itens_restantes = [
                item for item in carrinho_atualizado 
                if item["id_usuario"] == usuario_id and item["status"] == "em processo"
            ]
            total_geral = sum(float(item["valor_total"]) for item in itens_restantes)
            
            print(f"🗑️ {itens_removidos} item(ns) removido(s) do carrinho do usuário {usuario_id}")
            
            # Se for requisição AJAX (exclusão individual), retorna JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    "success": True, 
                    "message": f"{itens_removidos} item(ns) removido(s) do carrinho!",
                    "total_carrinho": f"R$ {total_geral:.2f}",
                    "itens_restantes": len(itens_restantes)
                })
            else:
                # Se for formulário normal (exclusão múltipla), usa flash e redirect
                flash(f"{itens_removidos} item(ns) removido(s) do carrinho!", "sucesso")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "message": "Nenhum item foi removido."})
            flash("Nenhum item foi removido.", "info")
            
        return redirect(url_for("routes.carrinho"))

    except Exception as e:
        print(f"❌ ERRO em excluir_item_carrinho: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "message": "Erro ao remover itens do carrinho."})
        flash("Erro ao remover itens do carrinho.", "erro")
        return redirect(url_for("routes.carrinho"))


# ==============================
# CONTADOR DO CARRINHO
# ==============================
@routes.route("/carrinho/contador")
def carrinho_contador():
    try:
        # VERIFICAR SE É USUÁRIO LOGADO OU GUEST
        if "usuario_id" in session:
            usuario_id = str(session["usuario_id"])
        elif "guest_id" in session:
            usuario_id = f"guest_{session['guest_id']}"
        else:
            return jsonify({"count": 0, "is_guest": True})
        
        carrinho = carregar_csv(CARRINHO_FILE)
        
        itens_usuario = [
            item for item in carrinho 
            if item["id_usuario"] == usuario_id and item["status"] == "em processo"
        ]
        
        count = len(itens_usuario)
        print(f"🔢 Contador do carrinho: {count} itens para {usuario_id}")
        
        return jsonify({
            "count": count, 
            "is_guest": usuario_id.startswith("guest_")
        })
        
    except Exception as e:
        print(f"❌ ERRO em carrinho_contador: {str(e)}")
        return jsonify({"count": 0, "is_guest": True})

# ==============================
# FINALIZAR COMPRA
# ============================== 
@routes.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    # VERIFICAR SE USUÁRIO ESTÁ LOGADO
    if "usuario_id" not in session:
        flash("Faça login para finalizar a compra.", "erro")
        return redirect(url_for("routes.login"))

    try:
        usuario_id = str(session["usuario_id"]) 
        itens_selecionados = request.form.getlist("selecionar_item")
        
        # CORREÇÃO: Receber diretamente o código do cupom
        codigo_cupom = request.form.get("cupom_aplicado", "").strip().upper()
        desconto_cupom = float(request.form.get("desconto_cupom", "0"))
        
        print(f"🔍 DEBUG - Itens selecionados para finalizar: {itens_selecionados}")
        print(f"🔍 DEBUG - Cupom recebido: {codigo_cupom}, Desconto: {desconto_cupom}%")

        if not itens_selecionados:
            flash("Nenhum item selecionado para finalizar compra.", "erro")
            return redirect(url_for("routes.carrinho"))

        carrinho = carregar_csv(CARRINHO_FILE)
        produtos = carregar_csv(PRODUTOS_FILE)
        vendas = carregar_csv(VENDAS_FILE)

        selecionados = [
            i for i in carrinho 
            if i["id_usuario"] == usuario_id and 
               i["status"] == "em processo" and 
               i["id_carrinho"] in itens_selecionados
        ]

        print(f"🔍 DEBUG - Itens encontrados para finalizar: {len(selecionados)}")

        for item in selecionados:
            print(f"🔍 DEBUG - Processando item: {item['nome_produto']}")

            produto = next((p for p in produtos if p["id"] == item["id_produto"]), None)
            if produto and produto.get("estoque"):
                try:
                    estoque_atual = int(produto.get("estoque", 0))
                    quantidade_comprada = int(item.get("quantidade", 1))
                    produto["estoque"] = str(max(0, estoque_atual - quantidade_comprada))
                    print(f"🔍 DEBUG - Estoque atualizado: {estoque_atual} -> {produto['estoque']}")
                except (ValueError, TypeError):
                    print(f"⚠️ Erro ao atualizar estoque do produto {produto['id']}")

            # CALCULAR VALOR ORIGINAL E VALOR COM DESCONTO - CORREÇÃO AQUI
            valor_unitario = float(item["valor_unitario"])
            quantidade = int(item["quantidade"])
            plano = item["plano"]
            
            # Calcular valor original (sem desconto)
            multiplicador = {"mensal": 1, "semestral": 6, "anual": 12}.get(plano, 1)
            valor_original = valor_unitario * multiplicador * quantidade
            
            # CORREÇÃO: Aplicar primeiro desconto da recorrência
            descontos_plano = {"mensal": 0, "semestral": 0.05, "anual": 0.10}
            desconto_plano = descontos_plano.get(plano, 0)
            
            # Valor após desconto da recorrência
            valor_apos_recorrencia = valor_original * (1 - desconto_plano)
            
            # CORREÇÃO: Aplicar desconto do cupom sobre o valor já com desconto da recorrência
            valor_com_desconto = valor_apos_recorrencia * (1 - (desconto_cupom / 100))
            
            # Garantir que não fique negativo
            valor_com_desconto = max(0, valor_com_desconto)

            # Calcular desconto total para registro
            desconto_total_percentual = ((valor_original - valor_com_desconto) / valor_original) * 100

            nova_compra = {
                "id_compra": str(uuid.uuid4()),
                "id_usuario": usuario_id,
                "id_produto": item["id_produto"],
                "quantidade": str(quantidade),
                "valor_original": round(valor_original, 2),
                "valor_desconto": round(valor_original - valor_com_desconto, 2),
                "valor_total": round(valor_com_desconto, 2),
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "plano": plano,
                "desconto_aplicado": round(desconto_total_percentual, 2),  # Percentual total real
                "cupom_aplicado": codigo_cupom
            }
            vendas.append(nova_compra)
            print(f"🔍 DEBUG - Nova compra registrada: {nova_compra}")
            print(f"🔍 DEBUG - Valor original: R$ {valor_original:.2f}")
            print(f"🔍 DEBUG - Após recorrência ({desconto_plano*100}%): R$ {valor_apos_recorrencia:.2f}")
            print(f"🔍 DEBUG - Após cupom ({desconto_cupom}%): R$ {valor_com_desconto:.2f}")

            item["status"] = "finalizado"

        salvar_csv(VENDAS_FILE, vendas, [
            "id_compra", "id_usuario", "id_produto", "quantidade", 
            "valor_original", "valor_desconto", "valor_total", "data",
            "plano", "desconto_aplicado", "cupom_aplicado"
        ])
        salvar_csv(PRODUTOS_FILE, produtos, ["id","nome","tipo","descricao","preco","imagem","estoque"])
        salvar_csv(CARRINHO_FILE, carrinho, CARRINHO_FIELDS)

        print(f"✅ Compra finalizada com sucesso para {len(selecionados)} itens")
        flash(f"Compra de {len(selecionados)} item(ns) finalizada com sucesso!", "sucesso")
        return redirect(url_for("routes.carrinho"))

    except Exception as e:
        print(f"❌ ERRO em finalizar_compra: {str(e)}")
        flash("Erro ao finalizar compra.", "erro")
        return redirect(url_for("routes.carrinho"))     

# ==============================
# ATUALIZAR QUANTIDADE DO ITEM
# ==============================

@routes.route("/atualizar_quantidade", methods=["POST"])
def atualizar_quantidade():
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Você precisa estar logado."})

    try:
        usuario_id = str(session["usuario_id"])
        item_id = request.form.get("item_id")
        nova_quantidade = int(request.form.get("quantidade", 1))

        if nova_quantidade < 1:
            return jsonify({"success": False, "message": "Quantidade deve ser maior que zero."})

        carrinho = carregar_csv(CARRINHO_FILE)
        produtos = carregar_csv(PRODUTOS_FILE)

        item = next((i for i in carrinho if i["id_carrinho"] == item_id and i["id_usuario"] == usuario_id), None)
        
        if not item:
            return jsonify({"success": False, "message": "Item não encontrado no carrinho."})

        produto = next((p for p in produtos if p["id"] == item["id_produto"]), None)
        if produto:
            estoque_disponivel = int(produto.get("estoque", 0))
            if estoque_disponivel > 0 and nova_quantidade > estoque_disponivel:
                return jsonify({
                    "success": False, 
                    "message": f"Quantidade indisponível. Estoque: {estoque_disponivel}"
                })

        valor_unitario = float(item["valor_unitario"])
        plano = item["plano"]
        
        # CORREÇÃO: Aplicar apenas desconto da recorrência (sem cupom no carrinho)
        multiplicador = {"mensal": 1, "semestral": 6, "anual": 12}.get(plano, 1)
        descontos = {"mensal": 0, "semestral": 0.05, "anual": 0.10}
        desconto = descontos.get(plano, 0)
        novo_valor_total = round((valor_unitario * multiplicador * nova_quantidade) * (1 - desconto), 2)

        item["quantidade"] = str(nova_quantidade)
        item["valor_total"] = str(novo_valor_total)

        salvar_csv(CARRINHO_FILE, carrinho, CARRINHO_FIELDS)

        itens_usuario = [i for i in carrinho if i["id_usuario"] == usuario_id and i["status"] == "em processo"]
        total_geral = sum(float(i["valor_total"]) for i in itens_usuario)

        return jsonify({
            "success": True, 
            "message": "Quantidade atualizada com sucesso!",
            "novo_total_item": f"R$ {novo_valor_total:.2f}",
            "total_carrinho": f"R$ {total_geral:.2f}"
        })

    except Exception as e:
        print(f"❌ ERRO em atualizar_quantidade: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao atualizar quantidade."})


# ==============================
# CKECKOUT
# ==============================

@routes.route('/checkout')
def checkout():
    if 'usuario_id' not in session:
        flash('Por favor, faça login para finalizar a compra.', 'warning')
        return redirect(url_for('routes.login'))
    
    return render_template('checkout.html')
# ==============================
# API PARA OBTER ITENS SELECIONADOS DO CARRINHO (PARA CHECKOUT)
# ==============================
@routes.route("/api/carrinho/itens_selecionados", methods=["POST"])
def api_carrinho_itens_selecionados():
    if "usuario_id" not in session:
        return jsonify({"itens": []})
    
    try:
        usuario_id = str(session["usuario_id"])
        dados = request.get_json()
        itens_selecionados = dados.get("itens_selecionados", [])
        
        print(f"🔍 DEBUG - Itens selecionados recebidos: {itens_selecionados}")
        
        carrinho = carregar_csv(CARRINHO_FILE)
        
        itens_filtrados = [
            item for item in carrinho 
            if (item["id_usuario"] == usuario_id and 
                item["status"] == "em processo" and 
                item["id_carrinho"] in itens_selecionados)
        ]
        
        print(f"🔍 DEBUG - Itens filtrados: {len(itens_filtrados)}")
        
        return jsonify({"itens": itens_filtrados})
        
    except Exception as e:
        print(f"❌ ERRO em api_carrinho_itens_selecionados: {str(e)}")
        return jsonify({"itens": []})

# ==============================
# DASHBOARD DE VENDAS
# ==============================
@routes.route("/dashboard_vendas")
def dashboard_vendas():
    if session.get("tipo") != "admin":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("routes.index"))

    try:
        vendas = carregar_csv(VENDAS_FILE)
        produtos = carregar_csv(PRODUTOS_FILE)
        usuarios = carregar_csv(USUARIOS_CLIENTE)
        
        for venda in vendas:
            venda["valor_total"] = float(venda.get("valor_total", 0))
            venda["quantidade"] = int(venda.get("quantidade", 1))
        
        total_vendas = len(vendas)
        faturamento_total = sum(venda["valor_total"] for venda in vendas)
        clientes_unicos = len(set(venda["id_usuario"] for venda in vendas))
        
        produtos_vendidos = {}
        for venda in vendas:
            produto_id = venda["id_produto"]
            produto = next((p for p in produtos if p["id"] == produto_id), {})
            nome_produto = produto.get("nome", f"Produto {produto_id}")
            
            if nome_produto not in produtos_vendidos:
                produtos_vendidos[nome_produto] = {
                    'quantidade': 0,
                    'faturamento': 0,
                    'id': produto_id
                }
            
            produtos_vendidos[nome_produto]['quantidade'] += venda["quantidade"]
            produtos_vendidos[nome_produto]['faturamento'] += venda["valor_total"]
        
        produtos_mais_vendidos = sorted(
            produtos_vendidos.items(), 
            key=lambda x: x[1]['quantidade'], 
            reverse=True
        )[:10]
        
        vendas_por_mes = {}
        for venda in vendas:
            data = venda.get("data", "")
            if data:
                mes_ano = data[:7]
                if mes_ano not in vendas_por_mes:
                    vendas_por_mes[mes_ano] = {
                        'quantidade': 0,
                        'faturamento': 0,
                        'vendas': 0
                    }
                vendas_por_mes[mes_ano]['quantidade'] += venda["quantidade"]
                vendas_por_mes[mes_ano]['faturamento'] += venda["valor_total"]
                vendas_por_mes[mes_ano]['vendas'] += 1
        
        ultimas_vendas = sorted(
            vendas, 
            key=lambda x: x.get("data", ""), 
            reverse=True
        )[:10]
        
        for venda in ultimas_vendas:
            produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
            venda["nome_produto"] = produto.get("nome", f"Produto {venda['id_produto']}")
            venda["tipo_produto"] = produto.get("tipo", "N/A")
        
        return render_template(
            "dashboard_vendas.html",
            total_vendas=total_vendas,
            faturamento_total=faturamento_total,
            clientes_unicos=clientes_unicos,
            produtos_mais_vendidos=produtos_mais_vendidos,
            vendas_por_mes=vendas_por_mes,
            ultimas_vendas=ultimas_vendas
        )
        
    except Exception as e:
        print(f"❌ ERRO em dashboard_vendas: {str(e)}")
        flash("Erro ao carregar dashboard de vendas.", "erro")
        return redirect(url_for("routes.usuario_adm"))

# ==============================
# DETALHES DA VENDA
# ==============================
@routes.route("/detalhes_venda/<venda_id>")
def detalhes_venda(venda_id):
    if session.get("tipo") != "admin":
        flash("Acesso restrito a administradores.", "erro")
        return redirect(url_for("routes.index"))

    try:
        vendas = carregar_csv(VENDAS_FILE)
        produtos = carregar_csv(PRODUTOS_FILE)
        usuarios = carregar_csv(USUARIOS_CLIENTE)
        
        venda = next((c for c in vendas if c["id_compra"] == venda_id), None)
        
        if not venda:
            flash("Venda não encontrada.", "erro")
            return redirect(url_for("routes.dashboard_vendas"))
        
        produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
        usuario = next((u for u in usuarios if u["id"] == venda["id_usuario"]), {})
        
        venda["nome_produto"] = produto.get("nome", f"Produto {venda['id_produto']}")
        venda["tipo_produto"] = produto.get("tipo", "N/A")
        venda["preco_unitario"] = float(venda["valor_total"]) / int(venda["quantidade"])
        venda["nome_usuario"] = usuario.get("nome", "Cliente")
        venda["email_usuario"] = usuario.get("email", "N/A")
        
        return render_template("detalhes_venda.html", venda=venda)
        
    except Exception as e:
        print(f"❌ ERRO em detalhes_venda: {str(e)}")
        flash("Erro ao carregar detalhes da venda.", "erro")
        return redirect(url_for("routes.dashboard_vendas"))
    
# ==============================
# MEUS PEDIDOS
# ==============================
@routes.route("/meus_pedidos")
def meus_pedidos():
    if "usuario_id" not in session:
        flash("Você precisa estar logado para ver seus pedidos.", "erro")
        return redirect(url_for("routes.login"))
    
    try:
        usuario_id = str(session["usuario_id"])
        vendas = carregar_csv(VENDAS_FILE)
        produtos = carregar_csv(PRODUTOS_FILE)
        
        minhas_vendas = [v for v in vendas if v["id_usuario"] == usuario_id]
        
        for venda in minhas_vendas:
            produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
            venda["nome_produto"] = produto.get("nome", "Produto não encontrado")
            venda["imagem_produto"] = produto.get("imagem", "")
            venda["descricao_produto"] = produto.get("descricao", "")
        
        minhas_vendas.sort(key=lambda x: x.get("data", ""), reverse=True)
        
        return render_template("meus_pedidos.html", vendas=minhas_vendas)
        
    except Exception as e:
        print(f"❌ ERRO em meus_pedidos: {str(e)}")
        flash("Erro ao carregar seus pedidos.", "erro")
        return redirect(url_for("routes.index"))

# ==============================
# CONFIGURAÇÕES
# ==============================

@routes.route("/configuracoes")
def configuracoes():
    print("🔍 ACESSANDO ROTA /configuracoes")  # Debug
    
    if "usuario_id" not in session:
        flash("Você precisa estar logado para acessar as configurações.", "erro")
        print("❌ Usuário não logado, redirecionando para login")
        return redirect(url_for("routes.login"))
    
    try:
        usuario_id = str(session["usuario_id"])
        print(f"🔍 Usuário ID: {usuario_id}")
        
        # Carregar dados
        clientes = carregar_csv(USUARIOS_CLIENTE)
        enderecos = carregar_csv(ENDERECOS_FILE)
        vendas = carregar_csv(VENDAS_FILE)
        produtos = carregar_csv(PRODUTOS_FILE)
        
        print(f"🔍 Dados carregados - Clientes: {len(clientes)}, Endereços: {len(enderecos)}, Vendas: {len(vendas)}, Produtos: {len(produtos)}")
        
        # Encontrar usuário
        usuario = next((c for c in clientes if c["id"] == usuario_id), None)
        
        if not usuario:
            flash("Usuário não encontrado.", "erro")
            print("❌ Usuário não encontrado nos dados")
            return redirect(url_for("routes.index"))
        
        print(f"✅ Usuário encontrado: {usuario.get('nome')}")
        
        # Carregar endereços
        meus_enderecos = [e for e in enderecos if e["id_cliente"] == usuario_id]
        endereco_principal = next((e for e in meus_enderecos if e.get("principal") == "sim"), None)
        
        print(f"📍 Endereços encontrados: {len(meus_enderecos)}, Principal: {endereco_principal is not None}")
        
        # Carregar pedidos - VERSÃO COMPLETA COM TODOS OS CAMPOS
        meus_pedidos = []
        for venda in vendas:
            if venda["id_usuario"] == usuario_id:
                produto = next((p for p in produtos if p["id"] == venda["id_produto"]), {})
                
                # Extrair todos os campos da venda
                valor_original = float(venda.get("valor_original", 0))
                valor_total = float(venda.get("valor_total", 0))
                desconto_aplicado = float(venda.get("desconto_aplicado", 0))
                cupom_aplicado = venda.get("cupom_aplicado", "")
                
                # Calcular valores se necessário
                if valor_original == 0 and valor_total > 0:
                    # Se não tem valor_original, calcular baseado no desconto
                    if desconto_aplicado > 0:
                        valor_original = valor_total / (1 - (desconto_aplicado / 100))
                    else:
                        valor_original = valor_total
                
                # Calcular economia
                economia = valor_original - valor_total if valor_original > valor_total else 0
                
                # Calcular desconto da recorrência baseado no plano
                plano = venda.get("plano", "mensal")
                descontos_plano = {"mensal": 0, "semestral": 5, "anual": 10}
                desconto_recorrencia = descontos_plano.get(plano, 0)
                
                pedido = {
                    # Informações básicas
                    "id_compra": venda.get("id_compra", ""),
                    "id_produto": venda.get("id_produto", ""),
                    "nome_produto": produto.get("nome", "Produto não encontrado"),
                    "quantidade": venda.get("quantidade", "1"),
                    "plano": plano,
                    "data": venda.get("data", ""),
                    "imagem_produto": produto.get("imagem", ""),
                    
                    # Valores monetários
                    "valor_total": valor_total,
                    "valor_sem_desconto": valor_original,
                    "valor_com_desconto": valor_total,
                    
                    # Descontos
                    "desconto_aplicado": desconto_aplicado,
                    "desconto_recorrencia": desconto_recorrencia,
                    "cupom_aplicado": cupom_aplicado,
                    
                    # Cálculos
                    "economia": economia
                }
                meus_pedidos.append(pedido)
        
        meus_pedidos.sort(key=lambda x: x.get("data", ""), reverse=True)
        print(f"📦 Pedidos encontrados: {len(meus_pedidos)}")
        
        # Debug: mostrar informações dos pedidos
        for i, pedido in enumerate(meus_pedidos):
            print(f"📋 Pedido {i+1}: {pedido['nome_produto']}")
            print(f"   💰 Original: R$ {pedido['valor_sem_desconto']:.2f}")
            print(f"   💸 Pago: R$ {pedido['valor_com_desconto']:.2f}")
            print(f"   📉 Desconto: {pedido['desconto_aplicado']:.1f}%")
            print(f"   🏷️ Cupom: {pedido['cupom_aplicado']}")
        
        return render_template("configuracoes.html", 
                             usuario=usuario, 
                             enderecos=meus_enderecos,
                             endereco_principal=endereco_principal,
                             pedidos=meus_pedidos)
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO em configuracoes: {str(e)}")
        import traceback
        traceback.print_exc()
        flash("Erro ao carregar configurações.", "erro")
        return redirect(url_for("routes.index"))

    
# ==============================
# COMPRAR NOVAMENTE
# ==============================

@routes.route("/comprar_novamente/<produto_id>")
def comprar_novamente(produto_id):
    """Redireciona para a página do produto específico para comprar novamente"""
    try:
        # Verificar se o produto existe
        produtos = carregar_csv(PRODUTOS_FILE)
        produto = next((p for p in produtos if p["id"] == produto_id), None)
        
        if not produto:
            flash("Produto não encontrado.", "erro")
            return redirect(url_for("routes.index"))
        
        # Redirecionar para a página do produto
        return redirect(url_for("routes.produto", produto_id=produto_id))
        
    except Exception as e:
        print(f"❌ ERRO em comprar_novamente: {str(e)}")
        flash("Erro ao redirecionar para o produto.", "erro")
        return redirect(url_for("routes.index"))

# ==============================
# ATUALIZAR PERFIL
# ==============================
@routes.route("/atualizar_perfil", methods=["POST"])
def atualizar_perfil():
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
    try:
        usuario_id = str(session["usuario_id"])
        clientes = carregar_csv(USUARIOS_CLIENTE)
        
        usuario = next((c for c in clientes if c["id"] == usuario_id), None)
        if not usuario:
            return jsonify({"success": False, "message": "Usuário não encontrado."})
        
        nome = request.form.get("nome", "").strip()
        sobrenome = request.form.get("sobrenome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        
        if not nome or not sobrenome or not email or not telefone:
            return jsonify({"success": False, "message": "Preencha todos os campos obrigatórios."})
        
        if any(u["id"] != usuario_id and u.get("email") == email for u in clientes):
            return jsonify({"success": False, "message": "Este e-mail já está em uso por outro usuário."})
        
        usuario["nome"] = nome
        usuario["sobrenome"] = sobrenome
        usuario["email"] = email
        usuario["telefone"] = telefone
        usuario["data_nascimento"] = request.form.get("data_nascimento", usuario.get("data_nascimento", ""))
        
        session["usuario_nome"] = usuario["nome"]
        session["primeiro_nome"] = usuario["nome"].split()[0]
        
        salvar_csv(USUARIOS_CLIENTE, clientes, ["id", "cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"])
        
        return jsonify({"success": True, "message": "Perfil atualizado com sucesso!"})
        
    except Exception as e:
        print(f"❌ ERRO em atualizar_perfil: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao atualizar perfil."})

# ==============================
# ADICIONAR ENDEREÇO (ROTA ÚNICA CORRIGIDA)
# ==============================
@routes.route("/adicionar_endereco", methods=["POST"])
def adicionar_endereco():
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
    try:
        usuario_id = str(session["usuario_id"])
        enderecos = carregar_csv(ENDERECOS_FILE)
        
        campos_obrigatorios = ["cep", "endereco", "numero", "bairro", "cidade", "estado"]
        for campo in campos_obrigatorios:
            if not request.form.get(campo, "").strip():
                return jsonify({"success": False, "message": f"O campo {campo} é obrigatório."})
        
        if request.form.get("endereco_principal"):
            for endereco in enderecos:
                if endereco["id_cliente"] == usuario_id:
                    endereco["principal"] = "nao"
            salvar_csv(ENDERECOS_FILE, enderecos, ["id", "id_cliente", "tipo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "pais", "principal"])
        
        novo_endereco = {
            "id": gerar_id_auto(enderecos),
            "id_cliente": usuario_id,
            "tipo": request.form.get("tipo", "residencial"),
            "cep": request.form.get("cep", "").strip(),
            "endereco": request.form.get("endereco", "").strip(),
            "numero": request.form.get("numero", "").strip(),
            "complemento": request.form.get("complemento", "").strip(),
            "bairro": request.form.get("bairro", "").strip(),
            "cidade": request.form.get("cidade", "").strip(),
            "estado": request.form.get("estado", "").strip(),
            "pais": request.form.get("pais", "Brasil").strip(),
            "principal": "sim" if request.form.get("endereco_principal") else "nao"
        }
        
        meus_enderecos = [e for e in enderecos if e["id_cliente"] == usuario_id]
        if not meus_enderecos:
            novo_endereco["principal"] = "sim"
        
        enderecos.append(novo_endereco)
        salvar_csv(ENDERECOS_FILE, enderecos, ["id", "id_cliente", "tipo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "pais", "principal"])
        
        return jsonify({"success": True, "message": "Endereço adicionado com sucesso!"})
        
    except Exception as e:
        print(f"❌ ERRO em adicionar_endereco: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao adicionar endereço."})

# ==============================
# ALTERAR SENHA
# ==============================
@routes.route("/alterar_senha", methods=["POST"])
def alterar_senha():
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
    try:
        usuario_id = str(session["usuario_id"])
        senha_atual = request.form.get("senha_atual", "").strip()
        nova_senha = request.form.get("nova_senha", "").strip()
        confirmar_senha = request.form.get("confirmar_senha", "").strip()
        
        if not senha_atual or not nova_senha or not confirmar_senha:
            return jsonify({"success": False, "message": "Preencha todos os campos."})
        
        if nova_senha != confirmar_senha:
            return jsonify({"success": False, "message": "As senhas não coincidem."})
        
        if len(nova_senha) < 6:
            return jsonify({"success": False, "message": "A senha deve ter pelo menos 6 caracteres."})
        
        clientes = carregar_csv(USUARIOS_CLIENTE)
        usuario = next((c for c in clientes if c["id"] == usuario_id), None)
        
        if not usuario:
            return jsonify({"success": False, "message": "Usuário não encontrado."})
        
        if usuario.get("senha") != senha_atual:
            return jsonify({"success": False, "message": "Senha atual incorreta."})
        
        usuario["senha"] = nova_senha
        salvar_csv(USUARIOS_CLIENTE, clientes, ["id", "cpf", "nome", "sobrenome", "data_nascimento", "email", "senha", "telefone"])
        
        return jsonify({"success": True, "message": "Senha alterada com sucesso!"})
        
    except Exception as e:
        print(f"❌ ERRO em alterar_senha: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao alterar senha."})

# ==============================
# EXCLUIR ENDEREÇO
# ==============================
@routes.route("/excluir_endereco/<endereco_id>", methods=["POST"])
def excluir_endereco(endereco_id):
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
    try:
        usuario_id = str(session["usuario_id"])
        enderecos = carregar_csv(ENDERECOS_FILE)
        
        endereco = next((e for e in enderecos if e["id"] == endereco_id and e["id_cliente"] == usuario_id), None)
        if not endereco:
            return jsonify({"success": False, "message": "Endereço não encontrado."})
        
        meus_enderecos = [e for e in enderecos if e["id_cliente"] == usuario_id]
        if len(meus_enderecos) <= 1:
            return jsonify({"success": False, "message": "Você não pode excluir seu único endereço."})
        
        enderecos_atualizados = [e for e in enderecos if not (e["id"] == endereco_id and e["id_cliente"] == usuario_id)]
        
        if endereco.get("principal") == "sim":
            outros_enderecos = [e for e in enderecos_atualizados if e["id_cliente"] == usuario_id]
            if outros_enderecos:
                outros_enderecos[0]["principal"] = "sim"
        
        salvar_csv(ENDERECOS_FILE, enderecos_atualizados, ["id", "id_cliente", "tipo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "pais", "principal"])
        
        return jsonify({"success": True, "message": "Endereço excluído com sucesso!"})
        
    except Exception as e:
        print(f"❌ ERRO em excluir_endereco: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao excluir endereço."})

# ==============================
# DEFINIR ENDEREÇO PRINCIPAL
# ==============================
@routes.route("/definir_endereco_principal/<endereco_id>", methods=["POST"])
def definir_endereco_principal(endereco_id):
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
    try:
        usuario_id = str(session["usuario_id"])
        enderecos = carregar_csv(ENDERECOS_FILE)
        
        endereco = next((e for e in enderecos if e["id"] == endereco_id and e["id_cliente"] == usuario_id), None)
        if not endereco:
            return jsonify({"success": False, "message": "Endereço não encontrado."})
        
        for e in enderecos:
            if e["id_cliente"] == usuario_id:
                e["principal"] = "nao"
        
        endereco["principal"] = "sim"
        
        salvar_csv(ENDERECOS_FILE, enderecos, ["id", "id_cliente", "tipo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "pais", "principal"])
        
        return jsonify({"success": True, "message": "Endereço principal definido com sucesso!"})
        
    except Exception as e:
        print(f"❌ ERRO em definir_endereco_principal: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao definir endereço principal."})
    
# ==============================
# EDITAR ENDEREÇO
# ==============================
@routes.route("/editar_endereco/<endereco_id>", methods=["POST"])
def editar_endereco(endereco_id):
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
    try:
        usuario_id = str(session["usuario_id"])
        enderecos = carregar_csv(ENDERECOS_FILE)
        
        # Encontrar o endereço a ser editado
        endereco_index = None
        for i, endereco in enumerate(enderecos):
            if endereco["id"] == endereco_id and endereco["id_cliente"] == usuario_id:
                endereco_index = i
                break
        
        if endereco_index is None:
            return jsonify({"success": False, "message": "Endereço não encontrado."})
        
        campos_obrigatorios = ["cep", "endereco", "numero", "bairro", "cidade", "estado"]
        for campo in campos_obrigatorios:
            if not request.form.get(campo, "").strip():
                return jsonify({"success": False, "message": f"O campo {campo} é obrigatório."})
        
        # Se marcar como principal, remover principal dos outros
        if request.form.get("endereco_principal"):
            for endereco in enderecos:
                if endereco["id_cliente"] == usuario_id:
                    endereco["principal"] = "nao"
        
        # Atualizar o endereço
        enderecos[endereco_index].update({
            "tipo": request.form.get("tipo", "residencial"),
            "cep": request.form.get("cep", "").strip(),
            "endereco": request.form.get("endereco", "").strip(),
            "numero": request.form.get("numero", "").strip(),
            "complemento": request.form.get("complemento", "").strip(),
            "bairro": request.form.get("bairro", "").strip(),
            "cidade": request.form.get("cidade", "").strip(),
            "estado": request.form.get("estado", "").strip(),
            "pais": request.form.get("pais", "Brasil").strip(),
            "principal": "sim" if request.form.get("endereco_principal") else "nao"
        })
        
        salvar_csv(ENDERECOS_FILE, enderecos, ["id", "id_cliente", "tipo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "pais", "principal"])
        
        return jsonify({"success": True, "message": "Endereço atualizado com sucesso!"})
        
    except Exception as e:
        print(f"❌ ERRO em editar_endereco: {str(e)}")
        return jsonify({"success": False, "message": "Erro ao editar endereço."})
    
# ==============================
# Mix Up Code
# ==============================

@routes.route('/mixupcode')
def mixupcode():
    return render_template('mixupcode.html')


# ==============================
# ROTAS DE DEBUG - ADICIONE ISSO
# ==============================

@routes.route("/teste_simples")
def teste_simples():
    return "TESTE SIMPLES: Funcionando!"

@routes.route("/teste_config")
def teste_config():
    return "TESTE CONFIG: Funcionando!"

@routes.route("/debug_session")
def debug_session():
    session_info = {
        'usuario_id': session.get('usuario_id'),
        'usuario_nome': session.get('usuario_nome'),
        'tipo': session.get('tipo'),
        'email': session.get('email')
    }
    return jsonify(session_info)


# ==============================
# API PARA ENDEREÇOS DO USUÁRIO
# ==============================
@routes.route("/api/enderecos")
def api_enderecos():
    if "usuario_id" not in session:
        return jsonify({"enderecos": []})
    
    try:
        usuario_id = str(session["usuario_id"])
        enderecos = carregar_csv(ENDERECOS_FILE)
        
        meus_enderecos = [
            e for e in enderecos 
            if e["id_cliente"] == usuario_id
        ]
        
        return jsonify({"enderecos": meus_enderecos})
        
    except Exception as e:
        print(f"❌ ERRO em api_enderecos: {str(e)}")
        return jsonify({"enderecos": []})