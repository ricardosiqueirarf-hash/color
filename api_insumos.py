from flask import Blueprint, request, jsonify
import requests

insumos_bp = Blueprint("insumos_bp", __name__)


# ===================== ROTAS INSUMOS =====================
@insumos_bp.route("/api/materiais", methods=["GET"])

def listar_materiais():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/materiais?select=*&order=nome.asc", headers=HEADERS)
    r.raise_for_status()
    return jsonify(r.json())

@insumos_bp.route("/api/materiais", methods=["POST"])
@login_required
def criar_material():
    data = request.json
    preco = float(data.get("preco", 0))  
    payload = {
        "nome": data["nome"],
        "custo": data["custo"],
        "tipo_medida": data["tipo_medida"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/materiais", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "ok"})

@insumos_bp.route("/api/materiais/<id>", methods=["PUT"])
@login_required
def editar_material(id):
    data = request.json
    preco = float(data.get("preco", 0))
    payload = {
        "nome": data["nome"],
        "custo": data["custo"],
        "tipo_medida": data["tipo_medida"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/materiais?id=eq.{id}", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "updated"})

@insumos_bp.route("/api/materiais/<id>", methods=["DELETE"])
@login_required
def deletar_material(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/materiais?id=eq.{id}", headers=HEADERS)
    r.raise_for_status()
    return jsonify({"status": "deleted"})

