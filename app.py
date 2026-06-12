"""
╔══════════════════════════════════════════════════════════════╗
║         TERMINAL FINANCIERA — Dashboard Cuantitativo         ║
║         S&P 500 + MERVAL · Tiempo Real · Análisis Técnico    ║
╚══════════════════════════════════════════════════════════════╝

Autor: Tomas (Balanz / Canal Finanzas)
Stack: Streamlit + Plotly + yfinance
Despliegue: Streamlit Community Cloud (gratuito)
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Terminal Financiera",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fuente & fondo ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #0a0e1a;
        border-right: 1px solid #1e2d4a;
    }
    section[data-testid="stSidebar"] * {
        color: #c8d6f0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #7fa3d0 !important;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ── Fondo principal ── */
    .main .block-container {
        background: #06090f;
        padding-top: 1.5rem;
        max-width: 1400px;
    }
    .stApp {
        background: #06090f;
    }

    /* ── Métricas (tarjetas KPI) ── */
    [data-testid="metric-container"] {
        background: #0d1526;
        border: 1px solid #1a2d4a;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        transition: border-color 0.2s;
    }
    [data-testid="metric-container"]:hover {
        border-color: #2563eb;
    }
    [data-testid="metric-container"] label {
        color: #5a7fa8 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e8f0fe !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.25rem !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    /* ── Tablas ── */
    .stDataFrame {
        border: 1px solid #1a2d4a;
        border-radius: 8px;
        overflow: hidden;
    }

    /* ── Títulos de sección ── */
    .section-title {
        color: #4a9eff;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        border-bottom: 1px solid #1a2d4a;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }

    /* ── Chip de recomendación ── */
    .rec-chip {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 100px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .rec-buy   { background: #0f3d2a; color: #22c55e; border: 1.5px solid #22c55e; }
    .rec-hold  { background: #3d3000; color: #f59e0b; border: 1.5px solid #f59e0b; }
    .rec-sell  { background: #3d0f0f; color: #ef4444; border: 1.5px solid #ef4444; }

    /* ── Logo/header ── */
    .terminal-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.3rem;
    }
    .terminal-logo {
        font-size: 1.8rem;
    }
    .terminal-name {
        color: #e8f0fe;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .terminal-sub {
        color: #3a5a80;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        margin-top: -0.2rem;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1526;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #1a2d4a;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #5a7fa8 !important;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #1a3a6e !important;
        color: #e8f0fe !important;
    }

    /* ── Plotly charts fondo ── */
    .js-plotly-plot {
        border-radius: 10px;
        border: 1px solid #1a2d4a;
        overflow: hidden;
    }

    /* ── Botones ── */
    .stButton button {
        background: #1a3a6e;
        color: #e8f0fe;
        border: 1px solid #2563eb;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.82rem;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background: #2563eb;
        border-color: #3b82f6;
    }

    /* ── Divider ── */
    hr {
        border-color: #1a2d4a !important;
        margin: 1rem 0;
    }

    /* Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #06090f; }
    ::-webkit-scrollbar-thumb { background: #1a2d4a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2563eb; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# UNIVERSO DE ACTIVOS
# ─────────────────────────────────────────────────────────────
SP500_UNIVERSE = {
    "Tecnología": {
        "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA", "GOOGL": "Alphabet",
        "META": "Meta", "AMZN": "Amazon", "AMD": "AMD", "INTC": "Intel",
        "CRM": "Salesforce", "ORCL": "Oracle",
    },
    "Finanzas": {
        "JPM": "JPMorgan", "BAC": "Bank of America", "GS": "Goldman Sachs",
        "MS": "Morgan Stanley", "WFC": "Wells Fargo", "BRK-B": "Berkshire",
        "C": "Citigroup", "AXP": "American Express", "V": "Visa", "MA": "Mastercard",
    },
    "Energía": {
        "XOM": "ExxonMobil", "CVX": "Chevron", "COP": "ConocoPhillips",
        "EOG": "EOG Resources", "SLB": "SLB", "MPC": "Marathon Petroleum",
        "PSX": "Phillips 66", "VLO": "Valero", "OXY": "Occidental", "HAL": "Halliburton",
    },
    "Salud": {
        "JNJ": "Johnson & Johnson", "UNH": "UnitedHealth", "LLY": "Eli Lilly",
        "PFE": "Pfizer", "ABBV": "AbbVie", "MRK": "Merck", "TMO": "Thermo Fisher",
        "ABT": "Abbott", "BMY": "Bristol-Myers", "AMGN": "Amgen",
    },
    "Consumo Discrecional": {
        "TSLA": "Tesla", "HD": "Home Depot", "MCD": "McDonald's", "NKE": "Nike",
        "SBUX": "Starbucks", "TGT": "Target", "LOW": "Lowe's", "F": "Ford",
        "GM": "General Motors", "BKNG": "Booking Holdings",
    },
    "Consumo Básico": {
        "PG": "Procter & Gamble", "KO": "Coca-Cola", "PEP": "PepsiCo",
        "WMT": "Walmart", "COST": "Costco", "PM": "Philip Morris",
        "MO": "Altria", "CL": "Colgate", "GIS": "General Mills", "K": "Kellanova",
    },
    "ETFs / Índices": {
        "SPY": "S&P 500 ETF", "QQQ": "Nasdaq 100 ETF", "IWM": "Russell 2000 ETF",
        "GLD": "Gold ETF", "TLT": "Treasury Bonds ETF", "VIX": "Volatility Index",
        "EEM": "Emerging Markets ETF", "DIA": "Dow Jones ETF",
    },
}

MERVAL_UNIVERSE = {
    "Bancos": {
        "GGAL.BA": "Galicia", "BMA.BA": "Macro", "BBAR.BA": "BBVA Argentina",
        "SUPV.BA": "Supervielle", "BHIP.BA": "Hipotecario", "BPAT.BA": "Patagonia",
    },
    "Energía & Petróleo": {
        "YPF.BA": "YPF", "PAMP.BA": "Pampa Energía", "TGNO4.BA": "TGN",
        "TGSU2.BA": "TGS", "CGPA2.BA": "Capex", "VALO.BA": "Valo",
        "METR.BA": "MetroGAS", "GARO.BA": "Garovaglio",
    },
    "Real Estate & Construcción": {
        "IRSA.BA": "IRSA", "BYMA.BA": "BYMA", "CRES.BA": "Cresud",
        "INTR.BA": "Intratex", "DGCU2.BA": "Distribuidora Gas Cuyana",
    },
    "Consumo & Retail": {
        "ALUA.BA": "Aluar", "MIRG.BA": "Mirgor", "MOLI.BA": "Molinos Río",
        "AGRO.BA": "AgroIndustria", "HARG.BA": "Holcim",
    },
    "Telecomunicaciones": {
        "TECO2.BA": "Telecom", "CEPU.BA": "Central Puerto", "EDN.BA": "Edenor",
    },
    "Acero & Industria": {
        "ERAR.BA": "Ternium", "LOMA.BA": "Loma Negra",
    },
}

# ─────────────────────────────────────────────────────────────
# FUNCIONES DE DATOS
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_quote(ticker: str) -> dict:
    """Obtiene cotización y métricas básicas para un ticker. TTL=5min."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        hist = t.history(period="2d", interval="1d")
        if hist.empty or len(hist) < 1:
            return None

        last_close = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2] if len(hist) >= 2 else last_close
        change_pct = ((last_close - prev_close) / prev_close) * 100 if prev_close else 0
        volume = hist["Volume"].iloc[-1] if "Volume" in hist.columns else 0

        return {
            "ticker":       ticker,
            "name":         info.get("shortName", ticker),
            "price":        round(last_close, 2),
            "change_pct":   round(change_pct, 2),
            "volume":       int(volume),
            "mktcap":       info.get("marketCap"),
            "pe":           info.get("trailingPE"),
            "eps":          info.get("trailingEps"),
            "dividend":     info.get("dividendYield"),
            "beta":         info.get("beta"),
            "52wHigh":      info.get("fiftyTwoWeekHigh"),
            "52wLow":       info.get("fiftyTwoWeekLow"),
            "currency":     info.get("currency", "USD"),
        }
    except Exception:
        return None


