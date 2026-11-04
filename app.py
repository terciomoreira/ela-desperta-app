import streamlit as st
import pandas as pd
import json
import os
import base64
from datetime import datetime

# ---------------------------------------------------------
# Configuração da Página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ela Desperta | Encontro Especial",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded"
)

DATA_FILE = "inscricoes.json"

def carregar_inscricoes():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_inscricao(nova_inscricao):
    dados = carregar_inscricoes()
    dados.append(nova_inscricao)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Conversão de imagens para Base64
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    alt_path = path + ".jpeg"
    if os.path.exists(alt_path):
        with open(alt_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

img_bg_b64 = get_image_base64("assets/background.jpeg")
img_amor_b64 = get_image_base64("assets/amor.jpeg")
bg_css_url = f"data:image/jpeg;base64,{img_bg_b64}" if img_bg_b64 else ""

# ---------------------------------------------------------
# Estilização CSS Definitiva
# ---------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    .stApp {{
        background: linear-gradient(135deg, rgba(42, 8, 21, 0.94) 0%, rgba(74, 18, 39, 0.96) 50%, rgba(31, 5, 16, 0.96) 100%),
                    url("{bg_css_url}") no-repeat center center fixed !important;
        background-size: cover !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #2A0815 0%, #1F0510 100%) !important;
        border-right: 2px solid #D4AF37 !important;
    }}

    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: #F7E7CE !important;
        font-weight: 600 !important;
    }}

    .stSidebar .stRadio label {{
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }}

    .glass-card {{
        background: rgba(35, 8, 18, 0.88);
        border: 1px solid rgba(212, 175, 55, 0.5);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        backdrop-filter: blur(12px);
    }}

    h1, h2, h3 {{
        font-family: 'Playfair Display', serif !important;
        color: #F7E7CE !important;
    }}

    .gold-title {{
        color: #F3D06C !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }}

    .gold-subtitle {{
        color: #D4AF37 !important;
        letter-spacing: 3px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.85rem;
    }}

    div[data-baseweb="radio"] label, 
    div[data-baseweb="radio"] span, 
    .stRadio div label p,
    .stRadio div label span {{
        color: #FFFFFF !important;
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.9);
    }}

    .stTextInput input {{
        background-color: rgba(255, 255, 255, 0
        