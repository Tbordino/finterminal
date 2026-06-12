# 📊 FinTerminal — Terminal Financiera

Dashboard financiero interactivo para S&P 500 y MERVAL, construido con Streamlit + Plotly + yfinance.

## Funcionalidades

- 🏛 **Cotizaciones por sector** con mapa de calor
- 📈 **Análisis individual** con gráfico de velas + RSI
- ⚖️ **Comparador de activos** (S&P 500 y MERVAL mezclados)
- 🤖 **Señal cuantitativa** SMA20/50 + RSI14 (Compra / Mantener / Vender)

## Stack

- **Frontend/Backend:** Python + Streamlit
- **Gráficos:** Plotly
- **Datos:** yfinance (Yahoo Finance)

---

## 🚀 Despliegue en Streamlit Community Cloud (GRATIS)

### Paso 1 — Clonar y preparar el repositorio

```bash
# Si aún no tenés git configurado:
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Inicializá el repositorio local
cd financial_terminal
git init
git add .
git commit -m "feat: initial commit — FinTerminal"
```

### Paso 2 — Subir a GitHub

1. Andá a [github.com](https://github.com) → **New repository**
2. Nombre sugerido: `finterminal`
3. Visibilidad: **Public** (requerido para Streamlit Community Cloud gratuito)
4. **No** marques "Initialize with README" (ya tenés uno)
5. Copiá la URL del repo (ej. `https://github.com/tu-usuario/finterminal.git`)

```bash
# Conectá tu repo local con GitHub
git remote add origin https://github.com/TU_USUARIO/finterminal.git
git branch -M main
git push -u origin main
```

### Paso 3 — Desplegar en Streamlit Community Cloud

1. Andá a **[share.streamlit.io](https://share.streamlit.io)**
2. Iniciá sesión con tu cuenta de GitHub
3. Hacé clic en **"New app"**
4. Completá el formulario:
   - **Repository:** `tu-usuario/finterminal`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Hacé clic en **"Deploy!"**
6. En ~2 minutos vas a tener tu URL pública HTTPS:
   `https://tu-usuario-finterminal.streamlit.app`

> ✅ **Gratuito**, **HTTPS automático**, **accesible desde cualquier dispositivo**.

---

## 🔄 Actualizaciones futuras

Cualquier `git push` al branch `main` redesplegará la app automáticamente.

```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push
```

---

## 🏃 Ejecución local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Correr la app
streamlit run app.py
```

La app quedará disponible en `http://localhost:8501`.

---

## 📁 Estructura del proyecto

```
financial_terminal/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias Python
├── .gitignore
├── README.md
└── .streamlit/
    └── config.toml     # Tema oscuro + configuración de servidor
```

---

## ⚠️ Disclaimer

Los datos son provistos por Yahoo Finance con diferimiento estándar de mercado (~15 min durante horario de apertura). Las señales de compra/venta son algorítmicas y educativas; no constituyen asesoramiento de inversión.
