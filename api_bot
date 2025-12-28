from flask import Blueprint, request, jsonify
import re
import requests

bot_bp = Blueprint("bot_bp", __name__)

# =====================
# HELPERS
# =====================
def extrair_dimensoes(texto):
    """
    Extrai algo como 80x210 ou 800x2100
    Retorna mm
    """
    match = re.search(r"(\d{2,4})\s*[xX]\s*(\d{2,4})", texto)
    if not match:
        return None, None

    w = int(match.group(1))
    h = int(match.group(2))

    # se veio em cm, converte pra mm
    if w < 1000:
        w *= 10
    if h < 1000:
        h *= 10

    return w, h


def buscar_perfil_por_nome(nome):
    from app import SUPABASE_URL, HEADERS
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/perfis?nome=ilike.*{nome}*&select=*",
        headers=HEADERS
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def buscar_vidro_por_nome(nome):
    from app import SUPABASE_URL, HEADERS
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/vidros?tipo=ilike.*{nome}*&select=*",
        headers=HEADERS
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


# =====================
# ROTA BOT
# =====================
@bot_bp.route("/api/bot", methods=["POST"])
def bot():
    """
    Espera:
    {
        "mensagem": "porta 80x210 perfil 2215 vidro reflecta"
    }
    """

    texto = request.json.get("mensagem", "").lower()

    largura, altura = extrair_dimensoes(texto)
    if not largura or not altura:
        return jsonify({"resposta": "Informe as medidas no formato 80x210."})

    perfil = None
    vidro = None

    for palavra in texto.split():
        if not perfil:
            perfil = buscar_perfil_por_nome(palavra)
        if not vidro:
            vidro = buscar_vidro_por_nome(palavra)

    if not perfil:
        return jsonify({"resposta": "Não encontrei o perfil informado."})

    if not vidro:
        return jsonify({"resposta": "Não encontrei o vidro informado."})

    # chama o motor de cálculo
    from api_portas import calcular_preco_porta

    preco = calcular_preco_porta(
        largura_mm=largura,
        altura_mm=altura,
        perfil=perfil,
        vidro=vidro
    )

    return jsonify({
        "resposta": (
            f"Orçamento estimado:\n"
            f"📐 {largura/10:.0f}x{altura/10:.0f} cm\n"
            f"🧱 Perfil: {perfil['nome']}\n"
            f"🪟 Vidro: {vidro['tipo']}\n"
            f"💰 Valor: R$ {preco:.2f}"
        )
    })
