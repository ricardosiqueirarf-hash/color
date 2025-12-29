import os
from functools import wraps
from flask import request, jsonify

# Token fixo definido no Render (Environment Variables)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

if not ADMIN_TOKEN:
    raise RuntimeError("ADMIN_TOKEN não definido nas variáveis de ambiente")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header ausente"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Formato inválido. Use Bearer <token>"}), 401

        token = auth_header.split(" ", 1)[1].strip()

        if token != ADMIN_TOKEN:
            return jsonify({"error": "Token inválido"}), 403

        return f(*args, **kwargs)

    return decorated