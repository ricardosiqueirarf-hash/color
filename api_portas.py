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
    Recebe um JSON com lista de portas e salva no Supabase vinculando ao orcamento_uuid.
    Converte 'dados' para array de texto (text[]) antes de enviar.
    Inclui 'quantidade' no payload.
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
            # converte dict para array de texto: ["chave:valor", ...]
            dados_array = [f"{k}:{v}" for k, v in dados_obj.items()]

            payload.append({
                "orcamento_uuid": p.get("orcamento_uuid", orcamento_uuid),
                "tipo": p.get("tipo"),
                "dados": dados_array,
                "quantidade": p.get("quantidade", 1),  # quantidade adicionada
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

    except requests.HTTPError as http_err:
        return jsonify({"success": False, "error": f"{http_err.response.status_code} {http_err.response.text}"}), http_err.response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@portas_bp.route("/api/orcamento/<orcamento_uuid>/portas", methods=["GET"])
def listar_portas(orcamento_uuid):
    """
    Lista todas as portas vinculadas a um determinado orçamento.
    Converte 'dados' de text[] de volta para dict.
    Inclui 'quantidade' ao retornar.
    """
    from app import SUPABASE_URL, HEADERS
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/portas?orcamento_uuid=eq.{orcamento_uuid}",
            headers=HEADERS
        )
        r.raise_for_status()

        portas = r.json()
        # converte array de texto de volta para dict
        for p in portas:
            dados_array = p.get("dados", [])
            if isinstance(dados_array, list):
                p["dados"] = dict(item.split(":", 1) for item in dados_array if ":" in item)
            # garante que quantidade seja um inteiro
            p["quantidade"] = int(p.get("quantidade", 1))

        return jsonify({"success": True, "portas": portas})
    except requests.HTTPError as http_err:
        return jsonify({"success": False, "error": f"{http_err.response.status_code} {http_err.response.text}"}), http_err.response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


