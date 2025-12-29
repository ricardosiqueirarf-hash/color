# api_portas.py
from flask import Blueprint, request, jsonify
import requests

portas_bp = Blueprint("portas_bp", __name__)

# =====================
# API PORTAS
# =====================

@portas_bp.route("/api/orcamento/<orcamento_uuid>/finalizar", methods=["POST"])
def finalizar_portas(orcamento_uuid):
    """
    Recebe um JSON com lista de portas e salva no Supabase vinculando ao orcamento_uuid
    Exemplo de payload:
    {
        "portas": [
            {"tipo":"giro","dados":{...},"preco":123.45,"svg":"<svg>...</svg>","orcamento_uuid":"abc-123"}
        ]
    }
    """
    from app import SUPABASE_URL, HEADERS  # pega as chaves do app principal
    data = request.json
    portas = data.get("portas")
    if not portas or not isinstance(portas, list):
        return jsonify({"success": False, "error": "Nenhuma porta enviada"}), 400

    try:
        # Mapeia cada porta para o formato da tabela Supabase
        payload = []
        for p in portas:
            payload.append({
                "orcamento_uuid": p.get("orcamento_uuid", orcamento_uuid),
                "tipo": p.get("tipo"),
                "dados": p.get("dados"),
                "preco": p.get("preco"),
                "svg": p.get("svg")
            })

        # POST para a tabela 'portas' no Supabase
        r_post = requests.post(
            f"{SUPABASE_URL}/rest/v1/portas",
            headers={**HEADERS, "Content-Type": "application/json", "Prefer": "return=representation"},
            json=payload
        )
        r_post.raise_for_status()
        portas_salvas = r_post.json()

        return jsonify({"success": True, "portas_salvas": portas_salvas})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@portas_bp.route("/api/orcamento/<orcamento_uuid>/portas", methods=["GET"])
def listar_portas(orcamento_uuid):
    """
    Lista todas as portas vinculadas a um determinado orçamento
    """
    from app import SUPABASE_URL, HEADERS
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/portas?orcamento_uuid=eq.{orcamento_uuid}",
            headers=HEADERS
        )
        r.raise_for_status()
        return jsonify({"success": True, "portas": r.json()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
