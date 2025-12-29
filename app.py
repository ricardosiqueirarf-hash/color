import os
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from functools import wraps
import jwt
import datetime

# =====================
# CONFIG GLOBAL
# =====================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")  # chave para assinar tokens JWT

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL ou SUPABASE_KEY não definidos")

if not ADMIN_PASSWORD or not SECRET_KEY:
    raise RuntimeError("ADMIN_PASSWORD ou SECRET_KEY não definidos")

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

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ColorGlass API"})

# =====================
# GERAR TOKEN
# =====================

@app.route("/get_token", methods=["POST"])
def get_token():
    data = request.get_json(silent=True)
    if not data or "password" not in data:
        return jsonify({"error": "Senha não enviada"}), 400

    if data["password"] != ADMIN_PASSWORD:
        return jsonify({"error": "Senha incorreta"}), 401

    # Cria token JWT válido por 12 horas
    payload = {
        "user": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

# =====================
# DECORATOR PARA PROTEGER ROTAS
# =====================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token não fornecido"}), 401

        token = token.split(" ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated

# =====================
# ROTAS PROTEGIDAS
# =====================

@app.route("/")
@token_required
def index():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>ColorGlass - Home</title>
    </head>
    <body>
        <h1>Bem-vindo ao ColorGlass!</h1>
        <p>Você está logado e todas as páginas protegidas estão liberadas.</p>
    </body>
    </html>
    """

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
# START
# =====================

if __name__ == "__main__":
    app.run(debug=True)