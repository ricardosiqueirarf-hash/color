from flask import Blueprint, request, jsonify
import requests

vidros_bp = Blueprint("vidros_bp", __name__)

def calcular_preco(custo, margem, perda):
    custo_com_perda = custo * (1 + perda / 100)
    return custo_com_perda * (1 + margem / 100)

# GET
@vidros_bp.route("/api/vidros", methods=["GET"])
def listar_vidros():
    from app import SUPABASE_URL, HEADERS  # importa as chaves do app.py
    r = requests.get(f"{SUPABASE_URL}/rest/v1/vidros?select=*&order=tipo.asc", headers=HEADERS)
    r.raise_for_status()
    return jsonify(r.json())

# POST
@vidros_bp.route("/api/vidros", methods=["POST"])
def criar_vidro():
    from app import SUPABASE_URL, HEADERS
    data = request.json
    preco = calcular_preco(float(data["custo"]), float(data["margem"]), float(data["perda"]))
    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/vidros", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "ok"})

# PUT
@vidros_bp.route("/api/vidros/<id>", methods=["PUT"])
def editar_vidro(id):
    from app import SUPABASE_URL, HEADERS
    data = request.json
    preco = calcular_preco(float(data["custo"]), float(data["margem"]), float(data["perda"]))
    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "updated"})

# DELETE
@vidros_bp.route("/api/vidros/<id>", methods=["DELETE"])
def deletar_vidro(id):
    from app import SUPABASE_URL, HEADERS
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}", headers=HEADERS)
    r.raise_for_status()
    return jsonify({"status": "deleted"})

