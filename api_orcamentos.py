# api_orcamentos.py
from flask import Blueprint, request, jsonify
import requests

orcamentos_bp = Blueprint("orcamentos_bp", __name__)

# =====================
# API ORÇAMENTOS
# =====================

@orcamentos_bp.route("/api/orcamento", methods=["POST"])
def criar_orcamento():
    from app import SUPABASE_URL, HEADERS  # pega as chaves do app principal
    data = request.json
    cliente_nome = data.get("cliente_nome")
    if not cliente_nome:
        return jsonify({"success": False, "error": "Cliente não informado"}), 400

    try:
        r_last = requests.get(
            f"{SUPABASE_URL}/rest/v1/orcamentos?select=numero_pedido&order=numero_pedido.desc&limit=1",
            headers=HEADERS
        )
        r_last.raise_for_status()
        last_pedido = r_last.json()
        numero_pedido = (last_pedido[0]['numero_pedido'] + 1) if last_pedido else 1

        payload = {"cliente_nome": cliente_nome, "numero_pedido": numero_pedido}
        r_post = requests.post(
            f"{SUPABASE_URL}/rest/v1/orcamentos",
            headers={**HEADERS, "Content-Type": "application/json", "Prefer": "return=representation"},
            json=payload
        )
        r_post.raise_for_status()
        new_orcamento = r_post.json()

        return jsonify({
            "success": True,
            "id": new_orcamento[0]['id'],
            "numero_pedido": numero_pedido,
            "cliente_nome": cliente_nome
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@orcamentos_bp.route("/api/orcamentos", methods=["GET"])
def listar_orcamentos():
    from app import SUPABASE_URL, HEADERS  # pega as chaves do app principal
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/orcamentos?select=id,numero_pedido,cliente_nome,data_criacao&order=numero_pedido.asc",
            headers=HEADERS
        )
        r.raise_for_status()
        return jsonify({"success": True, "orcamentos": r.json()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

