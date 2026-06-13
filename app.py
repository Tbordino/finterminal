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

    /* ── Ratios (texto reducido) ── */
    .ratio-block [data-testid="metric-container"] {
        padding: 0.6rem 0.8rem !important;
    }
    .ratio-block [data-testid="metric-container"] label {
        font-size: 0.62rem !important;
    }
    .ratio-block [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 0.95rem !important;
    }

    /* ── Section card ── */
    .ratio-card {
        background: #0a111f;
        border: 1px solid #1a2d4a;
        border-radius: 10px;
        padding: 0.8rem 1rem 0.6rem 1rem;
        margin-bottom: 0.8rem;
    }
    .ratio-card-title {
        color: #4a9eff;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.6rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #1a2d4a;
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
        "META": "Meta Platforms", "AMZN": "Amazon", "AMD": "AMD", "INTC": "Intel",
        "CRM": "Salesforce", "ORCL": "Oracle", "ADBE": "Adobe", "CSCO": "Cisco",
        "QCOM": "Qualcomm", "TXN": "Texas Instruments", "AVGO": "Broadcom",
        "NOW": "ServiceNow", "SNOW": "Snowflake", "PLTR": "Palantir",
        "MU": "Micron", "AMAT": "Applied Materials", "LRCX": "Lam Research",
        "KLAC": "KLA Corp", "MRVL": "Marvell", "FTNT": "Fortinet",
        "PANW": "Palo Alto Networks", "CRWD": "CrowdStrike", "ZS": "Zscaler",
        "DDOG": "Datadog", "NET": "Cloudflare", "TEAM": "Atlassian",
        "SHOP": "Shopify", "WDAY": "Workday", "INTU": "Intuit",
        "ADSK": "Autodesk", "ANSS": "Ansys", "CDNS": "Cadence",
        "SNPS": "Synopsys", "HPQ": "HP Inc", "DELL": "Dell Technologies",
    },
    "Finanzas": {
        "JPM": "JPMorgan Chase", "BAC": "Bank of America", "GS": "Goldman Sachs",
        "MS": "Morgan Stanley", "WFC": "Wells Fargo", "BRK-B": "Berkshire Hathaway",
        "C": "Citigroup", "AXP": "American Express", "V": "Visa", "MA": "Mastercard",
        "BLK": "BlackRock", "SCHW": "Charles Schwab", "COF": "Capital One",
        "USB": "U.S. Bancorp", "PNC": "PNC Financial", "TFC": "Truist Financial",
        "CB": "Chubb", "MMC": "Marsh McLennan", "AON": "Aon",
        "ICE": "Intercontinental Exchange", "CME": "CME Group", "SPGI": "S&P Global",
        "MCO": "Moody's", "MSCI": "MSCI Inc", "FIS": "Fidelity National",
        "FISV": "Fiserv", "PYPL": "PayPal", "SQ": "Block Inc",
        "HOOD": "Robinhood", "NU": "Nu Holdings", "MELI": "MercadoLibre",
    },
    "Energía": {
        "XOM": "ExxonMobil", "CVX": "Chevron", "COP": "ConocoPhillips",
        "EOG": "EOG Resources", "SLB": "SLB", "MPC": "Marathon Petroleum",
        "PSX": "Phillips 66", "VLO": "Valero Energy", "OXY": "Occidental Petroleum",
        "HAL": "Halliburton", "DVN": "Devon Energy", "FANG": "Diamondback Energy",
        "HES": "Hess Corp", "BKR": "Baker Hughes", "CTRA": "Coterra Energy",
        "APA": "APA Corp", "MRO": "Marathon Oil", "NOV": "NOV Inc",
        "NEE": "NextEra Energy", "DUK": "Duke Energy", "SO": "Southern Company",
        "D": "Dominion Energy", "AEP": "American Electric Power",
    },
    "Salud": {
        "JNJ": "Johnson & Johnson", "UNH": "UnitedHealth", "LLY": "Eli Lilly",
        "PFE": "Pfizer", "ABBV": "AbbVie", "MRK": "Merck", "TMO": "Thermo Fisher",
        "ABT": "Abbott Labs", "BMY": "Bristol-Myers Squibb", "AMGN": "Amgen",
        "GILD": "Gilead Sciences", "ISRG": "Intuitive Surgical", "SYK": "Stryker",
        "MDT": "Medtronic", "BSX": "Boston Scientific", "ZBH": "Zimmer Biomet",
        "REGN": "Regeneron", "VRTX": "Vertex Pharma", "BIIB": "Biogen",
        "MRNA": "Moderna", "BNTX": "BioNTech", "CVS": "CVS Health",
        "CI": "Cigna", "HUM": "Humana", "CNC": "Centene", "MOH": "Molina Healthcare",
        "IQV": "IQVIA", "A": "Agilent", "DHR": "Danaher", "BAX": "Baxter",
    },
    "Consumo Discrecional": {
        "TSLA": "Tesla", "HD": "Home Depot", "MCD": "McDonald's", "NKE": "Nike",
        "SBUX": "Starbucks", "TGT": "Target", "LOW": "Lowe's", "F": "Ford",
        "GM": "General Motors", "BKNG": "Booking Holdings", "ABNB": "Airbnb",
        "UBER": "Uber", "LYFT": "Lyft", "CMG": "Chipotle", "YUM": "Yum! Brands",
        "QSR": "Restaurant Brands", "DPZ": "Domino's", "DKNG": "DraftKings",
        "MGM": "MGM Resorts", "LVS": "Las Vegas Sands", "WYNN": "Wynn Resorts",
        "RCL": "Royal Caribbean", "CCL": "Carnival", "MAR": "Marriott",
        "HLT": "Hilton", "DHI": "D.R. Horton", "LEN": "Lennar", "PHM": "PulteGroup",
        "ROST": "Ross Stores", "TJX": "TJX Companies", "BBY": "Best Buy",
    },
    "Consumo Básico": {
        "PG": "Procter & Gamble", "KO": "Coca-Cola", "PEP": "PepsiCo",
        "WMT": "Walmart", "COST": "Costco", "PM": "Philip Morris",
        "MO": "Altria", "CL": "Colgate-Palmolive", "GIS": "General Mills",
        "K": "Kellanova", "KHC": "Kraft Heinz", "MDLZ": "Mondelez",
        "HSY": "Hershey", "CAG": "ConAgra", "CPB": "Campbell Soup",
        "SJM": "J.M. Smucker", "MKC": "McCormick", "CHD": "Church & Dwight",
        "CLX": "Clorox", "KMB": "Kimberly-Clark", "EL": "Estee Lauder",
        "ULTA": "Ulta Beauty", "COTY": "Coty Inc", "KR": "Kroger",
    },
    "Industriales": {
        "BA": "Boeing", "CAT": "Caterpillar", "GE": "GE Aerospace",
        "HON": "Honeywell", "UPS": "UPS", "FDX": "FedEx", "LMT": "Lockheed Martin",
        "RTX": "RTX Corp", "NOC": "Northrop Grumman", "GD": "General Dynamics",
        "MMM": "3M", "EMR": "Emerson Electric", "ETN": "Eaton",
        "PH": "Parker Hannifin", "ROK": "Rockwell Automation", "IR": "Ingersoll Rand",
        "XYL": "Xylem", "AME": "AMETEK", "ROP": "Roper Technologies",
        "CSGP": "CoStar Group", "WAB": "Wabtec", "CSX": "CSX Corp",
        "NSC": "Norfolk Southern", "UNP": "Union Pacific", "DAL": "Delta Air Lines",
        "UAL": "United Airlines", "AAL": "American Airlines", "LUV": "Southwest Airlines",
    },
    "Materiales": {
        "LIN": "Linde", "APD": "Air Products", "SHW": "Sherwin-Williams",
        "FCX": "Freeport-McMoRan", "NEM": "Newmont", "NUE": "Nucor",
        "STLD": "Steel Dynamics", "ALB": "Albemarle", "CE": "Celanese",
        "DD": "DuPont", "DOW": "Dow Inc", "LYB": "LyondellBasell",
        "PPG": "PPG Industries", "RPM": "RPM International", "ECL": "Ecolab",
        "IFF": "IFF", "MOS": "Mosaic", "CF": "CF Industries",
    },
    "Real Estate (REITs)": {
        "AMT": "American Tower", "PLD": "Prologis", "CCI": "Crown Castle",
        "EQIX": "Equinix", "PSA": "Public Storage", "EXR": "Extra Space Storage",
        "AVB": "AvalonBay", "EQR": "Equity Residential", "MAA": "Mid-America Apt",
        "SPG": "Simon Property", "O": "Realty Income", "VICI": "VICI Properties",
        "WELL": "Welltower", "VTR": "Ventas", "MPW": "Medical Properties",
        "DLR": "Digital Realty", "ARE": "Alexandria Real Estate",
    },
    "Comunicaciones": {
        "NFLX": "Netflix", "DIS": "Walt Disney", "CMCSA": "Comcast",
        "T": "AT&T", "VZ": "Verizon", "TMUS": "T-Mobile", "CHTR": "Charter Comm",
        "PARA": "Paramount", "WBD": "Warner Bros Discovery", "FOX": "Fox Corp",
        "SPOT": "Spotify", "SNAP": "Snap", "PINS": "Pinterest", "RDDT": "Reddit",
        "X": "X Holdings", "MTCH": "Match Group", "ZM": "Zoom", "TWLO": "Twilio",
    },
    "ETFs / Índices": {
        "SPY": "S&P 500 ETF", "QQQ": "Nasdaq 100 ETF", "IWM": "Russell 2000 ETF",
        "GLD": "Gold ETF", "TLT": "Treasury Bonds ETF", "EEM": "Emerging Markets ETF",
        "DIA": "Dow Jones ETF", "VTI": "Total Market ETF", "VOO": "Vanguard S&P 500",
        "VGK": "Europe ETF", "EWJ": "Japan ETF", "FXI": "China ETF",
        "XLK": "Tech Sector ETF", "XLF": "Financial Sector ETF",
        "XLE": "Energy Sector ETF", "XLV": "Health Sector ETF",
        "XLI": "Industrial ETF", "XLY": "Consumer Disc ETF",
        "SLV": "Silver ETF", "USO": "Oil ETF", "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
    },
}

