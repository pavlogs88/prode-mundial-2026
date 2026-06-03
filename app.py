import streamlit as st
from auth import get_supabase, get_current_user, process_supabase_session, logout
from ui_components import render_header, render_footer
import supabase
import pkg_resources

st.write(
    pkg_resources.get_distribution("supabase").version
)

import importlib.metadata

st.write(
    importlib.metadata.version("supabase")
)

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Handle token in query params (sent by callback.html) ──    
qp = st.query_params

st.write("Query Params:")
st.write(dict(st.query_params))

if "code" in st.query_params:
    st.success("CODE DETECTADO")
supabase = get_supabase()

try:
    session = supabase.auth.get_session()
    st.write("SESSION:")
    st.write(session)
except Exception as e:
    st.write("SESSION ERROR:")
    st.write(str(e))


user = get_current_user()
render_header()

qp = st.query_params

if "code" in qp:
    st.write("CODE:", qp["code"])

    try:
        supabase = get_supabase()
        st.write("URL:", st.secrets["SUPABASE_URL"])
        st.write("KEY LEN:", len(st.secrets["SUPABASE_ANON_KEY"]))
        result = supabase.auth.exchange_code_for_session(
            {
            "auth_code": qp["code"]
            }
        )

        st.write("RESULT:")
        st.write(result)

    except Exception as e:
        st.error(f"ERROR EXCHANGE: {e}")

if not user:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚽ MUNDIAL 2026</div>
        <h1 class="hero-title">PRODE<br><span class="hero-accent">MUNDIAL</span></h1>
        <p class="hero-subtitle">Predicí los resultados, acumulá puntos<br>y ganá el torneo entre amigos.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        supabase = get_supabase()
        REDIRECT_URI = st.secrets.get("REDIRECT_URI", "http://localhost:8501")
        response = supabase.auth.sign_in_with_oauth(
            {
                    "provider": "google",
                    "options": {
                            "redirect_to": st.secrets["REDIRECT_URI"],
                            "skip_browser_redirect": True,
                             }
            }
        )
        google_url = response.url if response else None
    except Exception as e:
        google_url = None
        st.error(f"Error: {e}")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Ingresá con tu cuenta Google")
        st.markdown("Compartí el link con tus amigos para que se unan al prode.")
        if google_url:
            st.link_button("🌐 Continuar con Google", url=google_url, use_container_width=True)
        else:
            st.warning("No se pudo generar el link de login.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    cols = st.columns(5)
    rules = [("3","resultado exacto"),("1","ganador/empate"),("1","goles de un equipo"),("0.5","diferencia de goles"),("10","bonus goleador/MVP")]
    for col, (pts, label) in zip(cols, rules):
        with col:
            st.markdown(f'<div class="rule-card"><div class="rule-pts">{pts}</div><div class="rule-label">pts por {label}</div></div>', unsafe_allow_html=True)

else:
    st.markdown(f'<p class="welcome-text">Bienvenido, <strong>{user["name"]}</strong>! 👋</p>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["⚽ Mis Pronósticos", "🏆 Tabla de Posiciones", "📊 Resultados", "🌟 Bonus Final"])
    with tab1:
        from pages_modules.pronosticos import render_pronosticos
        render_pronosticos(user)
    with tab2:
        from pages_modules.tabla import render_tabla
        render_tabla()
    with tab3:
        from pages_modules.resultados import render_resultados
        render_resultados(user)
    with tab4:
        from pages_modules.bonus import render_bonus
        render_bonus(user)

render_footer()
