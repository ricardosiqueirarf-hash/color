import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import requests
from functools import wraps

# =====================
# CONFIG
# =====================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

CORS(app)

# =====================
# CÁLCULOS
# =====================

def calcular_preco(custo, margem, perda):
    custo_com_perda = custo * (1 + perda / 100)
    return custo_com_perda * (1 + margem / 100)

# =====================
# AUTH
# =====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# =====================
# NO CACHE
# =====================

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Surrogate-Control"] = "no-store"
    return response

# =====================
# PÁGINAS
# =====================

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/perfis-page")
@login_required
def perfis_page():
    return render_template("perfis.html")

@app.route("/vidros-page")
@login_required
def vidros_page():
    return render_template("vidros.html")

@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")

@app.route("/producao-page")
@login_required
def producao_page():
    return render_template("producao.html")

@app.route("/insumos-page")
@login_required
def insumos_page():
    return render_template("insumos.html")

@app.route("/orcamentos-page")
@login_required
def orcamentos_page():
    return render_template("orcamentos.html")

# =====================
# LOGIN
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "kadumon" and password == "17241804":
            session["logged_in"] = True
            return redirect(request.args.get("next") or url_for("index"))
        return render_template("login.html", error="Usuário ou senha inválidos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/check_session")
def check_session():
    return jsonify({"logged_in": "logged_in" in session})

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
# API MATERIAIS / INSUMOS
# =====================

from api_insumos import insumos_bp
app.register_blueprint(insumos_bp)

# =====================
# API ORÇAMENTOS
# =====================

from api_orcamentos import orcamentos_bp
app.register_blueprint(orcamentos_bp)

# =====================
# START
# =====================

if __name__ == "__main__":
    app.run(debug=True)


