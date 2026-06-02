# ⚽ Prode Mundial 2026

App web para hacer el prode del Mundial 2026 con amigos. Login con Google, pronósticos por partido, tabla de posiciones en tiempo real.

## 🏆 Sistema de puntos

| Acierto | Puntos |
|---------|--------|
| Resultado exacto (ej: 2-1) | **3 pts** |
| Ganador o empate | **1 pt** |
| Goles de un equipo exactos | **1 pt** (hasta 2 pts) |
| Diferencia de goles exacta | **0.5 pts** |
| Goleador del mundial (bonus) | **10 pts** |
| Mejor jugador MVP (bonus) | **10 pts** |

---

## 🚀 Cómo deployar en Streamlit Cloud (gratis)

### 1. Prerequisitos
- Cuenta en [Streamlit Cloud](https://streamlit.io/cloud)
- Cuenta en [Google Cloud Console](https://console.cloud.google.com)
- Repositorio en GitHub

### 2. Subir el código a GitHub

```bash
git init
git add .
git commit -m "Prode Mundial 2026"
git remote add origin https://github.com/TU-USUARIO/prode-mundial.git
git push -u origin main
```

> ⚠️ Asegurate de tener `.streamlit/secrets.toml` en el `.gitignore`

---

### 3. Crear Google OAuth (para login)

1. Ir a [console.cloud.google.com](https://console.cloud.google.com)
2. Crear nuevo proyecto (o usar uno existente)
3. APIs & Services → OAuth consent screen
   - User type: **External**
   - Completar nombre de la app, email de soporte
   - Scopes: agregar `email`, `profile`, `openid`
4. APIs & Services → Credentials → **Create Credentials → OAuth Client ID**
   - Application type: **Web application**
   - Authorized redirect URIs: `https://TU-APP.streamlit.app` (y `http://localhost:8501` para dev)
5. Copiar **Client ID** y **Client Secret**

---

### 4. Crear Google Sheet como base de datos

1. Crear una nueva [Google Sheet](https://sheets.new)
2. Copiar el ID de la URL: `docs.google.com/spreadsheets/d/**ESTE-ID**/edit`
3. Crear una cuenta de servicio:
   - Google Cloud → IAM & Admin → Service Accounts → Create
   - Crear y descargar clave JSON
4. **Compartir** la Google Sheet con el email de la cuenta de servicio (como Editor)

---

### 5. Configurar secrets en Streamlit Cloud

En tu app de Streamlit Cloud → Settings → Secrets, pegá:

```toml
GOOGLE_CLIENT_ID = "xxxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-xxxxxxx"
REDIRECT_URI = "https://TU-APP.streamlit.app"
SHEET_ID = "1xxxxxxxxxxxxxxxxxxx"

GCP_SERVICE_ACCOUNT = """
{ ... pegá el JSON de la cuenta de servicio completo ... }
"""
```

---

### 6. Deploy en Streamlit Cloud

1. [share.streamlit.io](https://share.streamlit.io) → New app
2. Conectar tu repositorio de GitHub
3. Main file path: `app.py`
4. Click **Deploy**

¡Listo! Compartí el link con tus amigos.

---

## 📁 Estructura del proyecto

```
prode_mundial/
├── app.py              # App principal
├── auth.py             # Login con Google OAuth
├── database.py         # Google Sheets como DB
├── matches.py          # Todos los partidos del Mundial 2026
├── scoring.py          # Lógica de puntos
├── ui_components.py    # Header, sidebar, footer
├── style.css           # Estilos personalizados
├── requirements.txt    # Dependencias Python
├── .gitignore
└── pages/
    ├── pronosticos.py  # Cargar pronósticos
    ├── tabla.py        # Tabla de posiciones
    ├── resultados.py   # Cargar resultados reales
    └── bonus.py        # Predicciones bonus (goleador/MVP)
```

---

## 🛠️ Desarrollo local

```bash
pip install -r requirements.txt
# Crear .streamlit/secrets.toml con tus credenciales
streamlit run app.py
```

---

## ❓ FAQ

**¿Hasta cuándo se pueden cargar pronósticos?**
Hasta el momento exacto en que empieza cada partido (cierre automático).

**¿Quién puede cargar los resultados reales?**
Cualquier participante puede cargarlos desde la pestaña "Resultados".

**¿Cuándo se suman los puntos bonus?**
Al final del mundial, cuando se conozcan el goleador y el MVP.
