import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# =====================
# CONFIG GLOBAL
# =====================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL ou SUPABASE_KEY não definidos")

if not ADMIN_PASSWORD or not ADMIN_TOKEN:
    raise RuntimeError("ADMIN_PASSWORD ou ADMIN_TOKEN não definidos")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# =====================
# APP
# =====================

app = Flask(__name__)
CORS(app)

# =====================
# HEALTH CHECK
# =====================

@app.route("/")
def health():
    return jsonify({
        "status": "ok",
        "service": "ColorGlass API"
    })

# =====================
# LOGIN (SENHA ÚNICA)
# =====================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data or "password" not in data:
        return jsonify({"error": "Senha não enviada"}), 400

    if data["password"] != ADMIN_PASSWORD:
        return jsonify({"error": "Senha incorreta"}), 401

    return jsonify({
        "token": ADMIN_TOKEN
    })

# =====================
# REGISTRO DE BLUEPRINTS
# =====================

from api_perfis import perfis_bp
from api_vidros import vidros_bp
from api_insumos import insumos_bp
from api_orcamentos import orcamentos_bp

app.register_blueprint(perfis_bp)
app.register_blueprint(vidros_bp)
app.register_blueprint(insumos_bp)
app.register_blueprint(orcamentos_bp)

# =====================
# NO CACHE (ANTI BUG FRONT)
# =====================

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# =====================
# START LOCAL
# =====================

if __name__ == "__main__":
    app.run(debug=True)