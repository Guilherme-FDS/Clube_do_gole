import csv
import os

def garantir_arquivo(path, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def ler(caminho):
    if not os.path.exists(caminho):
        return []
    csv.field_size_limit(10 * 1024 * 1024)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            return []
        lines = content.splitlines()
        if not lines:
            return []
        headers = [h.strip('"') for h in lines[0].split(",")]
        dados = []
        for line in lines[1:]:
            if not line.strip():
                continue
            values, current, in_quotes = [], [], False
            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == "," and not in_quotes:
                    values.append("".join(current).strip('"'))
                    current = []
                else:
                    current.append(char)
            values.append("".join(current).strip('"'))
            if len(values) == len(headers):
                dados.append(dict(zip(headers, values)))
        return dados
    except Exception as e:
        print(f"[csv_helper] Erro ao ler {caminho}: {e}")
        try:
            with open(caminho, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except Exception:
            return []

def salvar(caminho, dados, campos):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(",".join(f'"{c}"' for c in campos) + "\n")
            for linha in dados:
                valores = []
                for campo in campos:
                    valor = str(linha.get(campo, ""))
                    if "," in valor or "\n" in valor or '"' in valor:
                        valor = valor.replace('"', '""')
                        valor = f'"{valor}"'
                    valores.append(valor)
                f.write(",".join(valores) + "\n")
    except Exception as e:
        print(f"[csv_helper] Erro ao salvar {caminho}: {e}")

def proximo_id(dados, campo="id"):
    if not dados:
        return "1"
    try:
        ids = [int(d[campo]) for d in dados if d.get(campo) and str(d[campo]).isdigit()]
        return str(max(ids) + 1) if ids else "1"
    except Exception:
        return str(len(dados) + 1)