@st.cache_data(ttl=300, show_spinner=False)
def fetch_ohlcv(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Descarga datos OHLCV históricos."""
    try:
        df = yf.download(ticker, period=period, interval=interval,
                         progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        # Aplanar MultiIndex si viene de una sola acción
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        df.dropna(subset=["Close"], inplace=True)
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600, show_spinner=False)
def fetch_sector_quotes(sector_tickers: dict) -> pd.DataFrame:
    """Descarga cotizaciones del día para todo un sector (batch)."""
    rows = []
    for ticker, name in sector_tickers.items():
        q = fetch_quote(ticker)
        if q:
            rows.append({
                "Ticker":    ticker,
                "Empresa":   name,
                "Precio":    q["price"],
                "Var. %":    q["change_pct"],
                "Volumen":   q["volume"],
                "Cap. Mdo":  q["mktcap"],
                "Moneda":    q["currency"],
            })
        else:
            rows.append({
                "Ticker": ticker, "Empresa": name,
                "Precio": None, "Var. %": None,
                "Volumen": None, "Cap. Mdo": None, "Moneda": "—",
            })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────
# INDICADORES TÉCNICOS
# ─────────────────────────────────────────────────────────────
def compute_technical_signals(df: pd.DataFrame) -> dict:
    """
    Calcula SMA20, SMA50, RSI14 y devuelve recomendación cuantitativa.
    Señal: COMPRA / MANTENER / VENDER
    """
    if df.empty or len(df) < 51:
        return {"signal": "DATOS INSUFICIENTES", "color": "hold",
                "sma20": None, "sma50": None, "rsi": None, "reason": "Historial < 51 sesiones."}

    close = df["Close"].squeeze()

    # SMA
    sma20 = close.rolling(20).mean().iloc[-1]
    sma50 = close.rolling(50).mean().iloc[-1]
    price = close.iloc[-1]

    # RSI 14
    delta   = close.diff()
    gain    = delta.clip(lower=0).rolling(14).mean()
    loss    = (-delta.clip(upper=0)).rolling(14).mean()
    rs      = gain / loss.replace(0, np.nan)
    rsi_series = 100 - (100 / (1 + rs))
    rsi = rsi_series.iloc[-1]

    # Lógica de señal
    cross_bullish = sma20 > sma50
    rsi_oversold  = rsi < 35
    rsi_overbought= rsi > 70
    price_above_sma20 = price > sma20

    if cross_bullish and price_above_sma20 and not rsi_overbought:
        signal, color = "COMPRA", "buy"
        reason = (f"SMA20 ({sma20:.2f}) > SMA50 ({sma50:.2f}) → cruce alcista. "
                  f"RSI {rsi:.1f} en zona neutral. Precio sobre media de 20 días.")
    elif rsi_overbought:
        signal, color = "VENDER", "sell"
        reason = (f"RSI {rsi:.1f} en zona de sobrecompra (>70). "
                  f"Posible corrección técnica a la vista.")
    elif rsi_oversold:
        signal, color = "COMPRA", "buy"
        reason = (f"RSI {rsi:.1f} en zona de sobreventa (<35). "
                  f"Señal de reversión potencial al alza.")
    elif not cross_bullish and not price_above_sma20:
        signal, color = "VENDER", "sell"
        reason = (f"SMA20 ({sma20:.2f}) < SMA50 ({sma50:.2f}) → cruce bajista. "
                  f"Precio bajo ambas medias. Tendencia negativa.")
    else:
        signal, color = "MANTENER", "hold"
        reason = (f"Señales mixtas: SMA20={sma20:.2f} vs SMA50={sma50:.2f}. "
                  f"RSI {rsi:.1f} en zona neutral. Sin confirmación de tendencia.")

    return {
        "signal": signal, "color": color,
        "sma20": round(float(sma20), 2),
        "sma50": round(float(sma50), 2),
        "rsi":   round(float(rsi), 1),
        "reason": reason,
    }


# ─────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor="#06090f",
    plot_bgcolor="#06090f",
    font=dict(color="#8fadc8", family="Inter, sans-serif", size=11),
    xaxis=dict(
        gridcolor="#0d1a2e", zerolinecolor="#0d1a2e",
        showspikes=True, spikecolor="#2563eb", spikethickness=1,
    ),
    yaxis=dict(gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1a2d4a", borderwidth=1),
    margin=dict(l=10, r=10, t=40, b=10),
    hovermode="x unified",
)


def plot_candlestick(df: pd.DataFrame, ticker: str, sma20=None, sma50=None) -> go.Figure:
    """Gráfico de velas OHLC con SMA overlay."""
    fig = go.Figure()

    # Velas
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"],   close=df["Close"],
        increasing_line_color="#22c55e",
        decreasing_line_color="#ef4444",
        increasing_fillcolor="#22c55e",
        decreasing_fillcolor="#ef4444",
        name=ticker,
        hovertext=ticker,
    ))

    # SMAs
    if sma20 is not None:
        ma20 = df["Close"].rolling(20).mean()
        fig.add_trace(go.Scatter(
            x=df.index, y=ma20, name="SMA 20",
            line=dict(color="#f59e0b", width=1.5, dash="solid"),
        ))
    if sma50 is not None:
        ma50 = df["Close"].rolling(50).mean()
        fig.add_trace(go.Scatter(
            x=df.index, y=ma50, name="SMA 50",
            line=dict(color="#3b82f6", width=1.5, dash="dash"),
        ))

    # Volumen como barras en eje secundario
    colors = ["#22c55e" if c >= o else "#ef4444"
              for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], name="Volumen",
        marker_color=colors, opacity=0.35,
        yaxis="y2",
    ))

    fig.update_layout(
        **CHART_THEME,
        title=dict(text=f"<b>{ticker}</b> — Precio y Volumen",
                   font=dict(color="#e8f0fe", size=14)),
        yaxis2=dict(
            overlaying="y", side="right",
            showgrid=False, showticklabels=False,
            range=[0, df["Volume"].max() * 5],
        ),
        xaxis_rangeslider_visible=False,
        height=460,
    )
    return fig


def plot_comparison(tickers: list, period: str = "6mo") -> go.Figure:
    """Gráfico de rendimiento % comparativo (base 100)."""
    fig = go.Figure()
    COLORS = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a855f7",
              "#06b6d4","#f97316","#ec4899","#84cc16","#14b8a6"]

    for i, ticker in enumerate(tickers):
        df = fetch_ohlcv(ticker, period=period)
        if df.empty:
            continue
        close = df["Close"].squeeze()
        ret = ((close / close.iloc[0]) - 1) * 100
        fig.add_trace(go.Scatter(
            x=df.index, y=ret,
            name=ticker,
            line=dict(color=COLORS[i % len(COLORS)], width=2),
            mode="lines",
            hovertemplate=f"<b>{ticker}</b><br>Rend: %{{y:.1f}}%<extra></extra>",
        ))

    fig.add_hline(y=0, line_color="#1a2d4a", line_width=1)
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="<b>Comparador de Rendimiento</b> (base 100)",
                   font=dict(color="#e8f0fe", size=14)),
        yaxis_title="Rendimiento %",
        height=460,
    )
    return fig


def plot_rsi(df: pd.DataFrame) -> go.Figure:
    """Panel RSI standalone."""
    close = df["Close"].squeeze()
    delta   = close.diff()
    gain    = delta.clip(lower=0).rolling(14).mean()
    loss    = (-delta.clip(upper=0)).rolling(14).mean()
    rs      = gain / loss.replace(0, np.nan)
    rsi     = 100 - (100 / (1 + rs))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=rsi, name="RSI 14",
        line=dict(color="#a855f7", width=1.8),
    ))
    fig.add_hrect(y0=70, y1=100, fillcolor="#ef4444", opacity=0.07, line_width=0)
    fig.add_hrect(y0=0,  y1=30,  fillcolor="#22c55e", opacity=0.07, line_width=0)
    fig.add_hline(y=70, line_color="#ef4444", line_width=1, line_dash="dash")
    fig.add_hline(y=30, line_color="#22c55e", line_width=1, line_dash="dash")
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="RSI (14)", font=dict(color="#e8f0fe", size=13)),
        yaxis=dict(range=[0, 100], gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
        height=180,
        margin=dict(l=10, r=10, t=35, b=10),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# HELPERS UI
# ─────────────────────────────────────────────────────────────
def fmt_large(n) -> str:
    """Formatea números grandes: B / M / K."""
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return "N/D"
    if n >= 1e12: return f"${n/1e12:.2f}T"
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.2f}M"
    if n >= 1e3:  return f"${n/1e3:.1f}K"
    return f"${n:.2f}"


def color_change(val) -> str:
    """Color para variación porcentual en tabla."""
    if pd.isna(val): return ""
    return "color: #22c55e" if val > 0 else ("color: #ef4444" if val < 0 else "color: #8fadc8")


def period_to_yf(period_label: str) -> tuple:
    """Convierte label de período a (period, interval) para yfinance."""
    mapping = {
        "1D": ("1d",  "5m"),
        "5D": ("5d",  "30m"),
        "1M": ("1mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y",  "1d"),
        "5Y": ("5y",  "1wk"),
    }
    return mapping.get(period_label, ("6mo", "1d"))


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="terminal-header">
        <span class="terminal-logo">📊</span>
        <div>
            <div class="terminal-name">FinTerminal</div>
            <div class="terminal-sub">v2.0 · Live Data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    market = st.radio(
        "MERCADO",
        ["🇺🇸 S&P 500", "🇦🇷 MERVAL"],
        horizontal=False,
    )

    universe = SP500_UNIVERSE if "S&P" in market else MERVAL_UNIVERSE
    sectors  = list(universe.keys())

    st.markdown("---")

    sector = st.selectbox("SECTOR / RUBRO", sectors)
    sector_tickers = universe[sector]

    ticker_list = list(sector_tickers.keys())
    ticker_names = {v: k for k, v in sector_tickers.items()}

    selected_name = st.selectbox(
        "ACTIVO",
        options=["— Seleccioná un activo —"] + list(sector_tickers.values()),
    )

    st.markdown("---")
    st.markdown("""
    <div style="color:#2a4060;font-size:0.68rem;line-height:1.6;">
    📡 Datos: Yahoo Finance<br>
    🔄 Caché: 5 minutos<br>
    ⏱ Zona: UTC-3 (Buenos Aires)<br><br>
    <span style="color:#1a3050;">FinTerminal · Tomas · Balanz</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TABS PRINCIPALES
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏛  Sector",
    "📈  Análisis Individual",
    "⚖️  Comparador",
    "🤖  Señal Cuantitativa",
])


