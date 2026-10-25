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
# Estilização CSS Definitiva (Botão com Estilo Idêntico à Caixa de Pagamento)
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
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #2A0815 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        border: 2px solid #D4AF37 !important;
        padding: 12px !important;
    }}

    /* BOTÃO DE CONFIRMAÇÃO COM O MESMO ESTILO DA CAIXA DE PAGAMENTO (FUNDO ESCURO + BORDAS DOURADAS) */
    .stButton > button {{
        background: rgba(35, 8, 18, 0.95) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 20px !important;
        padding: 18px 32px !important;
        width: 100% !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
        transition: all 0.3s ease !important;
    }}

    /* TEXTO DO BOTÃO EM DOURADO BRILHANTE E NEGRITO VISÍVEL */
    .stButton > button p, 
    .stButton > button span, 
    .stButton > button div, 
    .stButton > button * {{
        color: #F3D06C !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.5px !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        border-color: #FFE58F !important;
        background: rgba(55, 12, 28, 0.98) !important;
        box-shadow: 0 12px 35px rgba(212, 175, 55, 0.4) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Navegação
# ---------------------------------------------------------
menu = st.sidebar.radio("📌 Menu de Navegação", [
                        "🌸 Convite & Inscrição", "📊 Painel da Gestora (Admin)"])

if menu == "🌸 Convite & Inscrição":

    if img_bg_b64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <img src="data:image/jpeg;base64,{img_bg_b64}" style="max-width: 100%; border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.7); border: 2px solid rgba(212,175,55,0.4);">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <p class="gold-subtitle">✦ ENCONTRO EXCLUSIVO DE TRANSFORMAÇÃO ✦</p>
        <h1 class="gold-title">ELA DESPERTA</h1>
        <p style="font-size: 1.15rem; color: #FAF6F8 !important; margin-top: 12px; line-height: 1.6;">
            Um espaço seguro para resgatar a sua identidade, fortalecer a sua autoestima e despertar a mulher extraordinária que há em si.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="medium")
    with col1:
        if img_amor_b64:
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{img_amor_b64}" style="width: 100%; border-radius: 16px; border: 2px solid #D4AF37; box-shadow: 0 10px 25px rgba(0,0,0,0.6);">
                <p style="color: #F3D06C !important; font-weight: bold; margin-top: 10px; font-size: 1.1rem;">Emily Gisto Araujo</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #F3D06C !important; margin-top:0;">Uma Mensagem Especial para Si</h3>
            <p style="line-height: 1.7; color: #FFFFFF !important; font-size: 1.02rem;">
                Muitas vezes, passamos a vida a cuidar de tudo e de todos, esquecendo-nos da nossa própria essência. 
                Este encontro foi desenhado ao detalhe para a ajudar a pausar, refletir e dar o próximo passo na sua jornada com propósito e leveza.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("form_inscricao", clear_on_submit=True):
        st.markdown(
            "<h2 style='color: #F3D06C !important; text-align: center;'>Formulário de Inscrição</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(212,175,55,0.3);'>",
                    unsafe_allow_html=True)

        st.markdown(
            "<p style='color: #F7E7CE; font-weight: 700;'>1. Qual é o seu nome completo?</p>", unsafe_allow_html=True)
        nome = st.text_input("Nome", label_visibility="collapsed",
                             placeholder="O seu nome completo...")

        st.markdown(
            "<p style='color: #F7E7CE; font-weight: 700;'>Qual é o seu e-mail de contacto?</p>", unsafe_allow_html=True)
        email = st.text_input(
            "Email", label_visibility="collapsed", placeholder="exemplo@email.com")

        st.markdown(
            "<p style='color: #F7E7CE; font-weight: 700;'>2. Qual é o seu contacto de WhatsApp?</p>", unsafe_allow_html=True)
        whatsapp = st.text_input(
            "WhatsApp", label_visibility="collapsed", placeholder="+351 900 000 000")

        st.markdown(
            "<p style='color: #F7E7CE; font-weight: 700;'>3. O que a motivou a querer participar no Ela Desperta?</p>", unsafe_allow_html=True)
        motivacao = st.radio(
            "Motivação",
            [
                "Quero conhecer-me melhor",
                "Quero fortalecer a minha identidade e autoestima",
                "Quero compreender padrões que se repetem na minha vida",
                "Quero aproximar-me mais de Deus",
                "Senti que este encontro é para mim",
                "Outro motivo"
            ],
            label_visibility="collapsed"
        )

        st.markdown(
            "<p style='color: #F7E7CE; font-weight: 700;'>4. Em que área da sua vida sente que precisa de despertar?</p>", unsafe_allow_html=True)
        area_despertar = st.radio(
            "Área",
            [
                "Amor-próprio e identidade",
                "Relações familiares e afetivas",
                "Medos e inseguranças",
                "Propósito e direção de vida",
                "Crenças e padrões que me limitam",
                "Um pouco de tudo"
            ],
            label_visibility="collapsed"
        )

        st.markdown("<p style='color: #F7E7CE; font-weight: 700;'>5. Confirma a sua participação e compreende o valor de inscrição?</p>", unsafe_allow_html=True)
        confirmacao = st.radio(
            "Confirmação",
            [
                "Sim, confirmo a minha participação e aceito o valor de 17 €",
                "Ainda preciso de esclarecer algumas dúvidas"
            ],
            label_visibility="collapsed"
        )

        st.markdown("""
        <div class="glass-card" style="margin-top: 25px; border: 2px solid #D4AF37;">
            <h3 style="color: #F3D06C !important; margin-top:0;">💳 Informações de Pagamento</h3>
            <p>Valor: <b style="color: #F3D06C;">17 €</b> (destinado ao <i>coffee break</i> do hotel).</p>
            <p>IBAN: <b style="color: #F3D06C;">PT50581000019000006564779</b> (Titular: <i>Emily Gisto Araujo</i>)</p>
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "✨ Confirmar a minha Inscrição com Propósito")

        if submitted:
            if not nome or not whatsapp or not email:
                st.error("Por favor, preencha o seu Nome, E-mail e WhatsApp.")
            else:
                nova_entry = {
                    "data_inscricao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nome": nome,
                    "email": email,
                    "whatsapp": whatsapp,
                    "motivacao": motivacao,
                    "area_despertar": area_despertar,
                    "status_confirmacao": confirmacao
                }
                guardar_inscricao(nova_entry)
                st.balloons()
                st.success(
                    "Inscrição efetuada com sucesso! Esperamos por si. 🌸")

elif menu == "📊 Painel da Gestora (Admin)":
    st.markdown("<h1 class='gold-title'>📊 Painel de Controlo da Gestora</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='color: #E8C5C8;'>Acompanhe em tempo real as inscrições, contactos de WhatsApp/E-mail e métricas do evento.</p>", unsafe_allow_html=True)
    st.divider()

    senha = st.text_input(
        "Introduza a palavra-passe de acesso:", type="password")

    if senha == "crearis2026":
        st.success("Acesso autorizado com sucesso!")
        inscricoes = carregar_inscricoes()

        if len(inscricoes) == 0:
            st.info("Ainda não existem participantes inscritos.")
        else:
            df = pd.DataFrame(inscricoes)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Inscritos", len(df))
            confirmadas = len(
                df[df['status_confirmacao'].str.contains("Sim", na=False)])
            col2.metric("Inscrições Confirmadas", confirmadas)
            col3.metric("Valor Arrecadado", f"{confirmadas * 17} €")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📋 Lista Completa de Participantes (Leads)")

            st.dataframe(df, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Descarregar Lista de Participantes (CSV)",
                data=csv,
                file_name="participantes_ela_desperta.csv",
                mime="text/csv",
            )
    elif senha != "":
        st.error("Palavra-passe incorreta. Tente novamente.")
