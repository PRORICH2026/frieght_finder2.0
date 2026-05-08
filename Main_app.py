import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(layout="wide", page_title="Freight Finder", page_icon="🚚")
load_css()

@st.cache_data
def load_data():
    df = pd.read_excel("Freight_Master.xlsx").fillna("")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

if "page" not in st.session_state:
    st.session_state.page = "finder"

# ── Reset counter: changing widget key = guaranteed empty input ──
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0
rc = st.session_state.reset_count

# ── SIDEBAR ────────────────────────────────────────────
st.sidebar.markdown("""
<div class="logo-box">
  <span class="logo-icon">☰</span>
  <div class="logo-text">MENU</div>
</div>
""", unsafe_allow_html=True)

def nav_btn(label, key, icon):
    css = "nav-active" if st.session_state.page == key else "nav-item"
    st.sidebar.markdown(f'<div class="{css}">', unsafe_allow_html=True)
    if st.sidebar.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
        st.session_state.page = key
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

nav_btn("Freight Finder", "finder", "🚚")
nav_btn("Data View",      "data",   "🗂️")
nav_btn("About",          "about",  "ℹ️")

# Spacer then Reset button at bottom (replaces Logout)
st.sidebar.markdown("<div style='min-height:300px'></div>", unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-reset">', unsafe_allow_html=True)
if st.sidebar.button("🔄  Reset Search", key="sidebar_reset", use_container_width=True):
    st.session_state.reset_count += 1
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

page = st.session_state.page

# ── FREIGHT FINDER ─────────────────────────────────────
if page == "finder":

    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-title">Freight Finder</div>
      <div class="hero-sub">Find the best freight rates across locations</div>
    </div>
    """, unsafe_allow_html=True)

    # Search Card — party left, delivery right, SEARCH below (no Clear All Filters)
    with st.container(border=True):
        col1, col2 = st.columns([5, 5])
        with col1:
            # key uses rc so resetting rc clears the widget instantly
            party = st.text_input(
                "Enter Loading Party",
                placeholder="Type loading party...",
                key=f"p_in_{rc}"
            )
        with col2:
            delivery = st.text_input(
                "Enter Delivery Location",
                placeholder="Type delivery location...",
                key=f"d_in_{rc}"
            )
        btn_col1, btn_col2, btn_col3 = st.columns([3, 2, 3])
        with btn_col2:
            search = st.button("🔍 SEARCH", use_container_width=True, key="search_btn")

    # Filter
    filtered = df.copy()
    if delivery:
        filtered = filtered[filtered["DELIVERY LOCATION"].str.contains(delivery, case=False, na=False)]
    if party:
        filtered = filtered[filtered["LOADING PARTY"].str.contains(party, case=False, na=False)]

    # Results
    if search or delivery or party:
        if filtered.empty:
            st.markdown("<div style='padding:20px 40px'>", unsafe_allow_html=True)
            st.warning("❌ No records found. Try different search terms.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            rates = pd.to_numeric(filtered["FROM RATE"], errors="coerce").dropna()
            count  = f"{len(filtered):,}"
            r_min  = f"₹ {int(rates.min()):,}"  if len(rates) else "N/A"
            r_max  = f"₹ {int(rates.max()):,}"  if len(rates) else "N/A"
            r_avg  = f"₹ {int(rates.mean()):,}" if len(rates) else "N/A"

            st.markdown("<div style='padding:28px 40px 0 40px;'>", unsafe_allow_html=True)
            mc1, mc2, mc3, mc4 = st.columns(4)

            card_style = "border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.45);"
            body_style = ("background:rgba(10,18,38,0.88);padding:18px 18px 20px 18px;"
                          "border:1px solid rgba(255,255,255,0.08);border-top:none;"
                          "border-radius:0 0 16px 16px;")
            val_style = "font-size:36px;font-weight:900;color:white;line-height:1;margin-bottom:4px;"
            sub_style = "font-size:12px;color:rgba(255,255,255,0.4);font-weight:500;"

            def hdr(bg, icon, label):
                return (f'<div style="background:{bg};padding:11px 18px;font-size:11px;'
                        f'font-weight:800;letter-spacing:1.8px;text-transform:uppercase;color:white;">'
                        f'{icon}&nbsp;{label}</div>')

            with mc1:
                st.markdown(f'<div style="{card_style}">' + hdr("linear-gradient(135deg,#6c4ff7,#a855f7)","📋","Records Found") +
                    f'<div style="{body_style}"><div style="{val_style}">{count}</div><div style="{sub_style}">matching shipments</div></div></div>',
                    unsafe_allow_html=True)
            with mc2:
                st.markdown(f'<div style="{card_style}">' + hdr("linear-gradient(135deg,#0ea5e9,#22d3ee)","💰","Min Rate") +
                    f'<div style="{body_style}"><div style="{val_style}">{r_min}</div><div style="{sub_style}">lowest freight rate</div></div></div>',
                    unsafe_allow_html=True)
            with mc3:
                st.markdown(f'<div style="{card_style}">' + hdr("linear-gradient(135deg,#f43f5e,#fb923c)","💰","Max Rate") +
                    f'<div style="{body_style}"><div style="{val_style}">{r_max}</div><div style="{sub_style}">highest freight rate</div></div></div>',
                    unsafe_allow_html=True)
            with mc4:
                st.markdown(f'<div style="{card_style}">' + hdr("linear-gradient(135deg,#10b981,#34d399)","📈","Avg Rate") +
                    f'<div style="{body_style}"><div style="{val_style}">{r_avg}</div><div style="{sub_style}">average freight rate</div></div></div>',
                    unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
            cols = [c for c in ["ID","LOADING PARTY","LOADING LOCATION",
                                 "DELIVERY LOCATION","FROM RATE","TO RATE","DATE"]
                    if c in filtered.columns]
            st.dataframe(filtered[cols].reset_index(drop=True), use_container_width=True)
            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Results", csv, "freight_results.csv", "text/csv")
            st.markdown('</div>', unsafe_allow_html=True)

# ── DATA VIEW ──────────────────────────────────────────
elif page == "data":
    st.markdown('<div class="page-title">🗂️ Data View</div>', unsafe_allow_html=True)
    st.markdown("<div style='padding:20px 40px'>", unsafe_allow_html=True)
    c1, c2 = st.columns([4, 1])
    with c1: st.info(f"Showing all **{len(df):,}** records")
    with c2:
        csv_all = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export CSV", csv_all, "freight_master.csv", "text/csv")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── ABOUT ──────────────────────────────────────────────
elif page == "about":
    st.markdown('<div class="page-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style='padding:30px 40px; max-width:720px;'>
      <div style='background:rgba(13,22,42,0.85);border:1px solid rgba(255,255,255,0.1);
                  border-radius:22px;padding:38px;backdrop-filter:blur(20px);'>
        <h3 style='color:white;font-size:24px;font-weight:800;margin:0 0 14px 0;'>🚚 Freight Finder System</h3>
        <p style='color:rgba(255,255,255,0.65);font-size:16px;line-height:1.8;margin:0 0 24px 0;'>
          An internal freight rate lookup tool — search delivery locations and loading parties instantly.
        </p>
        <hr style='border-color:rgba(255,255,255,0.08);margin-bottom:24px;'/>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:16px;'>
          <div style='background:rgba(255,255,255,0.05);border-radius:14px;padding:18px;'>
            <div style='color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;'>Total Records</div>
            <div style='color:white;font-size:28px;font-weight:800;margin-top:6px;'>{len(df):,}</div>
          </div>
          <div style='background:rgba(255,255,255,0.05);border-radius:14px;padding:18px;'>
            <div style='color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;'>Loading Parties</div>
            <div style='color:white;font-size:28px;font-weight:800;margin-top:6px;'>{df["LOADING PARTY"].nunique()}</div>
          </div>
          <div style='background:rgba(255,255,255,0.05);border-radius:14px;padding:18px;'>
            <div style='color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;'>Delivery Locations</div>
            <div style='color:white;font-size:28px;font-weight:800;margin-top:6px;'>{df["DELIVERY LOCATION"].nunique()}</div>
          </div>
          <div style='background:rgba(255,255,255,0.05);border-radius:14px;padding:18px;'>
            <div style='color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;'>Version</div>
            <div style='color:white;font-size:28px;font-weight:800;margin-top:6px;'>v2.0</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)