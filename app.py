import streamlit as st
from auth import get_current_user, logout
from ui_components import render_header, render_footer

st.set_page_config(page_title="Prode Mundial 2026 🏆", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==================== LOGIN NATIVO ====================
if "user" not in st.session_state:
    st.login(provider="google")
    st.stop()

user = get_current_user()
# ====================================================

render_header()

st.markdown(f"**Bienvenido, {user.get('name', user.get('email', 'Usuario'))}** 👋")

tab1, tab2, tab3, tab4 = st.tabs(["⚽ Mis Pronósticos", "🏆 Tabla", "📊 Resultados", "🌟 Bonus"])

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

logout()
render_footer()
