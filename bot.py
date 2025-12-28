from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ===================== CONFIGURAÇÕES =====================
# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xyz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "SEU_SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# WhatsApp Business
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "SEU_PHONE_ID")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "SEU_TEMPORARY_ACCESS_TOKEN")
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"

# ===================== FUNÇÕES =====================
def enviar_mensagem_whatsapp(numero, mensagem):
    """Envia mensagem pelo WhatsApp Business API"""
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensagem}
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    r = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

def calcular_preco_porta(largura, altura, perfil_id=None, vidro_id=None):
    """Busca perfis/vidros no Supabase e calcula preço da porta"""
    # Pegar todos os perfis
    r = requests.get(f"{SUPABASE_URL}/rest/v1/perfis?select=*", headers=HEADERS)
    r.raise_for_status()
    perfis = r.json()

    # Pegar todos os vidros
    r = requests.get(f"{SUPABASE_URL}/rest/v1/vidros?select=*", headers=HEADERS)
    r.raise_for_status()
    vidros = r.json()

    preco_perfil = 0
    preco_vidro = 0

    if perfil_id:
        perfil = next((p for p in perfis if p["id"] == perfil_id), None)
        if perfil:
            preco_perfil = perfil["preco"] * 2 * (largura + altura)

    if vidro_id:
        vidro = next((v for v in vidros if v["id"] == vidro_id), None)
        if vidro:
            preco_vidro = vidro["preco"] * largura * altura

    return round(preco_perfil + preco_vidro, 2)

# ===================== ROTAS WHATSAPP =====================
@app.route("/webhook", methods=["GET"])
def webhook_verificacao():
    """Webhook GET para verificação do WhatsApp"""
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == os.getenv("WHATSAPP_VERIFY_TOKEN", "meu_token_de_verificacao"):
        return challenge
    return "Token incorreto", 403

@app.route("/webhook", methods=["POST"])
def webhook_receber():
    """Recebe mensagens do WhatsApp"""
    data = request.json
    try:
        if "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    mensagem_obj = change.get("value", {}).get("messages", [])
                    for msg in mensagem_obj:
                        numero = msg["from"]
                        texto = msg.get("text", {}).get("body", "").lower()

                        # ===================== LÓGICA DO BOT =====================
                        if "preço" in texto or "orçamento" in texto:
                            try:
                                params = {}
                                for part in texto.split():
                                    if "=" in part:
                                        k, v = part.split("=")
                                        params[k] = v

                                largura = float(params.get("largura", 0)) / 1000
                                altura = float(params.get("altura", 0)) / 1000
                                perfil_id = params.get("perfil")
                                vidro_id = params.get("vidro")

                                preco = calcular_preco_porta(largura, altura, perfil_id, vidro_id)
                                resposta = f"O preço estimado da porta é: R$ {preco:.2f}"
                            except Exception as e:
                                resposta = f"Erro ao calcular o preço: {str(e)}"
                        else:
                            resposta = "Olá! Para calcular o preço de uma porta, envie algo como:\naltura=200 largura=100 perfil=<id> vidro=<id>"

                        enviar_mensagem_whatsapp(numero, resposta)
        return jsonify({"status": "ok"})
    except Exception as e:
        print("Erro webhook:", e)
        return jsonify({"error": str(e)}), 500

# ===================== RODA APP =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
