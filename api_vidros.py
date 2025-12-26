# =====================
# API VIDROS
# =====================

@app.route("/api/vidros", methods=["GET"])
@login_required
def listar_vidros():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/vidros?select=*&order=tipo.asc", headers=HEADERS)
    r.raise_for_status()
    return jsonify(r.json())

@app.route("/api/vidros", methods=["POST"])
@login_required
def criar_vidro():
    data = request.json
    preco = float(data["custo"]) * (1 + float(data["margem"])/100) * (1 + float(data["perda"])/100)
    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.post(f"{SUPABASE_URL}/rest/v1/vidros", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "ok"})

@app.route("/api/vidros/<id>", methods=["PUT"])
@login_required
def editar_vidro(id):
    data = request.json
    preco = float(data["custo"]) * (1 + float(data["margem"])/100) * (1 + float(data["perda"])/100)
    payload = {
        "tipo": data["tipo"],
        "espessura": data["espessura"],
        "custo": data["custo"],
        "margem": data["margem"],
        "perda": data["perda"],
        "preco": round(preco, 2)
    }
    r = requests.patch(f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}", headers=HEADERS, json=payload)
    r.raise_for_status()
    return jsonify({"status": "updated"})

@app.route("/api/vidros/<id>", methods=["DELETE"])
@login_required
def deletar_vidro(id):
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{id}", headers=HEADERS)
    r.raise_for_status()
    return jsonify({"status": "deleted"})
