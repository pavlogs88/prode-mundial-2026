import streamlit as st
from database import save_bonus, get_bonus_user, get_all_bonus, get_all_users

# List of top players for autocomplete suggestions
TOP_PLAYERS = [
    "Lionel Messi", "Kylian Mbappé", "Erling Haaland", "Vinicius Jr.",
    "Pedri", "Jude Bellingham", "Rodri", "Lamine Yamal", "Phil Foden",
    "Bukayo Saka", "Florian Wirtz", "Gavi", "Federico Valverde",
    "Rafael Leão", "Victor Osimhen", "Harry Kane", "Romelu Lukaku",
    "Neymar Jr.", "Bernardo Silva", "Trent Alexander-Arnold",
    "Ousmane Dembélé", "Antoine Griezmann", "Riyad Mahrez",
    "Son Heung-min", "Sadio Mané", "Richarlison", "Julian Alvarez",
    "Enzo Fernández", "Alexis Mac Allister", "Paulo Dybala",
]

BONUS_CLOSE_DATE = "2026-06-11T00:00:00"  # Closes when WC starts


def render_bonus(user):
    from datetime import datetime, timezone
    user_id = user["id"]

    st.markdown("## 🌟 Predicciones Bonus del Mundial")
    st.markdown("Estas predicciones valen **10 puntos cada una** si las acertás. Se cierran al inicio del Mundial.")

    # Check if still open
    close_dt = datetime.fromisoformat(BONUS_CLOSE_DATE).replace(tzinfo=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    bonus_open = now < close_dt

    with st.spinner("Cargando..."):
        current = get_bonus_user(user_id)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚽ Goleador del Mundial")
        st.markdown("¿Quién va a ser el máximo goleador?")

        if bonus_open:
            goleador = st.selectbox(
                "Seleccioná un jugador",
                options=[""] + sorted(TOP_PLAYERS),
                index=0 if not current.get("goleador") else
                      ([""] + sorted(TOP_PLAYERS)).index(current.get("goleador", ""))
                      if current.get("goleador") in TOP_PLAYERS else 0,
                key="bonus_goleador"
            )
            custom_g = st.text_input("O escribí otro nombre:", key="custom_goleador",
                                     placeholder="Nombre del jugador...")
            final_goleador = custom_g.strip() if custom_g.strip() else goleador
        else:
            final_goleador = current.get("goleador", "No ingresado")
            st.info(f"Tu predicción: **{final_goleador}**")

    with col2:
        st.markdown("### 🏅 Mejor Jugador (MVP)")
        st.markdown("¿Quién va a ganar el Balón de Oro del torneo?")

        if bonus_open:
            mejor = st.selectbox(
                "Seleccioná un jugador",
                options=[""] + sorted(TOP_PLAYERS),
                index=0 if not current.get("mejor_jugador") else
                      ([""] + sorted(TOP_PLAYERS)).index(current.get("mejor_jugador", ""))
                      if current.get("mejor_jugador") in TOP_PLAYERS else 0,
                key="bonus_mejor"
            )
            custom_m = st.text_input("O escribí otro nombre:", key="custom_mejor",
                                     placeholder="Nombre del jugador...")
            final_mejor = custom_m.strip() if custom_m.strip() else mejor
        else:
            final_mejor = current.get("mejor_jugador", "No ingresado")
            st.info(f"Tu predicción: **{final_mejor}**")

    st.markdown("---")

    if bonus_open:
        if st.button("💾 Guardar predicciones bonus", use_container_width=True, type="primary"):
            if not final_goleador or not final_mejor:
                st.warning("⚠️ Completá ambas predicciones antes de guardar.")
            else:
                save_bonus(user_id, final_goleador, final_mejor)
                st.success(f"✅ Guardado! Goleador: **{final_goleador}** | MVP: **{final_mejor}**")
                st.rerun()
    else:
        st.warning("🔒 Las predicciones bonus están cerradas (el Mundial ya empezó).")

    # Show all predictions (spoiler warning)
    st.markdown("---")
    with st.expander("👀 Ver predicciones de todos (spoiler)"):
        try:
            all_bonus = get_all_bonus()
            all_users = get_all_users()
            if not all_bonus.empty and not all_users.empty:
                user_map = {str(r["id"]): r["name"] for _, r in all_users.iterrows()}
                all_bonus["nombre"] = all_bonus["user_id"].apply(
                    lambda uid: user_map.get(str(uid), str(uid))
                )
                display = all_bonus[["nombre", "goleador", "mejor_jugador"]].copy()
                display.columns = ["Participante", "Goleador", "MVP"]
                st.dataframe(display, use_container_width=True, hide_index=True)
            else:
                st.info("Nadie cargó predicciones bonus todavía.")
        except Exception as e:
            st.error(f"Error: {e}")
