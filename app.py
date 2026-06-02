import streamlit as st
from auth import init_auth, get_current_user, logout   # ← mantengo tus imports por ahora
from ui_components import render_header, render_footer

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==================== LOGIN NATIVO ====================
if "user" not in st.session_state:
    st.login(provider="google")
    st.stop()

user = st.session_state.user
# =====================================================

render_header()

st.markdown(f'<p class="welcome-text">Bienvenido, <strong>{user.name if hasattr(user, "name") else user.email}</strong>! 👋</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["⚽ Mis Pronósticos", "🏆 Tabla de Posiciones", "📊 Resultados", "🌟 Bonus Final"])

with tab1:
    from pages.pronosticos import render_pronosticos
    render_pronosticos(user)

with tab2:
    from pages.tabla import render_tabla
    render_tabla()

with tab3:
    from pages.resultados import render_resultados
    render_resultados(user)

with tab4:
    from pages.bonus import render_bonus
    render_bonus(user)

render_footer()
