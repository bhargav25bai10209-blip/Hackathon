"""
Bharat Pashudhan — AI Field Entry Module
"""

import random
import time
from datetime import datetime

import streamlit as st
from PIL import Image

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Bharat Pashudhan — AI Field Entry",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# DESIGN TOKENS
# ----------------------------------------------------------------------------
FOREST_GREEN = "#1E5631"
NAVY_PRIMARY = "#0A2540"
SAFFRON_GOLD = "#FF9933"
CARD_BG = "#FFFFFF"
BORDER_COLOR = "#E2E8F0"
TEXT_MAIN = "#0F172A"

# ----------------------------------------------------------------------------
# REFINED CUSTOM CSS (FIXES DARK MODE & FORM INPUTS)
# --------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Force font family across all elements */
        html, body, [class*="css"], .stApp {{
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
            background-color: #F8FAFC !important;
        }}

        /* Constrain view width to native mobile app column */
        .main > div {{
            max-width: 460px;
            margin: 0 auto;
            padding: 0.5rem 0.8rem;
        }}

        /* Fix native input styling to prevent dark mode conflict */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div, 
        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border-radius: 10px !important;
            border: 1px solid #CBD5E1 !important;
        }}

        /* Government Top Header */
        .gov-header-card {{
            background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
            border-radius: 16px;
            padding: 16px;
            color: #FFFFFF;
            margin-bottom: 16px;
            box-shadow: 0 10px 25px -5px rgba(10, 37, 64, 0.25);
            position: relative;
            overflow: hidden;
        }}
        
        .gov-header-card::after {{
            content: "";
            position: absolute;
            top: -20px;
            right: -20px;
            width: 90px;
            height: 90px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 50%;
        }}

        /* Badge Styling */
        .step-heading {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            font-weight: 700;
            color: #0A2540;
            margin: 16px 0 10px 0;
        }}
        .step-number {{
            background: #0A2540;
            color: #FFFFFF;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
        }}

        /* Custom Card Container */
        .ui-card {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}

        /* Metadata Pill Display */
        .meta-pill {{
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #334155;
        }}

        /* Hide Streamlit default blank wrapper gaps */
        .stMarkdown:empty {{ display: none; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# MOCK PREDICTION DATA & HIGH-QUALITY REFERENCE IMAGE LINKS
# -------------------------------------------------------------------------
# Note: To use local images, replace these URLs with local relative paths (e.g., 'assets/gir.jpg')
BREED_DATA = {
    "Gir": {
        "traits": ["Convex forehead", "Long pendulous ears", "Prominent dewlap", "Speckled reddish coat"],
        "ref_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Gir_bull.jpg/320px-Gir_bull.jpg",
    },
    "Sahiwal": {
        "traits": ["Loose skin / Dewlap", "Reddish-brown color", "Short stumpy horns", "Dull passive eyes"],
        "ref_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Sahiwal_cow.jpg/320px-Sahiwal_cow.jpg",
    },
    "Tharparkar": {
        "traits": ["White/Grey lyre coat", "Medium build", "Lyre-shaped horns", "Black tail switch"],
        "ref_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Tharparkar_breed.jpg/320px-Tharparkar_breed.jpg",
    },
    "Murrah (Buffalo)": {
        "traits": ["Tightly curled horns", "Jet black coat", "Large well-developed udder", "Short compact neck"],
        "ref_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Murrah_buffalo.jpg/320px-Murrah_buffalo.jpg",
    },
    "Red Sindhi": {
        "traits": ["Deep red coat", "Broad forehead", "Short thick horns", "Compact humped frame"],
        "ref_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Red_Sindhi_Bull.jpg/320px-Red_Sindhi_Bull.jpg",
    },
    "Jaffarabadi (Buffalo)": {
        "traits": ["Massive drooping horns", "Broad heavy forehead", "Prominent dewlap", "Heavy build frame"],
        "ref_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Jaffrabadi_buffalo.jpg/320px-Jaffrabadi_buffalo.jpg",
    },
}


def predict_breed(image):
    time.sleep(0.5)
    all_breeds = list(BREED_DATA.keys())
    random.seed(hash(image.size) % (10**6))

    top = random.choice(all_breeds)
    remaining = [b for b in all_breeds if b != top]
    second, third = random.sample(remaining, 2)

    hard_case = random.random() < 0.4
    if hard_case:
        c1 = round(random.uniform(0.45, 0.54), 2)
        c2 = round(c1 - random.uniform(0.02, 0.08), 2)
    else:
        c1 = round(random.uniform(0.70, 0.92), 2)
        c2 = round(random.uniform(0.06, 0.18), 2)
    c3 = round(max(0.03, 1 - c1 - c2), 2)

    return [
        {"breed": top, "confidence": c1, "traits": BREED_DATA[top]["traits"], "ref_url": BREED_DATA[top]["ref_url"]},
        {"breed": second, "confidence": c2, "traits": BREED_DATA[second]["traits"], "ref_url": BREED_DATA[second]["ref_url"]},
        {"breed": third, "confidence": c3, "traits": BREED_DATA[third]["traits"], "ref_url": BREED_DATA[third]["ref_url"]},
    ]


# ----------------------------------------------------------------------------
# HEADER & EMBLEM
# ---------------------------------------------------------------------------
st.markdown('<div class="tricolor-bar"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="gov-header">
        <div class="emblem-row">
            <div class="emblem-badge">
                <svg class="emblem-svg" viewBox="0 0 24 24">
                    <path d="M12 2L4 5v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V5l-8-3zm0 4a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm0 14.3c-2.8-1.02-5.5-4.85-5.95-8.5 1.5.6 3.5 1 5.95 1 2.45 0 4.45-.4 5.95-1-.45 3.65-3.15 7.48-5.95 8.5z"/>
                </svg>
            </div>
            <div>
                <h1>Bharat Pashudhan</h1>
                <div class="subtitle">DAHD — National AI Field Entry Portal</div>
            </div>
        </div>
        <div style="margin-top:12px; display:flex; justify-content:space-between; align-items:center;">
            <span class="status-pill">🟢 Network: Sync Active</span>
            <span style="font-size:0.72rem; opacity:0.85; font-weight:600;">v1.42-field</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "predictions" not in st.session_state:
    st.session_state.predictions = None
if "saved_log" not in st.session_state:
    st.session_state.saved_log = []

# ----------------------------------------------------------------------------
# STEP 1 — FIELD METADATA
# ---------------------------------------------------------------------------
st.markdown('<div class="step-label"><span class="step-badge">1</span> Field Metadata</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="field-card">', unsafe_allow_html=True)
    ear_tag = f"IND-1200-{random.randint(1000, 9999)}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="meta-badge">Tag ID: <b>{ear_tag}</b></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="meta-badge">Worker: <b>DAHD-EN-2291</b></div>', unsafe_allow_html=True)

    state = st.selectbox("State", ["Madhya Pradesh", "Gujarat", "Punjab", "Rajasthan", "Uttar Pradesh", "Haryana"])
    district = st.text_input("District / Tehsil", value="Bhopal")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STEP 2 — PHOTO CAPTURE
# ----------------------------------------------------------------------------
st.markdown('<div class="step-label"><span class="step-badge">2</span> Capture Animal Photo</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="field-card">', unsafe_allow_html=True)
    tab_upload, tab_camera = st.tabs(["📁 Upload File", "📷 Use Camera"])

    image = None
    with tab_upload:
        uploaded_file = st.file_uploader("Choose a photo from device", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded_file:
            image = Image.open(uploaded_file)

    with tab_camera:
        camera_file = st.camera_input("Take a live photo", label_visibility="collapsed")
        if camera_file:
            image = Image.open(camera_file)

    if image is not None:
        st.image(image, caption="Captured Field Photo", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

if image is not None:
    if st.button("🔍 Analyze Breed Characteristics", type="primary"):
        with st.spinner("Extracting facial & hump geometry..."):
            st.session_state.predictions = predict_breed(image)

# ----------------------------------------------------------------------------
# STEP 3 — PREDICTIONS & REFERENCE COMPARISON
# ----------------------------------------------------------------------------
if st.session_state.predictions:
    preds = st.session_state.predictions

    st.markdown('<div class="step-label"><span class="step-badge">3</span> AI Recommendations (Top-3)</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="field-card">', unsafe_allow_html=True)

        top_conf = preds[0]["confidence"]
        second_conf = preds[1]["confidence"]
        if (top_conf - second_conf) < 0.15:
            st.markdown(
                '<div class="warn-badge">⚠️ Borderline confidence gap (<15%). Visually similar breeds detected.</div>',
                unsafe_allow_html=True,
            )

        for i, p in enumerate(preds):
            rank_class = "pred-rank1" if i == 0 else "pred-rank-other"
            bar_class = "bar-fill-1" if i == 0 else "bar-fill-other"
            pct = int(p["confidence"] * 100)
            st.markdown(
                f"""
                <div class="pred-row">
                    <div class="pred-top-line">
                        <span class="{rank_class}">#{i+1} {p['breed']}</span>
                        <span class="{rank_class}">{pct}%</span>
                    </div>
                    <div class="bar-track">
                        <div class="{bar_class}" style="width:{pct}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # --- STEP 4: VISUAL EXPLAINER & REFERENCE BREED COMPARE ---
    st.markdown('<div class="step-label"><span class="step-badge">4</span> Feature Traits & Reference Match</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="field-card">', unsafe_allow_html=True)
        st.markdown(f"**Detected traits driving {preds[0]['breed']} prediction:**")
        tags_html = "".join([f'<span class="trait-tag">✓ {t}</span>' for t in preds[0]["traits"]])
        st.markdown(tags_html, unsafe_allow_html=True)

        st.divider()
        st.caption(f"📷 **Standard Breed Reference Photo ({preds[0]['breed']}):**")
        
        # Display image directly with fallback error handling
        try:
            st.image(preds[0]["ref_url"], caption=f"Standard Breed Reference — {preds[0]['breed']}", use_container_width=True)
        except Exception:
            st.warning(f"Could not load reference image for {preds[0]['breed']}.")
            
        st.markdown("</div>", unsafe_allow_html=True)

    # --- STEP 5: CONFIRMATION & LOGGING ---
    st.markdown('<div class="step-label"><span class="step-badge">5</span> Enumerator Confirmation</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="field-card">', unsafe_allow_html=True)
        breed_options = [p["breed"] for p in preds] + ["Other (manual entry)"]
        final_breed = st.selectbox("Confirm breed to log into Bharat Pashudhan record:", breed_options, index=0)
        
        notes = st.text_input("Additional observations / notes (optional)")

        if st.button("✅ Confirm & Save Entry to Record", type="primary"):
            st.session_state.saved_log.append(
                {
                    "ear_tag": ear_tag,
                    "state": state,
                    "district": district,
                    "breed": final_breed,
                    "ai_top_suggestion": preds[0]["breed"],
                    "ai_confidence": f"{int(preds[0]['confidence']*100)}%",
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                }
            )
            st.markdown(
                f"""
                <div class="confirm-card">
                    ✅ <b>Pashudhan Record Logged!</b><br>
                    Tag ID <b>{ear_tag}</b> saved as <b>{final_breed}</b> for {district}, {state}.
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# ROADMAP PLACEHOLDERS (FUTURE BACKEND INTEGRATIONS)
# ---------------------------------------------------------------------------
st.markdown('<div class="step-label">🚀 Upcoming Backend Modules</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="roadmap-grid">
        <div class="roadmap-card">
            <span class="roadmap-badge">Phase 2</span>
            <b>🏷️ Ear Tag OCR</b>
            Auto-extract 12-digit ear tag IDs from photo scan.
        </div>
        <div class="roadmap-card">
            <span class="roadmap-badge">Phase 2</span>
            <b>💉 Vaccine Verify</b>
            Cross-reference FMD & Brucellosis logs instantly.
        </div>
        <div class="roadmap-card">
            <span class="roadmap-badge">Phase 3</span>
            <b>📊 Breed Map</b>
            Real-time geospatial breed population analytics.
        </div>
        <div class="roadmap-card">
            <span class="roadmap-badge">Phase 3</span>
            <b>🌐 Offline Sync</b>
            Queue local records without active cellular data.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION LOG SUMMARY
# ----------------------------------------------------------------------------
if st.session_state.saved_log:
    with st.expander(f"📋 Session Logged Entries ({len(st.session_state.saved_log)})"):
        st.table(st.session_state.saved_log)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="impact-footer">
        <b>Impact Note:</b> Manual breed misclassification in field logs currently leads to distorted genetic tracking for national breeding schemes. AI second-opinions reduce entry error without removing field judgment.
    </div>
    """,
    unsafe_allow_html=True,
)
