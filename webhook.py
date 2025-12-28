from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "meu_token_verificacao"
WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]

# ===================== VERIFICAÇÃO META =====================
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erro", 403

# ===================== RECEBER MSG =====================
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = msg["from"]
        text = msg["text"]["body"].lower()

        resposta = processar_mensagem(text)

        enviar_mensagem(from_number, resposta)
    except Exception as e:
        print("Erro:", e)

    return jsonify(status="ok"), 200

# ===================== ENVIAR MSG =====================
def enviar_mensagem(numero, texto):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=payload)

# ===================== LÓGICA INICIAL =====================
def processar_mensagem(texto):
    if "porta" in texto:
        return "Certo. Qual perfil? Ex: 1036, 2215"
    return "Sou o bot de orçamentos. Digite PORTA para começar."
