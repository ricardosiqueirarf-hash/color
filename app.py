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
# PÁGINAS (TODAS PROTEGIDAS)
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
    return jsonify(r.json()), r.status_code

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
    return jsonify({"status": "ok"}), r.status_code

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
    return jsonify({"status": "updated"}), r.status_code

@app.route("/api/perfis/<id>", methods=["DELETE"])
@login_required
def deletar_perfil(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/perfis?id=eq.{id}", headers=HEADERS)
    return jsonify({"status": "deleted"}), r.status_code

# =====================
# API VIDROS
# =====================

@app.route("/api/vidros", methods=["GET"])
@login_required
def listar_vidros():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/vidros?select=*&order=tipo.asc", headers=HEADERS)
    return jsonify(r.json()), r.status_code

@app.route("/api/vidros", methods=["POST"])
@login_required
def criar_vidro():
    data = request.json
    preco = calcular_preco(float(data["custo"]), float(data["margem"]), float(data["perda"]))
    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/vidros", headers=HEADERS, json=payload)
    return jsonify({"status": "ok"}), r.status_code

@app.route("/api/vidros/<id>", methods=["PUT"])
@login_required
def editar_vidro(id):
    data = request.json
    preco = calcular_preco(float(data["custo"]), float(data["margem"]), float(data["perda"]))
    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}", headers=HEADERS, json=payload)
    return jsonify({"status": "updated"}), r.status_code

@app.route("/api/vidros/<id>", methods=["DELETE"])
@login_required
def deletar_vidro(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}", headers=HEADERS)
    return jsonify({"status": "deleted"}), r.status_code

# =====================
# API ORÇAMENTO
# =====================

@app.route("/api/orcamento", methods=["POST"])
@login_required
def criar_orcamento():
    data = request.json
    cliente_nome = data.get("cliente_nome")
    portas = data.get("portas", [])

    if not cliente_nome:
        return jsonify({"success": False, "error": "Cliente não informado"}), 400

    # Buscar o último número de pedido
    r_last = requests.get(f"{SUPABASE_URL}/rest/v1/orcamentos?select=numero_pedido&order=numero_pedido.desc&limit=1", headers=HEADERS)
    last_pedido = r_last.json()
    numero_pedido = (last_pedido[0]['numero_pedido'] + 1) if last_pedido else 1

    # Criar orçamento
    payload = {
        "cliente_nome": cliente_nome,
        "numero_pedido": numero_pedido
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/orcamentos", headers=HEADERS, json=payload)
    if r.status_code not in [200,201]:
        return jsonify({"success": False, "error": "Erro ao criar orçamento"}), r.status_code

    orcamento = r.json()
    orcamento_id = orcamento[0]["id"] if isinstance(orcamento, list) and len(orcamento) > 0 else None
    if not orcamento_id:
        return jsonify({"success": False, "error": "Não retornou ID do orçamento"}), 500

    # Salvar portas vinculadas ao orçamento
    portas_payload = []
    for p in portas:
        portas_payload.append({
            "orcamento_id": orcamento_id,
            "tipologia": p.get("tipologia"),
            "dados": p.get("dados"),
            "svg": p.get("svg")
        })
    if portas_payload:
        r_portas = requests.post(f"{SUPABASE_URL}/rest/v1/portas", headers=HEADERS, json=portas_payload)
        if r_portas.status_code not in [200,201]:
            return jsonify({"success": False, "error": "Erro ao salvar portas"}), r_portas.status_code

    return jsonify({
        "success": True,
        "id": orcamento_id,
        "numero_pedido": numero_pedido,
        "cliente_nome": cliente_nome
    })

# =====================
# START
# =====================

if __name__ == "__main__":
    app.run()

