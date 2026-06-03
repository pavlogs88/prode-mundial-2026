import streamlit as st
import streamlit.components.v1 as components
from auth import get_supabase, get_current_user, process_supabase_session, logout
from ui_components import render_header, render_footer

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Handle token from URL hash via iframe component ──
qp = st.query_params
if "access_token" not in qp:
    token_html = """
    <script>
        const hash = window.top.location.hash || window.location.hash;
        if (hash && hash.includes('access_token')) {
            const params = new URLSearchParams(hash.substring(1));
            const at = params.get('access_token');
            const rt = params.get('refresh_token') || '';
            if (at) {
                const base = window.top.location.href.split('#')[0].split('?')[0];
                window.top.location.href = base + '?access_token=' + encodeURIComponent(at) + '&refresh_token=' + encodeURIComponent(rt);
            }
        }
    </script>
    """
    components.html(token_html, height=0)

# ── Process token ──
if "access_token" in qp and not st.session_state.get("user"):
    process_supabase_session(qp["access_token"], qp.get("refresh_token", ""))
    st.query_params.clear()
    st.rerun()

user = get_current_user()
render_header()

if not user:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚽ MUNDIAL 2026</div>
        <h1 class="hero-title">PRODE<br><span class="hero-accent">MUNDIAL</span></h1>
        <p class="hero-subtitle">Predicí los resultados, acumulá puntos<br>y ganá el torneo entre amigos.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Ingresá con tu cuenta Google")
        st.markdown("Compartí el link con tus amigos para que se unan al prode.")

        if st.button("🌐 Continuar con Google", type="primary", use_container_width=True):
            supabase = get_supabase()
            REDIRECT_URI = st.secrets.get("REDIRECT_URI", "http://localhost:8501")
            response = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {"redirect_to": REDIRECT_URI}
            })
            if response and response.url:
                # Use components.html to do a top-level redirect (bypasses iframe)
                components.html(f"""
                <script>
                    window.top.location.href = "{response.url}";
                </script>
                """, height=0)

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
