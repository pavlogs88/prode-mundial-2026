import streamlit as st
from auth import logout


def render_header():
    user = st.session_state.get("user")
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:1rem 0'>
            <div style='font-size:3rem'>⚽</div>
            <h2 style='margin:0;font-family:serif'>Prode Mundial</h2>
            <p style='color:#888;font-size:0.85rem'>FIFA World Cup 2026</p>
        </div>
        """, unsafe_allow_html=True)

        if user:
            st.markdown("---")
            if user.get("picture"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(user["picture"], width=40)
                with col2:
                    st.markdown(f"**{user['name']}**")
                    st.caption(user["email"])
            else:
                st.markdown(f"👤 **{user['name']}**")

            st.markdown("---")
            st.markdown("""
            **📋 Sistema de puntos:**
            - 🎯 Resultado exacto: **3 pts**
            - ✅ Ganador/empate: **1 pt**
            - ⚽ Goles de un equipo: **1 pt**
            - 📐 Diferencia de goles: **0.5 pts**
            - 🌟 Bonus goleador: **10 pts**
            - 🏅 Bonus MVP: **10 pts**
            """)
            st.markdown("---")
            if st.button("🚪 Cerrar sesión", use_container_width=True):
                logout()


def render_footer():
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#888;font-size:0.8rem'>Prode Mundial 2026 · Hecho con ❤️ para jugar entre amigos</p>",
        unsafe_allow_html=True
    )
