import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(layout="wide", page_title="Freight Finder", page_icon="🚚")
load_css()

@st.cache_data
def load_data():
    df = pd.read_excel("Freight_Master(1).xlsx").fillna("")
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

    # ── BIDIRECTIONAL CASCADING LOGIC ──
    # Step 1: Read current selections from session state (before rendering)
    current_party    = st.session_state.get(f"p_in_{rc}", "")
    current_delivery = st.session_state.get(f"d_in_{rc}", "")

    # Step 2: Filter party options based on delivery selection
    if current_delivery:
        matched_parties = (
            df[df["DELIVERY LOCATION"] == current_delivery]["LOADING PARTY"]
            .dropna().unique().tolist()
        )
        party_options  = [""] + sorted(matched_parties)
        party_help     = f"{len(matched_parties)} parties ship to this location"
    else:
        party_options  = [""] + sorted(df["LOADING PARTY"].dropna().unique().tolist())
        party_help     = "Select a Delivery Location to filter parties"

    # Step 3: Filter delivery options based on party selection
    if current_party:
        matched_deliveries = (
            df[df["LOADING PARTY"] == current_party]["DELIVERY LOCATION"]
            .dropna().unique().tolist()
        )
        delivery_options = [""] + sorted(matched_deliveries)
        delivery_help    = f"{len(matched_deliveries)} locations for this party"
    else:
        delivery_options = [""] + sorted(df["DELIVERY LOCATION"].dropna().unique().tolist())
        delivery_help    = "Select a Loading Party to filter locations"

    # Search Card — bidirectional cascading dropdowns
    with st.container(border=True):
        col1, col2 = st.columns([5, 5])
        with col1:
            party = st.selectbox(
                "Enter Loading Party",
                options=party_options,
                index=0,
                key=f"p_in_{rc}",
                help=party_help
            )
        with col2:
            delivery = st.selectbox(
                "Enter Delivery Location",
                options=delivery_options,
                index=0,
                key=f"d_in_{rc}",
                help=delivery_help
            )

        btn_col1, btn_col2, btn_col3 = st.columns([3, 2, 3])
        with btn_col2:
            search = st.button("🔍 SEARCH", use_container_width=True, key="search_btn")

    # Filter — exact match from selectbox
    filtered = df.copy()
    if delivery:
        filtered = filtered[filtered["DELIVERY LOCATION"] == delivery]
    if party:
        filtered = filtered[filtered["LOADING PARTY"] == party]

    # Results
    if search or delivery or party:
        if filtered.empty:
            st.markdown("<div style='padding:20px 40px'>", unsafe_allow_html=True)
            st.warning("❌ No records found. Try different search terms.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Only include real rates > 0 (removes blanks, zeros, adjustments)
            all_rates = pd.to_numeric(filtered["FROM RATE"], errors="coerce")
            rates = all_rates[all_rates > 0].dropna()

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
            # Show all columns except LOADING PARTY
            cols = [c for c in ["ID","LOADING LOCATION","DELIVERY LOCATION",
                                 "FROM RATE","TRANSPORTER NAME","PARTY NAME",
                                 "A/E","DATE"]
                    if c in filtered.columns]
            st.dataframe(filtered[cols].reset_index(drop=True), use_container_width=True)
            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Results", csv, "freight_results.csv", "text/csv")
            st.markdown('</div>', unsafe_allow_html=True)

# ── DATA VIEW ──────────────────────────────────────────
elif page == "data":
    st.markdown('<div class="page-title">🗂️ Data View</div>', unsafe_allow_html=True)
    st.markdown("<div style='padding:10px 40px 40px 40px;'>", unsafe_allow_html=True)

    # Top bar — record count + export button
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"""
        <div style="font-size:16px;font-weight:600;color:#4f8ef7;padding:12px 0 16px 0;">
            Showing all &nbsp;<span style="color:white;font-weight:800;">{len(df):,}</span>&nbsp; records
            &nbsp;·&nbsp;
            <span style="color:rgba(255,255,255,0.45);font-size:14px;">{len(df.columns)} columns</span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        csv_all = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export CSV", csv_all, "freight_master.csv", "text/csv")

    # Show ALL columns exactly as they are in the Excel — no hardcoding
    st.dataframe(
        df.reset_index(drop=True),
        use_container_width=True,
        height=600
    )
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
