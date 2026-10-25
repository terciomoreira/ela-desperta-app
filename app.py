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
    initial_sidebar_state="collapsed"
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

# Conversão de imagens para Base64 para garantir carregamento perfeito


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
# Estilização CSS e Movimento (Cores Vivas e Contraste Absoluto)
# ---------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Fundo dinâmico com a imagem do evento texturizada */
    .stApp {{
        background: linear-gradient(135deg, rgba(42, 8, 21, 0.92) 0%, rgba(74, 18, 39, 0.95) 50%, rgba(31, 5, 16, 0.95) 100%),
                    url("{bg_css_url}") no-repeat center center fixed !important;
        background-size: cover !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* Animações fluidas de movimento */
    @keyframes fadeInSlide {{
        from {{ opacity: 0; transform: translateY(25px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes goldGlow {{
        0% {{ box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }}
        50% {{ box-shadow: 0 0 35px rgba(212, 175, 55, 0.7); }}
        100% {{ box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }}
    }}

    .animated-block {{
        animation: fadeInSlide 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    /* Cartões e caixas com efeito de vidro elegante */
    .glass-card {{
        background: rgba(35, 8, 18, 0.88);
        border: 1px solid rgba(212, 175, 55, 0.5);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        backdrop-filter: blur(12px);
        animation: goldGlow 5s infinite;
    }}

    .content-box {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }}

    .content-box:hover {{
        transform: translateY(-3px);
        border-color: #D4AF37;
    }}

    /* Tipografia de Alta Qualidade */
    h1, h2, h3 {{
        font-family: 'Playfair Display', serif !important;
        color: #F7E7CE !important;
    }}

    .gold-title {{
        color: #F3D06C !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        letter-spacing: 1px;
    }}

    .gold-subtitle {{
        color: #D4AF37 !important;
        letter-spacing: 3px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.85rem;
    }}

    /* CORREÇÃO TOTAL DO CONTRASTE DE TODAS AS OPÇÕES E BOTÕES DE RÁDIO */
    .stRadio label, div[data-baseweb="radio"] div {{
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.9);
    }}
    
    .stRadio span {{
        color: #FFFFFF !important;
    }}

    /* Inputs de Texto */
    .stTextInput input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #2A0815 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        border: 2px solid #D4AF37 !important;
        padding: 12px !important;
    }}

    /* Botão Principal Dourado com Animação ao Passar o Rato */
    .stButton>button {{
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #2A0815 !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        border-radius: 30px !important;
        padding: 15px 32px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 15px;
    }}

    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.8);
        background: linear-gradient(135deg, #F3D06C 0%, #D4AF37 100%) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Navegação
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Navegação", ["Convite & Inscrição", "Painel da Gestora (Admin)"])

if menu == "Convite & Inscrição":

    # 1. Poster Principal com Efeito Dinâmico
    if img_bg_b64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;" class="animated-block">
            <img src="data:image/jpeg;base64,{img_bg_b64}" style="max-width: 100%; border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.7); border: 2px solid rgba(212,175,55,0.4);">
        </div>
        """, unsafe_allow_html=True)

    # 2. Hero Box de Apresentação
    st.markdown("""
    <div class="glass-card animated-block" style="text-align: center;">
        <p class="gold-subtitle">✦ ENCONTRO EXCLUSIVO DE TRANSFORMAÇÃO ✦</p>
        <h1 class="gold-title">ELA DESPERTA</h1>
        <p style="font-size: 1.15rem; color: #FAF6F8 !important; margin-top: 12px; line-height: 1.6;">
            Um espaço seguro para resgatar a sua identidade, fortalecer a sua autoestima e despertar a mulher extraordinária que há em si.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3. Apresentação da Palestrante
    col1, col2 = st.columns([1, 2], gap="medium")
    with col1:
        if img_amor_b64:
            st.markdown(f"""
            <div style="text-align: center;" class="animated-block">
                <img src="data:image/jpeg;base64,{img_amor_b64}" style="width: 100%; border-radius: 16px; border: 2px solid #D4AF37; box-shadow: 0 10px 25px rgba(0,0,0,0.6);">
                <p style="color: #F3D06C !important; font-weight: bold; margin-top: 10px; font-size: 1.1rem;">Emily Gisto Araujo</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="content-box animated-block">
            <h3 style="color: #F3D06C !important; margin-top:0;">Uma Mensagem Especial para Si</h3>
            <p style="line-height: 1.7; color: #FFFFFF !important; font-size: 1.02rem;">
                Muitas vezes, passamos a vida a cuidar de tudo e de todos, esquecendo-nos da nossa própria essência. 
                Este encontro foi desenhado ao detalhe para a ajudar a pausar, refletir e dar o próximo passo na sua jornada com propósito e leveza.
            </p>
            <p style="color: #F3D06C !important; font-weight: 700; margin-top: 10px;">
                Garanta a sua presença preenchendo o formulário abaixo.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Formulário Interativo com Contraste Total em Todas as Opções
    with st.form("form_inscricao", clear_on_submit=True):
        st.markdown(
            "<h2 style='color: #F3D06C !important; text-align: center;'>🌸 Formulário de Inscrição</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(212,175,55,0.3);'>",
                    unsafe_allow_html=True)

        st.markdown("<p style='color: #F7E7CE; font-weight: 700; font-size: 1.05rem;'>1. Qual é o seu nome completo? <span style='font-weight: 400; font-size: 0.9rem; color: #E8C5C8;'>(Para confirmar a sua inscrição)</span></p>", unsafe_allow_html=True)
        nome = st.text_input(
            "Nome completo", label_visibility="collapsed", placeholder="O seu nome completo...")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F7E7CE; font-weight: 700; font-size: 1.05rem;'>Qual é o seu e-mail de contacto? <span style='font-weight: 400; font-size: 0.9rem; color: #E8C5C8;'>(Para conteúdos exclusivos)</span></p>", unsafe_allow_html=True)
        email = st.text_input(
            "E-mail", label_visibility="collapsed", placeholder="exemplo@email.com")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F7E7CE; font-weight: 700; font-size: 1.05rem;'>2. Qual é o seu contacto de WhatsApp? <span style='font-weight: 400; font-size: 0.9rem; color: #E8C5C8;'>(Para receber as informações do evento)</span></p>", unsafe_allow_html=True)
        whatsapp = st.text_input(
            "WhatsApp", label_visibility="collapsed", placeholder="+351 900 000 000")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F7E7CE; font-weight: 700; font-size: 1.05rem;'>3. O que a motivou a querer participar no Ela Desperta?</p>", unsafe_allow_html=True)
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

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F7E7CE; font-weight: 700; font-size: 1.05rem;'>4. Em que área da sua vida sente que precisa de despertar?</p>", unsafe_allow_html=True)
        area_despertar = st.radio(
            "Área a Despertar",
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

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: #F7E7CE; font-weight: 700; font-size: 1.05rem;'>5. Confirma a sua participação e compreende o valor de inscrição?</p>", unsafe_allow_html=True)
        confirmacao = st.radio(
            "Confirmação",
            [
                "Sim, confirmo a minha participação e aceito o valor de 17 €",
                "Ainda preciso de esclarecer algumas dúvidas"
            ],
            label_visibility="collapsed"
        )

        # Bloco de Pagamento em Destaque
        st.markdown("""
        <div class="glass-card" style="margin-top: 25px; border: 2px solid #D4AF37;">
            <h3 style="color: #F3D06C !important; margin-top:0;">💳 Confirmação da Inscrição</h3>
            <p style="font-size: 1.05rem; line-height: 1.6;">O valor de participação é de <b style="color: #F3D06C;">17 €</b>, destinado ao <i>coffee break</i> do hotel.</p>
            <p style="line-height: 1.6;">O pagamento deverá ser efetuado até ao dia <b>12 de novembro</b>, através de:</p>
            <ul style="line-height: 1.8;">
                <li>Dinheiro (em espécie); ou</li>
                <li>Por IBAN: <b style="color: #F3D06C; font-size: 1.1rem;">PT50581000019000006564779</b><br>(Titular: <i>Emily Gisto Araujo</i>)</li>
            </ul>
            <p style="font-size: 0.9rem; color: #F3D06C !important; margin-top: 12px;">* A inscrição ficará confirmada após a validação do pagamento.</p>
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "✨ Confirmar a minha Inscrição com Propósito")

        if submitted:
            if not nome or not whatsapp or not email:
                st.error(
                    "Por favor, preencha o seu Nome, E-mail e WhatsApp para validar a inscrição.")
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
                    "Agradecemos a sua inscrição e esperamos por si neste encontro especial! 🌸")

# ---------------------------------------------------------
# Painel da Gestora (Admin)
# ---------------------------------------------------------
elif menu == "Painel da Gestora (Admin)":
    st.markdown("<h2 style='color: #F3D06C !important;'>📊 Gestão de Participantes — Ela Desperta</h2>",
                unsafe_allow_html=True)

    senha = st.text_input("Palavra-passe de acesso restrito:", type="password")

    if senha == "crearis2026":
        st.success("Acesso autorizado com sucesso!")
        inscricoes = carregar_inscricoes()

        if len(inscricoes) == 0:
            st.info("Ainda não existem inscrições registadas.")
        else:
            df = pd.DataFrame(inscricoes)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Inscrições", len(df))
            confirmadas = len(
                df[df['status_confirmacao'].str.contains("Sim", na=False)])
            col2.metric("Confirmadas", confirmadas)
            col3.metric("Valor Arrecadado (Coffee)", f"{confirmadas * 17} €")

            st.divider()
            st.markdown("### 📋 Lista Completa de Participantes")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Descarregar Lista de Inscrições (CSV)",
                data=csv,
                file_name="participantes_ela_desperta.csv",
                mime="text/csv",
            )
    elif senha != "":
        st.error("Palavra-passe incorreta.")
