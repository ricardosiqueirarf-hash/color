import os
from flask import Flask, jsonify, request, make_response, redirect
from flask_cors import CORS
from functools import wraps

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
# DECORATOR PARA PROTEGER ROTAS
# =====================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = (
            request.headers.get("Authorization") or
            request.args.get("token") or
            request.cookies.get("ADMIN_TOKEN") or
            request.headers.get("X-ADMIN-TOKEN")
        )
        if not token or token != f"Bearer {ADMIN_TOKEN}":
            # Redireciona direto para o domínio do Render, sem /login
            return redirect("https://colorglass.onrender.com")
        return f(*args, **kwargs)
    return decorated

# =====================
# LOGIN (HTML incorporado)
# =====================
@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if not data or "password" not in data:
            return jsonify({"error": "Senha não enviada"}), 400
        if data["password"] != ADMIN_PASSWORD:
            return jsonify({"error": "Senha incorreta"}), 401
        return jsonify({"success": True, "token": ADMIN_TOKEN})

    # GET -> mostra o login
    login_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Login | ColorGlass</title>
        <style>
            * {{ box-sizing: border-box; font-family: Arial, Helvetica, sans-serif; }}
            body {{ margin:0; height:100vh; display:flex; justify-content:center; align-items:center; background:#111; color:#fff; }}
            .login-container {{ background:#222; padding:30px; border-radius:10px; width:400px; text-align:center; }}
            input {{ width:100%; padding:10px; margin:10px 0; border-radius:5px; border:none; }}
            button {{ padding:10px 20px; border:none; border-radius:5px; cursor:pointer; background:#2a9ecb; color:#fff; }}
            .error {{ background:#f44336; color:#fff; padding:8px; border-radius:5px; margin-bottom:10px; display:none; }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>ColorGlass</h2>
            <form id="loginForm">
                <input type="password" name="password" placeholder="Digite a senha" required>
                <div class="error" id="errorMsg"></div>
                <button type="submit">Entrar</button>
            </form>
        </div>
        <script>
            const form = document.getElementById('loginForm');
            form.addEventListener('submit', async (e) => {{
                e.preventDefault();
                const password = form.password.value.trim();
                const res = await fetch('/', {{
                    method:'POST',
                    headers:{{'Content-Type':'application/json'}},
                    body: JSON.stringify({{ password }})
                }});
                const data = await res.json();
                if(data.success){{
                    localStorage.setItem('ADMIN_TOKEN', data.token);
                    window.location.href = '/';
                }} else {{
                    const msg = document.getElementById('errorMsg');
                    msg.style.display = 'block';
                    msg.textContent = data.error || 'Senha inválida';
                }}
            }});
        </script>
    </body>
    </html>
    """
    response = make_response(login_html)
    response.headers["Content-Type"] = "text/html"
    return response

# =====================
# ROTAS PROTEGIDAS DE EXEMPLO
# =====================
@app.route("/index.html")
@token_required
def index():
    return "<h1>Bem-vindo ao ColorGlass! Você passou pelo login.</h1>"

@app.route("/vidros.html")
@token_required
def vidros():
    return "<h1>Vidros - Acesso permitido</h1>"

@app.route("/perfis.html")
@token_required
def perfis():
    return "<h1>Perfis - Acesso permitido</h1>"

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