# ═════════════════════════════════════════════════════════════
# TAB 1 — SECTOR / COTIZACIONES DEL DÍA
# ═════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f'<div class="section-title">Cotizaciones del día — {market} · {sector}</div>',
                unsafe_allow_html=True)

    col_info, col_btn = st.columns([5, 1])
    with col_info:
        st.caption(f"Mostrando {len(sector_tickers)} activos del sector **{sector}**. "
                   f"Datos diferidos ~15 min (mercado abierto).")
    with col_btn:
        if st.button("🔄 Actualizar"):
            st.cache_data.clear()
            st.rerun()

    with st.spinner("Cargando cotizaciones…"):
        df_sector = fetch_sector_quotes(sector_tickers)

    if df_sector.empty:
        st.error("⚠️ No se pudo obtener datos para este sector. Intentá en unos minutos.")
    else:
        # KPIs resumen
        valid = df_sector.dropna(subset=["Var. %"])
        if not valid.empty:
            gainers = (valid["Var. %"] > 0).sum()
            losers  = (valid["Var. %"] < 0).sum()
            avg_chg = valid["Var. %"].mean()

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total activos", len(df_sector))
            k2.metric("Subas", f"{gainers}", delta=f"{gainers} positivos")
            k3.metric("Bajas", f"{losers}", delta=f"-{losers} negativos")
            k4.metric("Variación promedio", f"{avg_chg:+.2f}%",
                      delta=f"{'↑' if avg_chg > 0 else '↓'}")

        st.markdown("---")

        # Tabla estilizada
        display_df = df_sector.copy()
        display_df["Cap. Mdo"] = display_df["Cap. Mdo"].apply(fmt_large)
        display_df["Volumen"]  = display_df["Volumen"].apply(
            lambda x: f"{int(x):,}" if pd.notna(x) and x else "N/D")
        display_df["Precio"]   = display_df.apply(
            lambda r: f"{r['Moneda']} {r['Precio']:,.2f}" if pd.notna(r["Precio"]) else "N/D",
            axis=1,
        )
        display_df["Var. %"] = display_df["Var. %"].apply(
            lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/D")

        st.dataframe(
            display_df[["Ticker", "Empresa", "Precio", "Var. %", "Volumen", "Cap. Mdo"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ticker":  st.column_config.TextColumn("Ticker", width=90),
                "Empresa": st.column_config.TextColumn("Empresa", width=180),
                "Precio":  st.column_config.TextColumn("Precio", width=130),
                "Var. %":  st.column_config.TextColumn("Var. %", width=100),
                "Volumen": st.column_config.TextColumn("Volumen", width=110),
                "Cap. Mdo":st.column_config.TextColumn("Cap. de Mercado", width=130),
            },
        )

        # Mini mapa de calor de variaciones
        st.markdown("---")
        st.markdown('<div class="section-title">Mapa de Variaciones del Sector</div>',
                    unsafe_allow_html=True)

        raw = fetch_sector_quotes(sector_tickers)
        raw_valid = raw.dropna(subset=["Var. %"])
        if not raw_valid.empty:
            fig_heat = go.Figure(go.Treemap(
                labels=raw_valid["Ticker"],
                parents=[""] * len(raw_valid),
                values=[max(abs(v), 0.01) for v in raw_valid["Var. %"]],
                customdata=raw_valid[["Empresa", "Var. %"]].values,
                hovertemplate="<b>%{label}</b><br>%{customdata[0]}<br>Var: %{customdata[1]:+.2f}%<extra></extra>",
                marker=dict(
                    colors=raw_valid["Var. %"],
                    colorscale=[
                        [0.0, "#7f1d1d"], [0.3, "#dc2626"],
                        [0.5, "#1a2d4a"],
                        [0.7, "#16a34a"], [1.0, "#14532d"],
                    ],
                    cmid=0,
                    showscale=True,
                    colorbar=dict(
                        title="Var. %", thickness=12,
                        tickfont=dict(color="#8fadc8"),
                        titlefont=dict(color="#8fadc8"),
                    ),
                ),
                texttemplate="<b>%{label}</b><br>%{customdata[1]:+.1f}%",
                textfont=dict(color="white", size=13),
            ))
            fig_heat.update_layout(
                **{k: v for k, v in CHART_THEME.items() if k != "hovermode"},
                height=320,
                title=dict(text="", font=dict(color="#e8f0fe")),
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig_heat, use_container_width=True)


# ═════════════════════════════════════════════════════════════
# TAB 2 — ANÁLISIS INDIVIDUAL
# ═════════════════════════════════════════════════════════════
with tab2:
    if selected_name == "— Seleccioná un activo —":
        st.info("👈 Seleccioná un activo desde el panel lateral para ver su análisis.")
    else:
        selected_ticker = sector_tickers[selected_name]
        st.markdown(f'<div class="section-title">{selected_ticker} — {selected_name} · Análisis Técnico</div>',
                    unsafe_allow_html=True)

        # Datos de cotización
        with st.spinner(f"Cargando {selected_ticker}…"):
            quote = fetch_quote(selected_ticker)

        if quote is None:
            st.error(f"⚠️ No se pudieron obtener datos para **{selected_ticker}**. "
                     f"El ticker puede estar caído o fuera de horario.")
        else:
            # ── KPIs header ──
            c1, c2, c3, c4, c5 = st.columns(5)
            currency = quote.get("currency", "")
            c1.metric("Precio",   f"{currency} {quote['price']:,.2f}")
            c2.metric("Var. Día", f"{quote['change_pct']:+.2f}%",
                      delta=f"{quote['change_pct']:+.2f}%")
            c3.metric("P/E Ratio", f"{quote['pe']:.1f}" if quote['pe'] else "N/D")
            c4.metric("EPS",      f"{quote['eps']:.2f}" if quote['eps'] else "N/D")
            c5.metric("Beta",     f"{quote['beta']:.2f}" if quote['beta'] else "N/D")

            c6, c7, c8, c9, c10 = st.columns(5)
            c6.metric("Cap. Mercado",   fmt_large(quote['mktcap']))
            c7.metric("Div. Yield",
                      f"{quote['dividend']*100:.2f}%" if quote['dividend'] else "N/D")
            c8.metric("Máx 52 sem",
                      f"{currency} {quote['52wHigh']:,.2f}" if quote['52wHigh'] else "N/D")
            c9.metric("Mín 52 sem",
                      f"{currency} {quote['52wLow']:,.2f}" if quote['52wLow'] else "N/D")
            vol_24h = quote.get("volume", 0)
            c10.metric("Volumen",       f"{vol_24h:,}" if vol_24h else "N/D")

            st.markdown("---")

            # ── Selector de período ──
            col_period, _ = st.columns([2, 5])
            with col_period:
                period_label = st.radio(
                    "PERÍODO", ["1D", "5D", "1M", "6M", "1Y", "5Y"],
                    horizontal=True, index=3,
                )

            yf_period, yf_interval = period_to_yf(period_label)

            with st.spinner("Cargando historial de precios…"):
                df_hist = fetch_ohlcv(selected_ticker, period=yf_period, interval=yf_interval)

            if df_hist.empty:
                st.error("No hay datos históricos disponibles para este período.")
            else:
                # Calcular señales para overlay
                signals = compute_technical_signals(df_hist) if period_label not in ["1D", "5D"] else {}

                # Gráfico principal
                show_sma = period_label not in ["1D", "5D"]
                fig_candle = plot_candlestick(
                    df_hist, selected_ticker,
                    sma20=signals.get("sma20") if show_sma else None,
                    sma50=signals.get("sma50") if show_sma else None,
                )
                st.plotly_chart(fig_candle, use_container_width=True)

                # RSI (solo para períodos > 5D)
                if period_label not in ["1D", "5D"] and len(df_hist) >= 15:
                    fig_rsi = plot_rsi(df_hist)
                    st.plotly_chart(fig_rsi, use_container_width=True)

                # Stats del período
                st.markdown("---")
                st.markdown('<div class="section-title">Estadísticas del Período</div>',
                            unsafe_allow_html=True)

                close = df_hist["Close"].squeeze()
                ret_periodo = ((close.iloc[-1] / close.iloc[0]) - 1) * 100
                volatilidad = close.pct_change().std() * np.sqrt(252) * 100
                max_drawdown = ((close / close.cummax()) - 1).min() * 100

                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Retorno del Período", f"{ret_periodo:+.2f}%",
                          delta=f"{ret_periodo:+.2f}%")
                s2.metric("Volatilidad Anual.",  f"{volatilidad:.1f}%")
                s3.metric("Máx. Drawdown",       f"{max_drawdown:.1f}%")
                s4.metric("Días analizados",      str(len(df_hist)))


# ═════════════════════════════════════════════════════════════
# TAB 3 — COMPARADOR
# ═════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Comparador de Activos — Rendimiento Relativo</div>',
                unsafe_allow_html=True)
    st.caption("Compará el rendimiento % de múltiples activos desde el mismo punto de partida. "
               "Podés mezclar S&P 500 y MERVAL.")

    # Pool de activos disponibles
    all_tickers: dict = {}
    for sec_dict in SP500_UNIVERSE.values():
        all_tickers.update(sec_dict)
    for sec_dict in MERVAL_UNIVERSE.values():
        all_tickers.update(sec_dict)

    # Display "Nombre (TICKER)"
    display_options = {f"{name} ({ticker})": ticker for ticker, name in all_tickers.items()}

    col_sel, col_per = st.columns([4, 1])
    with col_sel:
        selected_display = st.multiselect(
            "Seleccioná activos para comparar (máx. 10):",
            options=list(display_options.keys()),
            default=[
                k for k, v in display_options.items()
                if v in ("SPY", "GGAL.BA", "YPF.BA")
            ][:3],
            max_selections=10,
        )
    with col_per:
        comp_period = st.selectbox("Período", ["1M", "3M", "6M", "1Y", "5Y"],
                                   index=2, key="comp_period")

    # Mapear período a yfinance
    period_map = {"1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "5Y": "5y"}
    yf_comp_period = period_map[comp_period]

    selected_tickers_comp = [display_options[d] for d in selected_display]

    if not selected_tickers_comp:
        st.info("Seleccioná al menos un activo para comparar.")
    else:
        with st.spinner("Descargando datos para comparación…"):
            fig_comp = plot_comparison(selected_tickers_comp, period=yf_comp_period)
        st.plotly_chart(fig_comp, use_container_width=True)

        # Tabla de métricas comparativas
        st.markdown("---")
        st.markdown('<div class="section-title">Tabla Comparativa de Métricas</div>',
                    unsafe_allow_html=True)

        comp_rows = []
        for ticker in selected_tickers_comp:
            df_c = fetch_ohlcv(ticker, period=yf_comp_period)
            if df_c.empty:
                comp_rows.append({"Ticker": ticker, "Retorno %": None,
                                  "Volatilidad % (anual.)": None, "Máx. Drawdown %": None})
                continue
            close = df_c["Close"].squeeze()
            ret   = ((close.iloc[-1] / close.iloc[0]) - 1) * 100
            vol   = close.pct_change().std() * np.sqrt(252) * 100
            dd    = ((close / close.cummax()) - 1).min() * 100
            sharpe = (ret / vol) if vol > 0 else 0
            comp_rows.append({
                "Ticker":              ticker,
                "Nombre":              all_tickers.get(ticker, ticker),
                "Retorno %":           round(ret, 2),
                "Volatilidad % (anual.)": round(vol, 2),
                "Máx. Drawdown %":     round(dd, 2),
                "Sharpe aprox.":       round(sharpe, 2),
            })

        df_comp_table = pd.DataFrame(comp_rows)
        st.dataframe(
            df_comp_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Retorno %":            st.column_config.NumberColumn(format="%.2f%%"),
                "Volatilidad % (anual.)": st.column_config.NumberColumn(format="%.2f%%"),
                "Máx. Drawdown %":      st.column_config.NumberColumn(format="%.2f%%"),
                "Sharpe aprox.":        st.column_config.NumberColumn(format="%.2f"),
            },
        )


