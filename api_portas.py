from flask import Blueprint, request, jsonify
import requests

portas_bp = Blueprint("portas_bp", __name__)

# =====================
# API PORTAS
# =====================

@portas_bp.route("/api/orcamento/<orcamento_uuid>/finalizar", methods=["POST"])
def salvar_portas(orcamento_uuid):
    """
    Recebe portas via JSON e salva no Supabase vinculando ao orcamento_uuid.
    """
    from app import SUPABASE_URL, HEADERS
    data = request.json
    portas = data.get("portas")
    if not portas or not isinstance(portas, list):
        return jsonify({"success": False, "error": "Nenhuma porta enviada"}), 400

    try:
        payload = []
        for p in portas:
            dados_obj = p.get("dados", {})
            dados_array = [f"{k}:{v}" for k, v in dados_obj.items()]

            payload.append({
                "orcamento_uuid": p.get("orcamento_uuid", orcamento_uuid),
                "tipo": p.get("tipo"),
                "dados": dados_array,
                "quantidade": p.get("quantidade", 1),
                "preco": p.get("preco"),
                "svg": p.get("svg")
            })

        r_post = requests.post(
            f"{SUPABASE_URL}/rest/v1/portas",
            headers={**HEADERS, "Content-Type": "application/json", "Prefer": "return=representation"},
            json=payload
        )
        r_post.raise_for_status()
        portas_salvas = r_post.json()

        return jsonify({"success": True, "portas_salvas": portas_salvas})

    except requests.HTTPError as http_err:
        return jsonify({"success": False, "error": f"{http_err.response.status_code} {http_err.response.text}"}), http_err.response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@portas_bp.route("/api/orcamento/<orcamento_uuid>/portas", methods=["GET"])
def listar_portas(orcamento_uuid):
    """
    Lista portas vinculadas a um orçamento.
    """
    from app import SUPABASE_URL, HEADERS
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/portas?orcamento_uuid=eq.{orcamento_uuid}",
            headers=HEADERS
        )
        r.raise_for_status()

        portas = r.json()
        for p in portas:
            dados_array = p.get("dados", [])
            if isinstance(dados_array, list):
                p["dados"] = dict(item.split(":", 1) for item in dados_array if ":" in item)
            p["quantidade"] = int(p.get("quantidade", 1))

        return jsonify({"success": True, "portas": portas})
    except requests.HTTPError as http_err:
        return jsonify({"success": False, "error": f"{http_err.response.status_code} {http_err.response.text}"}), http_err.response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



