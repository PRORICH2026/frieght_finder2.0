import streamlit as st
import base64

def get_base64(img):
    with open(img, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_css():
    bg = get_base64("bg.png")
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800;900&display=swap');
    * {{ font-family: 'Sora', sans-serif !important; }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}

    .stApp {{
        background-image: url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {{
        background: #0d1421 !important;
        border-right: 1px solid rgba(255,255,255,0.07) !important;
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        padding: 0 12px !important;
    }}
    .logo-box {{
        display: flex; align-items: center; gap: 10px;
        padding: 28px 8px 22px 8px; margin-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }}
    .logo-icon {{
        font-size: 28px;
        background: linear-gradient(135deg, #4f8ef7, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .logo-text {{
        font-size: 26px; font-weight: 900; line-height: 1.15;
        background: linear-gradient(135deg, #4f8ef7, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 3px;
    }}
    .nav-active button {{
        background: linear-gradient(135deg, #6c4ff7, #a855f7) !important;
        color: white !important; font-weight: 700 !important;
        box-shadow: 0 4px 18px rgba(108,79,247,0.5) !important;
        border: none !important; width: 100% !important; height: 50px !important;
        border-radius: 14px !important; font-size: 15px !important;
        text-align: left !important; padding: 0 16px !important; margin-bottom: 6px !important;
    }}
    .nav-item button {{
        background: transparent !important; color: rgba(255,255,255,0.55) !important;
        border: none !important; box-shadow: none !important; width: 100% !important;
        height: 50px !important; border-radius: 14px !important; font-size: 15px !important;
        font-weight: 600 !important; text-align: left !important;
        padding: 0 16px !important; margin-bottom: 6px !important;
    }}
    .nav-item button:hover {{ background: rgba(255,255,255,0.07) !important; color: white !important; }}
    .nav-logout button {{
        background: transparent !important; color: rgba(255,255,255,0.4) !important;
        border: none !important; box-shadow: none !important; width: 100% !important;
        height: 50px !important; border-radius: 14px !important; font-size: 15px !important; font-weight: 600 !important;
    }}
    .nav-logout button:hover {{ background: rgba(255,80,80,0.1) !important; color: #ff6b6b !important; }}

    /* ── SIDEBAR RESET BUTTON ── */
    .nav-reset button {{
        background: linear-gradient(135deg,#d946ef,#f43f5e) !important;
        color: white !important; border: none !important;
        box-shadow: 0 4px 18px rgba(212,70,239,0.4) !important;
        width: 100% !important; height: 50px !important;
        border-radius: 14px !important; font-size: 14px !important;
        font-weight: 800 !important; letter-spacing: 1px !important;
    }}
    .nav-reset button:hover {{
        box-shadow: 0 6px 24px rgba(212,70,239,0.65) !important;
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg,#c026d3,#e11d48) !important;
        color: white !important;
    }}

    /* ── HERO ── */
    .hero-wrap {{ text-align: center; padding: 60px 40px 0px 40px; }}
    .hero-title {{
        font-size: 72px !important; font-weight: 900 !important; color: white !important;
        letter-spacing: -2px; line-height: 1.05;
        text-shadow: 0 4px 30px rgba(0,0,0,0.6); margin-bottom: 12px;
    }}
    .hero-sub {{
        font-size: 18px !important; font-weight: 400;
        color: rgba(255,255,255,0.78); margin-bottom: 32px;
    }}

    /* ── SELECTBOX AUTOCOMPLETE STYLING ── */
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stSelectbox"] > div > div {{
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1.5px solid rgba(255,255,255,0.13) !important;
        border-radius: 11px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        min-height: 50px !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stSelectbox"] svg {{
        fill: rgba(255,255,255,0.5) !important;
    }}
    /* Dropdown popup list */
    [data-baseweb="popover"] ul {{
        background: #0d1421 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
    }}
    [data-baseweb="popover"] li {{
        color: rgba(255,255,255,0.75) !important;
        font-size: 14px !important;
    }}
    [data-baseweb="popover"] li:hover {{
        background: rgba(108,79,247,0.3) !important;
        color: white !important;
    }}
    /* Search box inside dropdown */
    [data-baseweb="popover"] input {{
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}

    /* ── SEARCH CARD (compact) ── */
    .search-wrap {{
        max-width: 820px; margin: 0 auto;
        background: rgba(10,18,38,0.90);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 18px;
        padding: 28px 28px 26px 28px;
        backdrop-filter: blur(28px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.55);
    }}
    .field-label {{
        font-size: 10px !important; font-weight: 700 !important;
        color: rgba(255,255,255,0.45) !important;
        letter-spacing: 2px !important; text-transform: uppercase !important;
        margin-bottom: 6px !important; display: block;
    }}

    /* Big H1-style label inside search card */
    .big-label {{
        font-size: 28px !important;
        font-weight: 800 !important;
        color: white !important;
        line-height: 1.15 !important;
        margin-bottom: 12px !important;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 12px rgba(0,0,0,0.4);
    }}
    .search-wrap input {{
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1.5px solid rgba(255,255,255,0.13) !important;
        border-radius: 11px !important;
        font-size: 14px !important; font-weight: 500 !important;
        height: 46px !important;
    }}
    .search-wrap input:focus {{
        border-color: rgba(108,79,247,0.8) !important;
        box-shadow: 0 0 0 3px rgba(108,79,247,0.18) !important;
        background: rgba(255,255,255,0.12) !important;
    }}
    .search-wrap input::placeholder {{
        color: rgba(255,255,255,0.25) !important; font-size: 13px !important;
    }}
    .search-wrap .stButton > button {{
        background: linear-gradient(135deg, #d946ef, #f43f5e) !important;
        color: white !important; border: none !important;
        border-radius: 11px !important; font-size: 13px !important;
        font-weight: 800 !important; height: 46px !important; width: 100% !important;
        letter-spacing: 2px !important; text-transform: uppercase !important;
        box-shadow: 0 4px 20px rgba(212,70,239,0.45) !important;
    }}
    .search-wrap .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(212,70,239,0.65) !important;
    }}

    /* ── METRIC CARDS ── */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        padding: 28px 40px 0 40px;
    }}
    .metric-card {{
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.45);
    }}
    .metric-card-header {{
        padding: 10px 18px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: white;
    }}
    .metric-card-body {{
        background: rgba(10,18,38,0.88);
        backdrop-filter: blur(20px);
        padding: 18px 18px 20px 18px;
        border: 1px solid rgba(255,255,255,0.08);
        border-top: none;
        border-radius: 0 0 16px 16px;
    }}
    .metric-card-value {{
        font-size: 36px;
        font-weight: 900;
        color: white;
        line-height: 1;
        margin-bottom: 4px;
    }}
    .metric-card-sub {{
        font-size: 12px;
        color: rgba(255,255,255,0.4);
        font-weight: 500;
    }}

    /* ── DATA TABLE ── */
    .table-wrap {{ padding: 24px 40px; }}
    [data-testid="stDataFrame"] {{
        background: rgba(10,18,35,0.88) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important; overflow: hidden !important;
    }}

    /* ── DOWNLOAD BTN ── */
    [data-testid="stDownloadButton"] > button {{
        background: rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.75) !important;
        border: 1px solid rgba(255,255,255,0.13) !important;
        border-radius: 10px !important; font-size: 14px !important;
        font-weight: 600 !important; box-shadow: none !important;
    }}

    /* ── PAGE TITLE ── */
    .page-title {{
        font-size: 42px !important; font-weight: 900 !important;
        color: white !important; padding: 44px 40px 8px 40px;
        text-shadow: 0 2px 20px rgba(0,0,0,0.5);
    }}

    </style>
    """, unsafe_allow_html=True)