# ═════════════════════════════════════════════════════════════
# TAB 4 — SEÑAL CUANTITATIVA
# ═════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Sistema de Recomendación Cuantitativa</div>',
                unsafe_allow_html=True)

    if selected_name == "— Seleccioná un activo —":
        st.info("👈 Seleccioná un activo desde el panel lateral para ver su señal.")
    else:
        selected_ticker_q = sector_tickers[selected_name]
        st.caption(f"Analizando: **{selected_ticker_q}** — {selected_name}")

        with st.spinner("Calculando indicadores técnicos…"):
            df_signal = fetch_ohlcv(selected_ticker_q, period="1y")
            signals   = compute_technical_signals(df_signal)

        # ── Chip de señal ──
        chip_class = {"buy": "rec-buy", "hold": "rec-hold", "sell": "rec-sell"}
        chip_emoji = {"buy": "🟢", "hold": "🟡", "sell": "🔴"}
        label_map  = {"buy": "COMPRA", "hold": "MANTENER", "sell": "VENDER"}

        color_key = signals["color"] if signals["color"] in chip_class else "hold"
        signal_label = label_map.get(color_key, signals["signal"])

        col_chip, col_reason = st.columns([1, 2])
        with col_chip:
            st.markdown(
                f'<div style="text-align:center;padding:1.5rem 0;">'
                f'<div class="rec-chip {chip_class[color_key]}">'
                f'{chip_emoji[color_key]} {signal_label}</div>'
                f'<div style="color:#5a7fa8;font-size:0.75rem;margin-top:0.5rem;">'
                f'Basado en SMA20/50 + RSI14</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col_reason:
            st.markdown("**📋 Justificación algorítmica:**")
            st.info(signals["reason"])

        # ── Indicadores numéricos ──
        st.markdown("---")
        st.markdown('<div class="section-title">Valores de Indicadores</div>',
                    unsafe_allow_html=True)

        i1, i2, i3 = st.columns(3)
        i1.metric("SMA 20 días",
                  f"{signals['sma20']:.2f}" if signals['sma20'] else "N/D",
                  help="Media móvil simple de 20 sesiones. Tendencia de corto plazo.")
        i2.metric("SMA 50 días",
                  f"{signals['sma50']:.2f}" if signals['sma50'] else "N/D",
                  help="Media móvil simple de 50 sesiones. Tendencia de mediano plazo.")
        i3.metric("RSI 14 días",
                  f"{signals['rsi']:.1f}" if signals['rsi'] else "N/D",
                  help="Índice de Fuerza Relativa. <30 sobreventa, >70 sobrecompra.")

        # ── Gráfico con señales ──
        st.markdown("---")
        st.markdown('<div class="section-title">Gráfico con Señales Técnicas (1 año)</div>',
                    unsafe_allow_html=True)

        if not df_signal.empty:
            fig_sig = plot_candlestick(
                df_signal, selected_ticker_q,
                sma20=signals.get("sma20"),
                sma50=signals.get("sma50"),
            )
            st.plotly_chart(fig_sig, use_container_width=True)

            # RSI panel
            if len(df_signal) >= 15:
                st.plotly_chart(plot_rsi(df_signal), use_container_width=True)

        # ── Disclaimer ──
        st.markdown("---")
        st.warning(
            "⚠️ **Disclaimer:** Esta señal es generada por un algoritmo cuantitativo básico "
            "para fines educativos e informativos. No constituye asesoramiento de inversión. "
            "Las decisiones de inversión son exclusiva responsabilidad del usuario. "
            "Consultá siempre con un asesor financiero certificado antes de operar."
        )