MERVAL_UNIVERSE = {
    "Bancos": {
        "GGAL.BA": "Grupo Galicia", "BMA.BA": "Banco Macro", "BBAR.BA": "BBVA Argentina",
        "SUPV.BA": "Supervielle", "BHIP.BA": "Banco Hipotecario", "BPAT.BA": "Banco Patagonia",
        "BYMA.BA": "BYMA", "VALO.BA": "Grupo Financiero Valores",
    },
    "Energía & Petróleo": {
        "YPF.BA": "YPF", "PAMP.BA": "Pampa Energía", "TGNO4.BA": "TGN",
        "TGSU2.BA": "TGS", "CGPA2.BA": "Capex", "METR.BA": "MetroGAS",
        "GARO.BA": "Garovaglio & Zorraquín", "AUSO.BA": "Autopistas del Sol",
        "DGCU2.BA": "Distrib. Gas Cuyana", "DGCE.BA": "Dist. Gas Centro",
    },
    "Electricidad": {
        "CEPU.BA": "Central Puerto", "EDN.BA": "Edenor", "TRAN.BA": "Transener",
        "CECO2.BA": "Central Costanera", "HARG.BA": "Holcim Argentina",
        "PATA.BA": "Patagonia Gold",
    },
    "Real Estate & Construcción": {
        "IRSA.BA": "IRSA Prop. Comerciales", "IRCP.BA": "IRSA Inversiones",
        "CRES.BA": "Cresud", "DYCA.BA": "Dycasa", "CTIO.BA": "Consultatio",
    },
    "Consumo & Retail": {
        "MIRG.BA": "Mirgor", "MOLI.BA": "Molinos Río de la Plata",
        "MOLA.BA": "Molinos Agro", "BRIG.BA": "Briggs & Stratton Arg",
        "POLL.BA": "Polledo", "LONG.BA": "Longvie",
        "GAMI.BA": "Gamer Corporation", "SEMI.BA": "Instituto Rosenbusch",
    },
    "Agro & Alimentos": {
        "AGRO.BA": "Agrometal", "SAMI.BA": "San Miguel",
        "MORI.BA": "Morixe Hnos", "GCDI.BA": "GCDI",
        "CADO.BA": "Cadoppi", "INTR.BA": "Intratex",
    },
    "Telecomunicaciones": {
        "TECO2.BA": "Telecom Argentina", "TECO.BA": "Telecom (ord)",
        "CABR.BA": "Cablevision Holding",
    },
    "Acero, Minería & Industria": {
        "ERAR.BA": "Ternium Argentina", "LOMA.BA": "Loma Negra",
        "ALUA.BA": "Aluar", "BOLT.BA": "Boldt",
        "GBAN.BA": "Gas Natural BAN", "FERR.BA": "Ferrum",
        "RIGO.BA": "Rigolleau", "ROSE.BA": "Rosario Puerto",
    },
    "Salud & Pharma": {
        "GRIM.BA": "Grimoldi", "BIOL.BA": "Bioceres Crop",
        "INVJ.BA": "Inversora Juramento",
    },
    "Medios & Tecnología": {
        "TXAR.BA": "Transportadora Gas Sur", "HAVA.BA": "Havanna",
        "ESME.BA": "Esmeba",
    },
    "CEDEARs Internacionales": {
        "AAPL.BA": "Apple (CEDEAR)", "MSFT.BA": "Microsoft (CEDEAR)",
        "AMZN.BA": "Amazon (CEDEAR)", "GOOGL.BA": "Alphabet (CEDEAR)",
        "META.BA": "Meta (CEDEAR)", "NVDA.BA": "NVIDIA (CEDEAR)",
        "TSLA.BA": "Tesla (CEDEAR)", "BRKB.BA": "Berkshire (CEDEAR)",
        "KO.BA": "Coca-Cola (CEDEAR)", "DIS.BA": "Disney (CEDEAR)",
        "MELI.BA": "MercadoLibre (CEDEAR)", "GLD.BA": "Gold ETF (CEDEAR)",
        "SPY.BA": "S&P 500 ETF (CEDEAR)", "QQQ.BA": "Nasdaq ETF (CEDEAR)",
        "BRK.BA": "Berkshire B (CEDEAR)", "GOLD.BA": "Barrick Gold (CEDEAR)",
        "AXP.BA": "Amex (CEDEAR)", "IBM.BA": "IBM (CEDEAR)",
        "JNJ.BA": "J&J (CEDEAR)", "XOM.BA": "ExxonMobil (CEDEAR)",
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
            # Precio & mercado
            "ticker":           ticker,
            "name":             info.get("shortName", ticker),
            "price":            round(last_close, 2),
            "change_pct":       round(change_pct, 2),
            "volume":           int(volume),
            "mktcap":           info.get("marketCap"),
            "currency":         info.get("currency", "USD"),
            "52wHigh":          info.get("fiftyTwoWeekHigh"),
            "52wLow":           info.get("fiftyTwoWeekLow"),
            "beta":             info.get("beta"),
            "float_shares":     info.get("floatShares"),
            "avg_volume":       info.get("averageVolume"),
            # Valuación
            "pe":               info.get("trailingPE"),
            "forward_pe":       info.get("forwardPE"),
            "peg":              info.get("pegRatio"),
            "pb":               info.get("priceToBook"),
            "ps":               info.get("priceToSalesTrailing12Months"),
            "ev_ebitda":        info.get("enterpriseToEbitda"),
            "ev":               info.get("enterpriseValue"),
            "eps":              info.get("trailingEps"),
            "forward_eps":      info.get("forwardEps"),
            # Dividendos
            "dividend":         info.get("dividendYield"),
            "dividend_rate":    info.get("dividendRate"),
            "payout_ratio":     info.get("payoutRatio"),
            # Rentabilidad
            "roe":              info.get("returnOnEquity"),
            "roa":              info.get("returnOnAssets"),
            "margin_net":       info.get("profitMargins"),
            "margin_op":        info.get("operatingMargins"),
            "margin_gross":     info.get("grossMargins"),
            "revenue":          info.get("totalRevenue"),
            "ebitda":           info.get("ebitda"),
            "revenue_growth":   info.get("revenueGrowth"),
            "earnings_growth":  info.get("earningsGrowth"),
            # Deuda & solvencia
            "debt_equity":      info.get("debtToEquity"),
            "current_ratio":    info.get("currentRatio"),
            "quick_ratio":      info.get("quickRatio"),
            "total_debt":       info.get("totalDebt"),
            "cash":             info.get("totalCash"),
            # Analistas
            "target_price":     info.get("targetMeanPrice"),
            "target_high":      info.get("targetHighPrice"),
            "target_low":       info.get("targetLowPrice"),
            "recommendation":   info.get("recommendationKey", ""),
            "num_analysts":     info.get("numberOfAnalystOpinions"),
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
    Motor cuantitativo multi-indicador con scoring ponderado (0-100).
    Indicadores: SMA20/50/200 · RSI14 · MACD(12,26,9) · Bollinger(20,2σ) · Volumen · ATR14
    Score >= 65 → COMPRA | 35-64 → MANTENER | <= 34 → VENDER
    """
    if df.empty or len(df) < 51:
        return {
            "signal": "DATOS INSUFICIENTES", "color": "hold", "score": 50,
            "sma20": None, "sma50": None, "sma200": None, "rsi": None,
            "macd": None, "macd_signal": None, "macd_hist": None,
            "bb_upper": None, "bb_lower": None, "bb_mid": None, "bb_pct": None,
            "atr": None, "atr_pct": None, "support": None, "resistance": None,
            "trend_long": "N/D", "vol_signal": "N/D",
            "reason": "Historial insuficiente (mínimo 51 sesiones).",
            "details": {},
        }

    close  = df["Close"].squeeze()
    high   = df["High"].squeeze()
    low    = df["Low"].squeeze()
    volume = df["Volume"].squeeze() if "Volume" in df.columns else None
    price  = float(close.iloc[-1])

    # ── SMA 20 / 50 / 200 ──
    sma20  = float(close.rolling(20).mean().iloc[-1])
    sma50  = float(close.rolling(50).mean().iloc[-1])
    sma200 = float(close.rolling(200).mean().iloc[-1]) if len(df) >= 200 else None

    # ── RSI 14 ──
    delta      = close.diff()
    gain       = delta.clip(lower=0).rolling(14).mean()
    loss       = (-delta.clip(upper=0)).rolling(14).mean()
    rs         = gain / loss.replace(0, np.nan)
    rsi        = float((100 - (100 / (1 + rs))).iloc[-1])

    # ── MACD (12, 26, 9) ──
    ema12      = close.ewm(span=12, adjust=False).mean()
    ema26      = close.ewm(span=26, adjust=False).mean()
    macd_line  = ema12 - ema26
    macd_sig_l = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist  = macd_line - macd_sig_l
    macd_val   = float(macd_line.iloc[-1])
    macd_s_val = float(macd_sig_l.iloc[-1])
    macd_h_val = float(macd_hist.iloc[-1])
    macd_prev  = float(macd_hist.iloc[-2]) if len(macd_hist) >= 2 else macd_h_val

    # ── Bollinger Bands (20, 2σ) ──
    bb_mid_s   = close.rolling(20).mean()
    bb_std     = close.rolling(20).std()
    bb_upper   = float((bb_mid_s + 2 * bb_std).iloc[-1])
    bb_lower   = float((bb_mid_s - 2 * bb_std).iloc[-1])
    bb_mid_v   = float(bb_mid_s.iloc[-1])
    bb_pct     = (price - bb_lower) / (bb_upper - bb_lower) if (bb_upper - bb_lower) else 0.5

    # ── ATR 14 ──
    tr     = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs(),
    ], axis=1).max(axis=1)
    atr     = float(tr.rolling(14).mean().iloc[-1])
    atr_pct = round(atr / price * 100, 2) if price else 0

    # ── Volumen ──
    vol_signal_str = "N/D"
    vol_score_val  = 50
    if volume is not None and len(volume) >= 20:
        vol_avg   = float(volume.rolling(20).mean().iloc[-1])
        vol_today = float(volume.iloc[-1])
        vol_ratio = vol_today / vol_avg if vol_avg else 1
        if vol_ratio > 1.5:
            vol_signal_str, vol_score_val = "Muy Alto", 75
        elif vol_ratio > 1.2:
            vol_signal_str, vol_score_val = "Alto", 65
        elif vol_ratio > 0.8:
            vol_signal_str, vol_score_val = "Normal", 50
        else:
            vol_signal_str, vol_score_val = "Bajo", 30

    # ── Soporte & Resistencia (últimas 52 semanas) ──
    window_sr  = min(252, len(df))
    resistance = float(high.iloc[-window_sr:].quantile(0.95))
    support    = float(low.iloc[-window_sr:].quantile(0.05))

    # ── Tendencia largo plazo ──
    trend_long = ("Alcista 📈" if sma200 and price > sma200
                  else "Bajista 📉" if sma200 else "N/D")

    # ════════════════════════════════════
    # SCORING PONDERADO (0–100)
    # ════════════════════════════════════
    scores  = {}
    details = {}

    # 1. Cruce SMA 20/50 (20%)
    if sma20 > sma50 and price > sma20:
        scores["sma_cross"] = 80
        details["SMA 20/50"] = f"✅ Cruce alcista — SMA20 {sma20:.2f} > SMA50 {sma50:.2f}"
    elif sma20 < sma50 and price < sma20:
        scores["sma_cross"] = 20
        details["SMA 20/50"] = f"❌ Cruce bajista — SMA20 {sma20:.2f} < SMA50 {sma50:.2f}"
    else:
        scores["sma_cross"] = 50
        details["SMA 20/50"] = f"⚠️ Mixto — SMA20 {sma20:.2f} vs SMA50 {sma50:.2f}"

    # 2. SMA 200 tendencia (15%)
    if sma200:
        if price > sma200:
            scores["sma200"] = 75
            details["SMA 200"] = f"✅ Precio sobre SMA200 {sma200:.2f} — bull market"
        else:
            scores["sma200"] = 25
            details["SMA 200"] = f"❌ Precio bajo SMA200 {sma200:.2f} — bear market"
    else:
        scores["sma200"] = 50
        details["SMA 200"] = "⚠️ Sin datos suficientes (requiere 200 sesiones)"

    # 3. RSI 14 (20%)
    if rsi < 30:
        scores["rsi"] = 82
        details["RSI 14"] = f"✅ Sobreventa RSI {rsi:.1f} (<30) → rebote potencial"
    elif rsi < 40:
        scores["rsi"] = 65
        details["RSI 14"] = f"✅ RSI {rsi:.1f} — zona de acumulación"
    elif rsi > 70:
        scores["rsi"] = 18
        details["RSI 14"] = f"❌ Sobrecompra RSI {rsi:.1f} (>70) → corrección potencial"
    elif rsi > 60:
        scores["rsi"] = 40
        details["RSI 14"] = f"⚠️ RSI {rsi:.1f} — momentum elevado, cautela"
    else:
        scores["rsi"] = 55
        details["RSI 14"] = f"⚠️ RSI {rsi:.1f} — zona neutral"

    # 4. MACD (20%)
    if macd_h_val > 0 and macd_h_val > macd_prev:
        scores["macd"] = 82
        details["MACD"] = f"✅ Histograma ↑ positivo ({macd_h_val:+.4f}) — momentum alcista"
    elif macd_h_val > 0:
        scores["macd"] = 60
        details["MACD"] = f"⚠️ Histograma positivo pero debilitándose ({macd_h_val:+.4f})"
    elif macd_h_val < 0 and macd_h_val < macd_prev:
        scores["macd"] = 18
        details["MACD"] = f"❌ Histograma ↓ negativo ({macd_h_val:+.4f}) — momentum bajista"
    else:
        scores["macd"] = 40
        details["MACD"] = f"⚠️ Histograma negativo mejorando ({macd_h_val:+.4f})"

    # 5. Bollinger Bands (15%)
    if bb_pct < 0.15:
        scores["bollinger"] = 80
        details["Bollinger"] = f"✅ Precio en banda inferior ({bb_pct:.0%}) — zona de compra"
    elif bb_pct > 0.85:
        scores["bollinger"] = 20
        details["Bollinger"] = f"❌ Precio en banda superior ({bb_pct:.0%}) — zona de venta"
    elif bb_pct < 0.35:
        scores["bollinger"] = 65
        details["Bollinger"] = f"✅ Precio bajo media Bollinger ({bb_pct:.0%}) — sesgo alcista"
    elif bb_pct > 0.65:
        scores["bollinger"] = 40
        details["Bollinger"] = f"⚠️ Precio sobre media Bollinger ({bb_pct:.0%}) — sesgo bajista"
    else:
        scores["bollinger"] = 52
        details["Bollinger"] = f"⚠️ Precio en zona media ({bb_pct:.0%})"

    # 6. Volumen (10%)
    scores["volume"] = vol_score_val
    icon = "✅" if vol_score_val >= 65 else "⚠️" if vol_score_val == 50 else "❌"
    details["Volumen"] = f"{icon} Volumen {vol_signal_str} vs promedio 20 días"

    # Score final
    weights = {"sma_cross": 0.20, "sma200": 0.15, "rsi": 0.20,
               "macd": 0.20, "bollinger": 0.15, "volume": 0.10}
    score = round(sum(scores[k] * weights[k] for k in weights), 1)

    if score >= 65:
        signal, color = "COMPRA", "buy"
    elif score <= 34:
        signal, color = "VENDER", "sell"
    else:
        signal, color = "MANTENER", "hold"

    bulls = [v.replace("✅ ", "") for v in details.values() if "✅" in v]
    bears = [v.replace("❌ ", "") for v in details.values() if "❌" in v]
    reason = f"Score: {score}/100. "
    if bulls: reason += f"Favorable: {bulls[0]}. "
    if bears: reason += f"En contra: {bears[0]}."

    return {
        "signal": signal, "color": color, "score": score,
        "sma20": round(sma20, 2), "sma50": round(sma50, 2),
        "sma200": round(sma200, 2) if sma200 else None,
        "rsi": round(rsi, 1),
        "macd": round(macd_val, 4), "macd_signal": round(macd_s_val, 4),
        "macd_hist": round(macd_h_val, 4),
        "bb_upper": round(bb_upper, 2), "bb_lower": round(bb_lower, 2),
        "bb_mid": round(bb_mid_v, 2), "bb_pct": round(bb_pct, 3),
        "atr": round(atr, 2), "atr_pct": atr_pct,
        "support": round(support, 2), "resistance": round(resistance, 2),
        "trend_long": trend_long, "vol_signal": vol_signal_str,
        "reason": reason, "details": details,
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

# Tema base sin propiedades de ejes — compatible con todos los tipos de gráfico
BASE_THEME = dict(
    paper_bgcolor="#06090f",
    plot_bgcolor="#06090f",
    font=dict(color="#8fadc8", family="Inter, sans-serif", size=11),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1a2d4a", borderwidth=1),
)


def plot_candlestick(df: pd.DataFrame, ticker: str,
                     sma20=None, sma50=None, sma200=None,
                     show_bb=False, support=None, resistance=None) -> go.Figure:
    """Gráfico de velas OHLC con SMA20/50/200 + Bollinger + Soporte/Resistencia."""
    fig = go.Figure()

    # ── Bollinger Bands (debajo de todo) ──
    if show_bb:
        bb_m = df["Close"].rolling(20).mean()
        bb_s = df["Close"].rolling(20).std()
        bb_u = bb_m + 2 * bb_s
        bb_l = bb_m - 2 * bb_s
        fig.add_trace(go.Scatter(
            x=df.index, y=bb_u, name="BB Superior",
            line=dict(color="#6366f1", width=1, dash="dot"), opacity=0.7,
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=bb_l, name="BB Inferior",
            line=dict(color="#6366f1", width=1, dash="dot"),
            fill="tonexty", fillcolor="rgba(99,102,241,0.05)", opacity=0.7,
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=bb_m, name="BB Media",
            line=dict(color="#818cf8", width=0.8, dash="dash"), opacity=0.6,
        ))

    # ── Velas ──
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"],   close=df["Close"],
        increasing_line_color="#22c55e",
        decreasing_line_color="#ef4444",
        increasing_fillcolor="#22c55e",
        decreasing_fillcolor="#ef4444",
        name=ticker,
    ))

    # ── SMAs ──
    if sma20 is not None:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"].rolling(20).mean(), name="SMA 20",
            line=dict(color="#f59e0b", width=1.5),
        ))
    if sma50 is not None:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"].rolling(50).mean(), name="SMA 50",
            line=dict(color="#3b82f6", width=1.5, dash="dash"),
        ))
    if sma200 is not None and len(df) >= 200:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"].rolling(200).mean(), name="SMA 200",
            line=dict(color="#ec4899", width=1.5, dash="longdash"),
        ))

    # ── Soporte & Resistencia ──
    if support is not None:
        fig.add_hline(y=support, line_color="#22c55e", line_width=1.2, line_dash="dot",
                      annotation_text=f"Soporte {support:.2f}",
                      annotation_font=dict(color="#22c55e", size=10))
    if resistance is not None:
        fig.add_hline(y=resistance, line_color="#ef4444", line_width=1.2, line_dash="dot",
                      annotation_text=f"Resistencia {resistance:.2f}",
                      annotation_font=dict(color="#ef4444", size=10))

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
        paper_bgcolor="#06090f",
        plot_bgcolor="#06090f",
        font=dict(color="#8fadc8", family="Inter, sans-serif", size=11),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1a2d4a", borderwidth=1),
        title=dict(text="<b>Comparador de Rendimiento</b> (base 100)",
                   font=dict(color="#e8f0fe", size=14)),
        xaxis=dict(gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
        yaxis=dict(gridcolor="#0d1a2e", zerolinecolor="#0d1a2e", title="Rendimiento %"),
        hovermode="x unified",
        margin=dict(l=10, r=10, t=40, b=10),
        height=460,
    )
    return fig


def plot_macd(df: pd.DataFrame) -> go.Figure:
    """Panel MACD (12,26,9) standalone."""
    close     = df["Close"].squeeze()
    ema12     = close.ewm(span=12, adjust=False).mean()
    ema26     = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    macd_sig  = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - macd_sig

    colors_hist = ["#22c55e" if v >= 0 else "#ef4444" for v in macd_hist]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index, y=macd_hist, name="Histograma",
        marker_color=colors_hist, opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=macd_line, name="MACD",
        line=dict(color="#3b82f6", width=1.5),
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=macd_sig, name="Señal",
        line=dict(color="#f59e0b", width=1.2, dash="dash"),
    ))
    fig.add_hline(y=0, line_color="#1a2d4a", line_width=1)
    fig.update_layout(
        paper_bgcolor="#06090f", plot_bgcolor="#06090f",
        font=dict(color="#8fadc8", family="Inter, sans-serif", size=11),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1a2d4a", borderwidth=1),
        title=dict(text="MACD (12, 26, 9)", font=dict(color="#e8f0fe", size=13)),
        xaxis=dict(gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
        yaxis=dict(gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
        hovermode="x unified",
        height=200,
        margin=dict(l=10, r=10, t=35, b=10),
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
        paper_bgcolor="#06090f",
        plot_bgcolor="#06090f",
        font=dict(color="#8fadc8", family="Inter, sans-serif", size=11),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1a2d4a", borderwidth=1),
        title=dict(text="RSI (14)", font=dict(color="#e8f0fe", size=13)),
        xaxis=dict(gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
        yaxis=dict(range=[0, 100], gridcolor="#0d1a2e", zerolinecolor="#0d1a2e"),
        hovermode="x unified",
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
    st.markdown('<div style="color:#7fa3d0;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">🔍 BUSCADOR POR TICKER</div>', unsafe_allow_html=True)
    manual_ticker = st.text_input(
        label="Ticker manual",
        placeholder="Ej: TSLA, GGAL.BA, BTC-USD",
        label_visibility="collapsed",
    ).strip().upper()
    if manual_ticker:
        st.caption(f"Analizando ticker: **{manual_ticker}**")

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
                ),
                texttemplate="<b>%{label}</b><br>%{customdata[1]:+.1f}%",
            ))
            fig_heat.update_layout(
                paper_bgcolor="#06090f",
                plot_bgcolor="#06090f",
                font=dict(color="#8fadc8", family="Inter, sans-serif", size=11),
                height=320,
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig_heat, use_container_width=True)


# ═════════════════════════════════════════════════════════════
# TAB 2 — ANÁLISIS INDIVIDUAL
# ═════════════════════════════════════════════════════════════
with tab2:
    # sector_tickers = {ticker: nombre} → invertimos para buscar por nombre
    _name_to_ticker2 = {v: k for k, v in sector_tickers.items()}
    # El buscador manual tiene prioridad sobre el selector
    if manual_ticker:
        selected_ticker = manual_ticker
        selected_name_display = manual_ticker
    elif selected_name != "— Seleccioná un activo —" and selected_name in _name_to_ticker2:
        selected_ticker = _name_to_ticker2[selected_name]
        selected_name_display = selected_name
    else:
        selected_ticker = None
        selected_name_display = None

    if not selected_ticker:
        st.info("👈 Seleccioná un activo desde el panel lateral o ingresá un ticker en el buscador.")
    if selected_ticker:
        st.markdown(f'<div class="section-title">{selected_ticker} — {selected_name_display} · Análisis Técnico</div>',
                    unsafe_allow_html=True)

        # Datos de cotización
        with st.spinner(f"Cargando {selected_ticker}…"):
            quote = fetch_quote(selected_ticker)

        if quote is None:
            st.error(f"⚠️ No se pudieron obtener datos para **{selected_ticker}**. "
                     f"El ticker puede estar caído o fuera de horario.")
        else:
            currency = quote.get("currency", "USD")

            def fv(val, fmt=".2f", suffix="", prefix=""):
                """Formatea un valor o devuelve N/D."""
                if val is None or (isinstance(val, float) and (val != val)):
                    return "N/D"
                try:
                    return f"{prefix}{val:{fmt}}{suffix}"
                except Exception:
                    return "N/D"

            def fpct(val):
                return fv(val * 100, ".1f", "%") if val is not None else "N/D"

            def frec(key):
                MAP = {
                    "strong_buy": "🟢 Compra Fuerte", "buy": "🟢 Compra",
                    "hold": "🟡 Mantener", "underperform": "🔴 Subperforma",
                    "sell": "🔴 Vender", "": "N/D",
                }
                return MAP.get(str(key).lower(), str(key).title()) if key else "N/D"

            # ── Fila 0: Header precio ──
            h1, h2, h3, h4, h5, h6 = st.columns(6)
            h1.metric("Precio",        f"{currency} {quote['price']:,.2f}")
            h2.metric("Var. Día",      f"{quote['change_pct']:+.2f}%", delta=f"{quote['change_pct']:+.2f}%")
            h3.metric("Cap. Mercado",  fmt_large(quote['mktcap']))
            h4.metric("Volumen",       f"{quote['volume']:,}" if quote['volume'] else "N/D")
            h5.metric("Máx 52 sem",    fv(quote['52wHigh'], ",.2f", prefix=f"{currency} "))
            h6.metric("Mín 52 sem",    fv(quote['52wLow'],  ",.2f", prefix=f"{currency} "))

            st.markdown("---")

            # Corrección Div. Yield (Yahoo a veces devuelve payout en ese campo)
            div_yield = quote.get('dividend')
            if div_yield and div_yield > 0.5:
                div_yield = None  # Valor anómalo, descartamos

            st.markdown('<div class="ratio-block">', unsafe_allow_html=True)

            # ── Card 1: Valuación (2 filas × 4 col) ──
            st.markdown('<div class="ratio-card"><div class="ratio-card-title">📊 Ratios de Valuación</div>', unsafe_allow_html=True)
            v1, v2, v3, v4 = st.columns(4)
            v1.metric("P/E Trailing",   fv(quote['pe'],        ".1f", "x"))
            v2.metric("P/E Forward",    fv(quote['forward_pe'],".1f", "x"))
            v3.metric("PEG Ratio",      fv(quote['peg'],       ".2f", "x"))
            v4.metric("P/Book",         fv(quote['pb'],        ".2f", "x"))
            v5, v6, v7, v8 = st.columns(4)
            v5.metric("P/Sales",        fv(quote['ps'],        ".2f", "x"))
            v6.metric("EV/EBITDA",      fv(quote['ev_ebitda'], ".1f", "x"))
            v7.metric("EPS Trailing",   fv(quote['eps'],       ".2f", prefix=f"{currency} "))
            v8.metric("EPS Forward",    fv(quote['forward_eps'],".2f",prefix=f"{currency} "))
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Card 2: Rentabilidad (2 filas × 4 col) ──
            st.markdown('<div class="ratio-card"><div class="ratio-card-title">💰 Rentabilidad & Crecimiento</div>', unsafe_allow_html=True)
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("ROE",            fpct(quote['roe']))
            r2.metric("ROA",            fpct(quote['roa']))
            r3.metric("Margen Bruto",   fpct(quote['margin_gross']))
            r4.metric("Margen Op.",     fpct(quote['margin_op']))
            r5, r6, r7, r8 = st.columns(4)
            r5.metric("Margen Neto",    fpct(quote['margin_net']))
            r6.metric("Revenue",        fmt_large(quote.get('revenue')))
            r7.metric("Crec. Revenue",  fpct(quote['revenue_growth']))
            r8.metric("Crec. EPS",      fpct(quote['earnings_growth']))
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Card 3: Deuda (1 fila × 4 col + upside) ──
            st.markdown('<div class="ratio-card"><div class="ratio-card-title">🏦 Deuda & Solvencia</div>', unsafe_allow_html=True)
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Deuda/Equity",   fv(quote['debt_equity'],  ".1f", "x"))
            d2.metric("Current Ratio",  fv(quote['current_ratio'],".2f", "x"))
            d3.metric("Quick Ratio",    fv(quote['quick_ratio'],  ".2f", "x"))
            d4.metric("Beta",           fv(quote['beta'],         ".2f"))
            d5, d6, d7, d8 = st.columns(4)
            d5.metric("Deuda Total",    fmt_large(quote['total_debt']))
            d6.metric("Caja & Equiv.",  fmt_large(quote['cash']))
            d7.metric("EV",             fmt_large(quote.get('ev')))
            d8.metric("EBITDA",         fmt_large(quote.get('ebitda')))
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Card 4: Dividendos & Analistas (2 filas × 4 col) ──
            st.markdown('<div class="ratio-card"><div class="ratio-card-title">🎯 Dividendos & Consenso de Analistas</div>', unsafe_allow_html=True)
            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Div. Yield",     fpct(div_yield))
            a2.metric("Div. Rate",      fv(quote['dividend_rate'], ".2f", prefix=f"{currency} "))
            a3.metric("Payout Ratio",   fpct(quote['payout_ratio']))
            a4.metric("Consenso",       frec(quote['recommendation']))
            a5, a6, a7, a8 = st.columns(4)
            a5.metric("Target Medio",   fv(quote['target_price'], ",.2f", prefix=f"{currency} "))
            a6.metric("Target Máx",     fv(quote['target_high'],  ",.2f", prefix=f"{currency} "))
            a7.metric("Target Mín",     fv(quote['target_low'],   ",.2f", prefix=f"{currency} "))
            n_analysts = quote.get('num_analysts') or 0
            a8.metric("N° Analistas",   str(n_analysts) if n_analysts else "N/D")

            # Upside/downside vs target
            if quote['target_price'] and quote['price']:
                upside = ((quote['target_price'] / quote['price']) - 1) * 100
                color_up = "#22c55e" if upside > 0 else "#ef4444"
                arrow = "▲" if upside > 0 else "▼"
                st.markdown(
                    f'<div style="margin-top:0.6rem;padding:0.5rem 1rem;background:#06090f;'
                    f'border:1px solid #1a2d4a;border-radius:8px;display:inline-block;">'
                    f'<span style="color:#5a7fa8;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;">Upside vs. Target Consenso &nbsp;</span>'
                    f'<span style="color:{color_up};font-weight:700;font-size:1rem;">{arrow} {upside:+.1f}%</span>'
                    f'<span style="color:#3a5a80;font-size:0.7rem;margin-left:0.8rem;">({n_analysts} analistas)</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)  # cierre ratio-block
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
# TAB 4 — SEÑAL CUANTITATIVA (MOTOR MULTI-INDICADOR)
# ═════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🤖 Sistema de Recomendación Cuantitativa — Motor Multi-Indicador</div>',
                unsafe_allow_html=True)

    if manual_ticker:
        selected_ticker_q = manual_ticker
        selected_name_q   = manual_ticker
    elif selected_name != "— Seleccioná un activo —" and selected_name in _name_to_ticker2:
        selected_ticker_q = _name_to_ticker2[selected_name]
        selected_name_q   = selected_name
    else:
        selected_ticker_q = None
        selected_name_q   = None

    if not selected_ticker_q:
        st.info("👈 Seleccioná un activo desde el panel lateral o ingresá un ticker en el buscador.")

    if selected_ticker_q:
        st.caption(f"Analizando: **{selected_ticker_q}** — {selected_name_q}")

        with st.spinner("Calculando 6 indicadores técnicos…"):
            df_signal = fetch_ohlcv(selected_ticker_q, period="2y")
            signals   = compute_technical_signals(df_signal)

        chip_class   = {"buy": "rec-buy", "hold": "rec-hold", "sell": "rec-sell"}
        chip_emoji   = {"buy": "🟢", "hold": "🟡", "sell": "🔴"}
        label_map    = {"buy": "COMPRA", "hold": "MANTENER", "sell": "VENDER"}
        color_key    = signals["color"] if signals["color"] in chip_class else "hold"
        signal_label = label_map.get(color_key, signals["signal"])
        score        = signals.get("score", 50)

        # ── FILA 1: Señal + Score gauge + Razón ──
        col_chip, col_gauge, col_reason = st.columns([1.2, 1, 2])

        with col_chip:
            st.markdown(
                f'<div style="text-align:center;padding:1.2rem 0 0.5rem 0;">'
                f'<div class="rec-chip {chip_class[color_key]}">'
                f'{chip_emoji[color_key]} {signal_label}</div>'
                f'<div style="color:#5a7fa8;font-size:0.7rem;margin-top:0.4rem;">'
                f'Motor: 6 indicadores ponderados</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col_gauge:
            gauge_color = "#22c55e" if score >= 65 else ("#ef4444" if score <= 34 else "#f59e0b")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Score", "font": {"color": "#8fadc8", "size": 12}},
                number={"font": {"color": gauge_color, "size": 28}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#1a2d4a",
                             "tickfont": {"color": "#5a7fa8", "size": 9}},
                    "bar":  {"color": gauge_color, "thickness": 0.25},
                    "bgcolor": "#0d1526",
                    "bordercolor": "#1a2d4a",
                    "steps": [
                        {"range": [0, 34],  "color": "rgba(239,68,68,0.15)"},
                        {"range": [34, 65], "color": "rgba(245,158,11,0.10)"},
                        {"range": [65, 100],"color": "rgba(34,197,94,0.15)"},
                    ],
                    "threshold": {"line": {"color": gauge_color, "width": 2},
                                  "thickness": 0.7, "value": score},
                },
            ))
            fig_gauge.update_layout(
                paper_bgcolor="#06090f", plot_bgcolor="#06090f",
                font=dict(color="#8fadc8"),
                height=160, margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig_gauge, use_container_width=True, key="chart_gauge")

        with col_reason:
            st.markdown("**📋 Análisis:**")
            st.info(signals["reason"])
            t_long = signals.get("trend_long", "N/D")
            vol_s  = signals.get("vol_signal", "N/D")
            atr_p  = signals.get("atr_pct", 0)
            st.markdown(
                f'<div style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-top:0.4rem;">'
                f'<span style="background:#0d1526;border:1px solid #1a2d4a;border-radius:6px;'
                f'padding:0.2rem 0.6rem;font-size:0.72rem;color:#8fadc8;">📈 Tendencia: <b style="color:#e8f0fe">{t_long}</b></span>'
                f'<span style="background:#0d1526;border:1px solid #1a2d4a;border-radius:6px;'
                f'padding:0.2rem 0.6rem;font-size:0.72rem;color:#8fadc8;">📊 Volumen: <b style="color:#e8f0fe">{vol_s}</b></span>'
                f'<span style="background:#0d1526;border:1px solid #1a2d4a;border-radius:6px;'
                f'padding:0.2rem 0.6rem;font-size:0.72rem;color:#8fadc8;">⚡ ATR: <b style="color:#e8f0fe">{atr_p:.1f}%</b></span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # ── FILA 2: Métricas de indicadores ──
        st.markdown("---")
        st.markdown('<div class="section-title">📐 Valores de Indicadores</div>', unsafe_allow_html=True)

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("SMA 20",   f"{signals['sma20']:.2f}"    if signals['sma20']   else "N/D",
                  help="Media móvil 20 sesiones — tendencia corto plazo")
        m2.metric("SMA 50",   f"{signals['sma50']:.2f}"    if signals['sma50']   else "N/D",
                  help="Media móvil 50 sesiones — tendencia mediano plazo")
        m3.metric("SMA 200",  f"{signals['sma200']:.2f}"   if signals['sma200']  else "N/D",
                  help="Media móvil 200 sesiones — tendencia largo plazo")
        m4.metric("RSI 14",   f"{signals['rsi']:.1f}"      if signals['rsi']     else "N/D",
                  help="<30 sobreventa · >70 sobrecompra")
        m5.metric("MACD Hist",f"{signals['macd_hist']:+.4f}"if signals['macd_hist'] is not None else "N/D",
                  help="Histograma MACD: positivo = momentum alcista")
        m6.metric("BB %",     f"{signals['bb_pct']:.0%}"   if signals['bb_pct']  is not None else "N/D",
                  help="Posición dentro de las Bandas de Bollinger (0%=inferior, 100%=superior)")

        m7, m8, m9, m10, _, _ = st.columns(6)
        m7.metric("Soporte",     f"{signals['support']:.2f}"     if signals['support']     else "N/D",
                  help="Nivel de soporte clave (percentil 5%, últimas 52 semanas)")
        m8.metric("Resistencia", f"{signals['resistance']:.2f}"  if signals['resistance']  else "N/D",
                  help="Nivel de resistencia clave (percentil 95%, últimas 52 semanas)")
        m9.metric("ATR 14",      f"{signals['atr']:.2f}"         if signals['atr']         else "N/D",
                  help="Average True Range — volatilidad real diaria promedio")
        m10.metric("ATR %",      f"{signals['atr_pct']:.1f}%"    if signals['atr_pct']     else "N/D",
                   help="ATR como % del precio — riesgo diario normalizado")

        # ── FILA 3: Detalle por indicador ──
        st.markdown("---")
        st.markdown('<div class="section-title">🔍 Detalle por Indicador</div>', unsafe_allow_html=True)

        details = signals.get("details", {})
        if details:
            for indicador, desc in details.items():
                icon_color = "#22c55e" if "✅" in desc else ("#ef4444" if "❌" in desc else "#f59e0b")
                st.markdown(
                    f'<div style="padding:0.45rem 0.8rem;margin-bottom:0.35rem;'
                    f'background:#0a111f;border-left:3px solid {icon_color};'
                    f'border-radius:0 6px 6px 0;font-size:0.82rem;color:#c8d6f0;">'
                    f'<b style="color:{icon_color};">{indicador}</b> — {desc}</div>',
                    unsafe_allow_html=True,
                )

        # ── FILA 4: Gráficos técnicos ──
        st.markdown("---")
        st.markdown('<div class="section-title">📈 Gráficos con Señales Técnicas (2 años)</div>',
                    unsafe_allow_html=True)

        if not df_signal.empty:
            fig_sig = plot_candlestick(
                df_signal, selected_ticker_q,
                sma20=signals.get("sma20"),
                sma50=signals.get("sma50"),
                sma200=signals.get("sma200"),
                show_bb=True,
                support=signals.get("support"),
                resistance=signals.get("resistance"),
            )
            st.plotly_chart(fig_sig, use_container_width=True, key="chart_sig")

            if len(df_signal) >= 26:
                st.plotly_chart(plot_macd(df_signal), use_container_width=True, key="chart_macd_tab4")
            if len(df_signal) >= 15:
                st.plotly_chart(plot_rsi(df_signal), use_container_width=True, key="chart_rsi_tab4")

        # ── Disclaimer ──
        st.markdown("---")
        st.warning(
            "⚠️ **Disclaimer:** Esta señal es generada por un algoritmo cuantitativo para fines "
            "educativos e informativos. No constituye asesoramiento de inversión. "
            "Las decisiones de inversión son exclusiva responsabilidad del usuario. "
            "Consultá siempre con un asesor financiero certificado antes de operar."
        )
