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

@app.route("/api/perfis", methods=["GET"])
@login_required
def listar_perfis():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/perfis?select=*&order=nome.asc", headers=HEADERS)
    r.raise_for_status()
    return jsonify(r.json())

@app.route("/api/perfis", methods=["POST"])
@login_required
def criar_perfil():
    data = request.json
    preco = calcular_preco(float(data["custo"]), float(data["margem"]), float(data["perda"]))
    payload = {
        "nome": data["nome"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2),
        "tipologias": data.get("tipologias", [])
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/perfis", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "ok"})

@app.route("/api/perfis/<id>", methods=["PUT"])
@login_required
def editar_perfil(id):
    data = request.json
    preco = calcular_preco(float(data["custo"]), float(data["margem"]), float(data["perda"]))
    payload = {
        "nome": data["nome"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2),
        "tipologias": data.get("tipologias", [])
    }
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/perfis?id=eq.{id}", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "updated"})

@app.route("/api/perfis/<id>", methods=["DELETE"])
@login_required
def deletar_perfil(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/perfis?id=eq.{id}", headers=HEADERS)
    r.raise_for_status()
    return jsonify({"status": "deleted"})

# =====================
# API ORÇAMENTOS
# =====================

@app.route("/api/orcamento", methods=["POST"])
def criar_orcamento():
    data = request.json
    cliente_nome = data.get("cliente_nome")
    if not cliente_nome:
        return jsonify({"success": False, "error": "Cliente não informado"}), 400

    try:
        # Buscar último número de pedido
        r_last = requests.get(
            f"{SUPABASE_URL}/rest/v1/orcamentos?select=numero_pedido&order=numero_pedido.desc&limit=1",
            headers=HEADERS
        )
        r_last.raise_for_status()
        last_pedido = r_last.json()
        numero_pedido = (last_pedido[0]['numero_pedido'] + 1) if last_pedido else 1

        # Criar o novo cliente/orçamento no Supabase
        payload = {"cliente_nome": cliente_nome, "numero_pedido": numero_pedido}
        r_post = requests.post(
            f"{SUPABASE_URL}/rest/v1/orcamentos",
            headers={**HEADERS, "Content-Type": "application/json", "Prefer": "return=representation"},
            json=payload
        )
        r_post.raise_for_status()
        new_orcamento = r_post.json()

        # Retornar sucesso com o ID real
        return jsonify({
            "success": True,
            "id": new_orcamento[0]['id'],
            "numero_pedido": numero_pedido,
            "cliente_nome": cliente_nome
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/orcamentos", methods=["GET"])
def listar_orcamentos():
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/orcamentos?select=id,numero_pedido,cliente_nome,data_criacao&order=numero_pedido.asc",
            headers=HEADERS
        )
        r.raise_for_status()
        return jsonify({"success": True, "orcamentos": r.json()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# =====================
# START
# =====================

if __name__ == "__main__":
    app.run(debug=True)


