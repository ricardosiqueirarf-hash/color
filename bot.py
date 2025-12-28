from flask import Blueprint, request, jsonify
import requests

portas_bp = Blueprint("portas_bp", __name__)

# =====================
# UTIL
# =====================
def calcular_preco_porta(largura_mm, altura_mm, perfil, vidro):
    """
    largura_mm, altura_mm em milímetros
    perfil: dict do Supabase (preco = R$/m)
    vidro: dict do Supabase (preco = R$/m²)
    """

    largura = largura_mm / 1000
    altura = altura_mm / 1000

    preco_perfil = 0
    preco_vidro = 0

    if perfil:
        perimetro = 2 * (largura + altura)
        preco_perfil = perfil["preco"] * perimetro

    if vidro:
        area = largura * altura
        preco_vidro = vidro["preco"] * area

    return round(preco_perfil + preco_vidro, 2)


# =====================
# HELPERS SUPABASE
# =====================
def buscar_perfil(perfil_id):
    from app import SUPABASE_URL, HEADERS
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/perfis?id=eq.{perfil_id}&select=*",
        headers=HEADERS
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def buscar_vidro(vidro_id):
    from app import SUPABASE_URL, HEADERS
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/vidros?id=eq.{vidro_id}&select=*",
        headers=HEADERS
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


# =====================
# ROTA ORÇAMENTO PORTA
# =====================
@portas_bp.route("/api/orcar-porta", methods=["POST"])
def orcar_porta():
    """
    Espera:
    {
        "largura": 800,
        "altura": 2100,
        "perfil_id": "...",
        "vidro_id": "..."
    }
    """

    data = request.json

    largura = float(data["largura"])
    altura = float(data["altura"])
    perfil_id = data.get("perfil_id")
    vidro_id = data.get("vidro_id")

    perfil = buscar_perfil(perfil_id) if perfil_id else None
    vidro = buscar_vidro(vidro_id) if vidro_id else None

    preco = calcular_preco_porta(
        largura_mm=largura,
        altura_mm=altura,
        perfil=perfil,
        vidro=vidro
    )

    return jsonify({
        "largura": largura,
        "altura": altura,
        "perfil": perfil["nome"] if perfil else None,
        "vidro": vidro["tipo"] if vidro else None,
        "preco": preco
    })

