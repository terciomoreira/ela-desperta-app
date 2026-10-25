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

# Função para converter qualquer imagem local em Base64 (Código)


def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    # Tenta procurar sem extensão duplicada se o ficheiro estiver renomeado
    alt_path = path + ".jpeg"
    if os.path.exists(alt_path):
        with open(alt_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    return None


img_bg_b64 = get_image_base64("assets/background.jpeg")
img_amor_b64 = get_image_base64("assets/amor.jpeg")

# ---------------------------------------------------------
# Estilização CSS e JavaScript para Animações e Leitura
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Fundo imersivo com gradiente vivo */
    .stApp {
        background: linear-gradient(135deg, #2A0815 0%, #4A1227 50%, #1F0510 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Correção total de contraste nos formulários */
    .stMarkdown, label, p, span, div {
        color: #FFFFFF !important;
    }

    .stRadio label, .stWidgetLabel, .stWidgetLabel p {
        color: #FFF8FA !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }

    /* Animações e Efeitos */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes goldPulse {
        0% { box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }
        50% { box-shadow: 0 0 35px rgba(212, 175, 55, 0.7); }
        100% { box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }
    }

    /* Cartões de Conteúdo */
    .hero-box {
        background: rgba(35, 8, 18, 0.85);
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        animation: fadeInUp 1s ease-out, goldPulse 4s infinite;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }

    .custom-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .custom-card:hover {
        transform: translateY(-4px);
        border-color: #D4AF37;
    }

    /* Textos Dourados */
    .gold-header {
        font-family: 'Playfair Display', serif !important;
        color: #F3D06C !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
        margin: 10px 0;
    }

    .gold-subtitle {
        color: #D4AF37 !important;
        letter-spacing: 2px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.9rem;
    }

    /* Estilo dos campos de texto */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #2A0815 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: 2px solid #D4AF37 !important;
        padding: 12px !important;
    }

    /* Botão Principal */
    .stButton>button {
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
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Navegação
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Navegação", ["Convite & Inscrição", "Painel da Gestora (Admin)"])

if menu == "Convite & Inscrição":

    # 1. Exibição Garantida do Banner "Ela Desperta" (Via Código Base64)
    if img_bg_b64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;" class="custom-card">
            <img src="{img_bg_b64}" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(
            "A imagem 'background.jpeg' não foi encontrada na pasta 'assets'. Verifique se o ficheiro existe.")

    # 2. Hero Box de Apresentação com Animação
    st.markdown("""
    <div class="hero-box">
        <p class="gold-subtitle">✦ ENCONTRO EXCLUSIVO DE TRANSFORMAÇÃO ✦</p>
        <h1 class="gold-header">ELA DESPERTA</h1>
        <p style="font-size: 1.1rem; color: #FAF6F8 !important; margin-top: 10px;">
            Um espaço seguro para resgatar a sua identidade, fortalecer a sua autoestima e despertar a mulher extraordinária que há em si.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3. Apresentação da Palestrante (Foto da Esposa via Código Base64)
    col1, col2 = st.columns([1, 2], gap="medium")
    with col1:
        if img_amor_b64:
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="{img_amor_b64}" style="width: 100%; border-radius: 16px; border: 2px solid #D4AF37; box-shadow: 0 8px 20px rgba(0,0,0,0.6);">
                <p style="color: #D4AF37 !important; font-weight: bold; margin-top: 8px;">Emily Gisto Araujo</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Coloque a foto 'amor.jpeg' na pasta 'assets'.")

    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #F3D06C !important; margin-top:0;">Uma Mensagem Especial para Si</h3>
            <p style="line-height: 1.6; color: #FFFFFF !important;">
                Muitas vezes, passamos a vida a cuidar de tudo e de todos, esquecendo-nos da nossa própria essência. 
                Este encontro foi desenhado ao detalhe para a ajudar a pausar, refletir e dar o próximo passo na sua jornada com propósito e leveza.
            </p>
            <p style="color: #D4AF37 !important; font-weight: 600;">
                Garanta a sua presença preenchendo o formulário abaixo.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Formulário com Contraste Total e Visibilidade Perfeita
    with st.form("form_inscricao", clear_on_submit=True):
        st.markdown(
            "<h2 style='color: #F3D06C !important; text-align: center;'>🌸 Formulário de Inscrição</h2>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown(
            "##### **1. Qual é o seu nome completo?** *(Para confirmar a sua inscrição)*")
        nome = st.text_input("Nome completo", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "##### **Qual é o seu e-mail de contacto?** *(Para conteúdos exclusivos)*")
        email = st.text_input("E-mail", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "##### **2. Qual é o seu contacto de WhatsApp?** *(Para receber as informações do evento)*")
        whatsapp = st.text_input("WhatsApp", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "##### **3. O que a motivou a querer participar no Ela Desperta?**")
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
        st.markdown(
            "##### **4. Em que área da sua vida sente que precisa de despertar?**")
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
        st.markdown(
            "##### **5. Confirms a sua participação e compreende o valor de inscrição?**")
        confirmacao = st.radio(
            "Confirmação",
            [
                "Sim, confirmo a minha participação e aceito o valor de 17 €",
                "Ainda preciso de esclarecer algumas dúvidas"
            ],
            label_visibility="collapsed"
        )

        # Bloco de Pagamento em Destaque Alto
        st.markdown("""
        <div class="custom-card" style="border: 2px solid #D4AF37; background: rgba(42, 8, 21, 0.95); margin-top: 20px;">
            <h3 style="color: #F3D06C !important; margin-top:0;">💳 Confirmação da Inscrição</h3>
            <p style="font-size: 1.05rem;">O valor de participação é de <b style="color: #F3D06C;">17 €</b>, destinado ao <i>coffee break</i> do hotel.</p>
            <p>O pagamento deverá ser efetuado até ao dia <b>12 de novembro</b>, através de:</p>
            <ul style="line-height: 1.8;">
                <li>Dinheiro (em espécie); ou</li>
                <li>Por IBAN: <b style="color: #F3D06C; font-size: 1.1rem;">PT50581000019000006564779</b><br>(Titular: <i>Emily Gisto Araujo</i>)</li>
            </ul>
            <p style="font-size: 0.9rem; color: #D4AF37 !important; margin-top: 10px;">* A inscrição ficará confirmada após o pagamento.</p>
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
