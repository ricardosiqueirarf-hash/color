
import os
import secrets
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# =====================
# CONFIG
# =====================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

if not ADMIN_USER or not ADMIN_PASS:
    raise RuntimeError("ADMIN_USER ou ADMIN_PASS não definidos no Render")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)
CORS(app)

# =====================
# UTIL
# =====================

def calcular_preco(custo, margem, perda):
    custo_com_perda = custo * (1 + perda / 100)
    return custo_com_perda * (1 + margem / 100)

# =====================
# LOGIN (API)
# =====================

@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "error": "Login ou senha ausentes"
        }), 400

    if username == ADMIN_USER and password == ADMIN_PASS:
        token = secrets.token_hex(16)
        return jsonify({
            "success": True,
            "token": token
        })

    return jsonify({
        "success": False,
        "error": "Usuário ou senha inválidos"
    }), 401

# =====================
# NO CACHE
# =====================

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# =====================
# API PERFIS
# =====================

from api_perfis import perfis_bp
app.register_blueprint(perfis_bp)

# =====================
# API VIDROS
# =====================

from api_vidros import vidros_bp
app.register_blueprint(vidros_bp)

# =====================
# API INSUMOS
# =====================

from api_insumos import insumos_bp
app.register_blueprint(insumos_bp)

# =====================
# API ORÇAMENTOS
# =====================

from api_orcamentos import orcamentos_bp
app.register_blueprint(orcamentos_bp)

# =====================
# HEALTH CHECK
# =====================

@app.route("/")
def health():
    return jsonify({"status": "ok"})

# =====================
# START
# =====================

if __name__ == "__main__":
    app.run(debug=True)

