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
def index():
    return render_template("index.html")

@app.route("/perfis-page")
def perfis_page():
    return render_template("perfis.html")

@app.route("/vidros-page")
def vidros_page():
    return render_template("vidros.html")

@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")

# =====================
# LOGIN
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "kadumon" and request.form.get("password") == "17241804":
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

@app.route("/api/perfis", methods=["GET"])
def listar_perfis():
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/perfis?select=*&order=nome.asc",
        headers=HEADERS
    )
    return jsonify(r.json()), r.status_code


@app.route("/api/perfis", methods=["POST"])
def criar_perfil():
    data = request.json

    preco = calcular_preco(
        float(data["custo"]),
        float(data["margem"]),
        float(data["perda"])
    )

    payload = {
        "nome": data["nome"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2),
        "tipologia": data.get("tipologias", [])  # 👈 AQUI
    }

    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/perfis",
        headers=HEADERS,
        json=payload
    )

    return jsonify({"status": "ok"}), r.status_code


@app.route("/api/perfis/<id>", methods=["PUT"])
def editar_perfil(id):
    data = request.json

    preco = calcular_preco(
        float(data["custo"]),
        float(data["margem"]),
        float(data["perda"])
    )

    payload = {
        "nome": data["nome"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2),
        "tipologia": data.get("tipologias", [])  # 👈 AQUI TAMBÉM
    }

    r = requests.patch(
        f"{SUPABASE_URL}/rest/v1/perfis?id=eq.{id}",
        headers=HEADERS,
        json=payload
    )

    return jsonify({"status": "updated"}), r.status_code


@app.route("/api/perfis/<id>", methods=["DELETE"])
def deletar_perfil(id):
    r = requests.delete(
        f"{SUPABASE_URL}/rest/v1/perfis?id=eq.{id}",
        headers=HEADERS
    )
    return jsonify({"status": "deleted"}), r.status_code

# =====================
# API VIDROS (inalterado)
# =====================

@app.route("/api/vidros", methods=["GET"])
def listar_vidros():
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/vidros?select=*&order=tipo.asc",
        headers=HEADERS
    )
    return jsonify(r.json()), r.status_code


@app.route("/api/vidros", methods=["POST"])
def criar_vidro():
    data = request.json

    preco = calcular_preco(
        float(data["custo"]),
        float(data["margem"]),
        float(data["perda"])
    )

    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }

    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/vidros",
        headers=HEADERS,
        json=payload
    )

    return jsonify({"status": "ok"}), r.status_code


@app.route("/api/vidros/<id>", methods=["PUT"])
def editar_vidro(id):
    data = request.json

    preco = calcular_preco(
        float(data["custo"]),
        float(data["margem"]),
        float(data["perda"])
    )

    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }

    r = requests.patch(
        f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}",
        headers=HEADERS,
        json=payload
    )

    return jsonify({"status": "updated"}), r.status_code


@app.route("/api/vidros/<id>", methods=["DELETE"])
def deletar_vidro(id):
    r = requests.delete(
        f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}",
        headers=HEADERS
    )
    return jsonify({"status": "deleted"}), r.status_code

# =====================
# START
# =====================

if __name__ == "__main__":
    app.run()

