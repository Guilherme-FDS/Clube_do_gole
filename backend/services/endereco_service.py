from config import Config
from backend.utils import csv_helper as csv

CAMPOS = [
    "id", "id_cliente", "tipo", "cep", "endereco", "numero",
    "complemento", "bairro", "cidade", "estado", "pais", "principal",
]

def listar_do_usuario(usuario_id):
    return [e for e in csv.ler(Config.ENDERECOS_FILE) if e["id_cliente"] == str(usuario_id)]

def buscar(endereco_id, usuario_id):
    return next(
        (e for e in csv.ler(Config.ENDERECOS_FILE)
         if e["id"] == str(endereco_id) and e["id_cliente"] == str(usuario_id)),
        None
    )

def adicionar(usuario_id, dados, definir_principal=False):
    usuario_id = str(usuario_id)
    enderecos = csv.ler(Config.ENDERECOS_FILE)
    meus = [e for e in enderecos if e["id_cliente"] == usuario_id]

    if not meus:
        definir_principal = True

    if definir_principal:
        for e in enderecos:
            if e["id_cliente"] == usuario_id:
                e["principal"] = "nao"

    novo = {
        "id": csv.proximo_id(enderecos),
        "id_cliente": usuario_id,
        "principal": "sim" if definir_principal else "nao",
        **dados,
    }
    enderecos.append(novo)
    csv.salvar(Config.ENDERECOS_FILE, enderecos, CAMPOS)
    return True, "Endereço adicionado com sucesso!"

def atualizar(endereco_id, usuario_id, dados, definir_principal=False):
    usuario_id = str(usuario_id)
    enderecos = csv.ler(Config.ENDERECOS_FILE)
    idx = next(
        (i for i, e in enumerate(enderecos)
         if e["id"] == str(endereco_id) and e["id_cliente"] == usuario_id),
        None
    )
    if idx is None:
        return False, "Endereço não encontrado."

    if definir_principal:
        for e in enderecos:
            if e["id_cliente"] == usuario_id:
                e["principal"] = "nao"

    enderecos[idx].update({**dados, "principal": "sim" if definir_principal else "nao"})
    csv.salvar(Config.ENDERECOS_FILE, enderecos, CAMPOS)
    return True, "Endereço atualizado com sucesso!"

def remover(endereco_id, usuario_id):
    usuario_id = str(usuario_id)
    enderecos = csv.ler(Config.ENDERECOS_FILE)
    meus = [e for e in enderecos if e["id_cliente"] == usuario_id]

    if len(meus) <= 1:
        return False, "Você não pode excluir seu único endereço."

    endereco = next((e for e in meus if e["id"] == str(endereco_id)), None)
    if not endereco:
        return False, "Endereço não encontrado."

    novos = [e for e in enderecos if not (e["id"] == str(endereco_id) and e["id_cliente"] == usuario_id)]

    if endereco.get("principal") == "sim":
        restantes = [e for e in novos if e["id_cliente"] == usuario_id]
        if restantes:
            restantes[0]["principal"] = "sim"

    csv.salvar(Config.ENDERECOS_FILE, novos, CAMPOS)
    return True, "Endereço excluído com sucesso!"

def definir_principal(endereco_id, usuario_id):
    usuario_id = str(usuario_id)
    enderecos = csv.ler(Config.ENDERECOS_FILE)
    encontrado = False

    for e in enderecos:
        if e["id_cliente"] == usuario_id:
            if e["id"] == str(endereco_id):
                e["principal"] = "sim"
                encontrado = True
            else:
                e["principal"] = "nao"

    if not encontrado:
        return False, "Endereço não encontrado."

    csv.salvar(Config.ENDERECOS_FILE, enderecos, CAMPOS)
    return True, "Endereço principal definido com sucesso!"