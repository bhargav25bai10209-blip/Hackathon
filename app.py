"""
Bharat Pashudhan — AI Field Entry Module
Hackathon prototype: AI-assisted breed identification as a "second opinion"
for field enumerators entering data into the national livestock database.

Run with: streamlit run app.py
"""

import random
import time
from datetime import datetime

import streamlit as st
from PIL import Image

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Bharat Pashudhan — AI Field Entry",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# DESIGN TOKENS
# ----------------------------------------------------------------------------
FOREST_GREEN = "#1E5631"
NAVY = "#002B49"
SAFFRON = "#FF9933"
SAGE_BG = "#F4F7F4"
CARD_BG = "rgba(255, 255, 255, 0.94)"
BORDER_COLOR = "#D4E0D5"
TEXT_MUTED = "#4A5D4E"

# ----------------------------------------------------------------------------
# CUSTOM CSS (WITH SUBTLE BACKGROUND WATERMARK & GLASSMORPHISM)
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        /* ---- App Shell & Background Image Overlay ---- */
        .main > div {{
            max-width: 480px;
            margin: 0 auto;
            padding-top: 0.2rem;
        }}
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        }}
        
        /* Subtle cattle watermark background (Low opacity ~6%) */
        .stApp {{
            background-color: {SAGE_BG};
            background-image: 
                linear-gradient(rgba(244, 247, 244, 0.94), rgba(244, 247, 244, 0.94)),
                url('https://images.unsplash.com/photo-1545468843-279d2bf1694f?auto=format&fit=crop&w=1200&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* ---- Tricolor Accent Top Bar ---- */
        .tricolor-bar {{
            height: 5px;
            width: 100%;
            background: linear-gradient(90deg, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%);
            border-radius: 6px 6px 0 0;
            margin-bottom: -5px;
        }}

        /* ---- Enhanced Government Header Banner ---- */
        .gov-header {{
            background: linear-gradient(135deg, {NAVY} 0%, #0D47A1 100%);
            border-radius: 0 0 16px 16px;
            padding: 18px 20px;
            color: white;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0, 43, 73, 0.18);
        }}
        .gov-header .emblem-row {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .gov-header .emblem-badge {{
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .gov-header .emblem-svg {{
            width: 32px;
            height: 32px;
            fill: #FFD700;
        }}
        .gov-header h1 {{
            font-size: 1.15rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0.3px;
            color: #FFFFFF;
        }}
        .gov-header .subtitle {{
            font-size: 0.74rem;
            color: #E0EAE2;
            margin-top: 2px;
            font-weight: 500;
        }}
        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 999px;
            padding: 3px 10px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #E8F5E9;
        }}

        /* ---- Step Label & Badge ---- */
        .step-label {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.84rem;
            font-weight: 700;
            color: {NAVY};
            margin: 18px 0 8px 0;
            letter-spacing: 0.2px;
        }}
        .step-badge {{
            background: {NAVY};
            color: white;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.72rem;
            font-weight: 700;
        }}

        /* ---- Glassmorphism Card Styling ---- */
        .field-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER_COLOR};
            backdrop-filter: blur(8px);
            border-radius: 14px;
            padding: 16px 18px;
            margin-bottom: 12px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
        }}

        /* ---- Metadata Badges ---- */
        .meta-badge {{
            background: #F0F5F1;
            border: 1px solid #D1E0D3;
            border-radius: 8px;
            padding: 7px 10px;
            font-size: 0.76rem;
            color: {NAVY};
            margin-bottom: 6px;
        }}
        .meta-badge b {{ color: #112817; }}

        /* ---- Predictions Bars ---- */
        .pred-row {{
            margin-bottom: 12px;
        }}
        .pred-row .pred-top-line {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }}
        .pred-rank1 {{
            font-weight: 700;
            color: {FOREST_GREEN};
        }}
        .pred-rank-other {{
            font-weight: 600;
            color: {NAVY};
        }}
        .bar-track {{
            width: 100%;
            height: 10px;
            background: #E5EBE5;
            border-radius: 6px;
            overflow: hidden;
        }}
        .bar-fill-1 {{
            height: 100%;
            background: linear-gradient(90deg, {FOREST_GREEN}, #2E7D32);
            border-radius: 6px;
        }}
        .bar-fill-other {{
            height: 100%;
            background: {NAVY};
            opacity: 0.55;
            border-radius: 6px;
        }}

        /* ---- Warning & Trait Badges ---- */
        .warn-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #FFF8E1;
            border: 1px solid {SAFFRON};
            color: #795548;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        .trait-tag {{
            display: inline-block;
            background: #E8F5E9;
            color: {FOREST_GREEN};
            border: 1px solid #C8E6C9;
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.74rem;
            font-weight: 600;
            margin: 0 4px 6px 0;
        }}

        /* ---- Roadmap Feature Grid Cards ---- */
        .roadmap-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 8px;
        }}
        .roadmap-card {{
            background: #FFFFFF;
            border: 1px dashed #B0C4B1;
            border-radius: 10px;
            padding: 10px;
            font-size: 0.72rem;
            color: {NAVY};
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .roadmap-card b {{
            font-size: 0.78rem;
            color: {FOREST_GREEN};
        }}
        .roadmap-badge {{
            align-self: flex-start;
            background: #ECEFF1;
            color: #546E7A;
            border-radius: 4px;
            padding: 1px 6px;
            font-size: 0.62rem;
            font-weight: 700;
            text-transform: uppercase;
        }}

        /* ---- Primary Buttons ---- */
        div.stButton > button {{
            width: 100%;
            border-radius: 10px;
            padding: 0.6rem 0.5rem;
            font-weight: 600;
            font-size: 0.88rem;
        }}
        div.stButton > button[kind="primary"] {{
            background-color: {FOREST_GREEN};
            border: none;
            color: white;
        }}

        /* ---- Impact Footer ---- */
        .impact-footer {{
            background: {CARD_BG};
            border-left: 4px solid {SAFFRON};
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 0.76rem;
            color: {TEXT_MUTED};
            margin-top: 18px;
            margin-bottom: 12px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        }}
        .impact-footer b {{ color: {NAVY}; }}

        /* ---- Confirmation toast ---- */
        .confirm-card {{
            background: #E8F5E9;
            border: 1px solid {FOREST_GREEN};
            border-radius: 10px;
            padding: 12px 14px;
            color: #1B5E20;
            font-size: 0.84rem;
            margin-top: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# MOCK PREDICTION DATA & HIGH-QUALITY REFERENCE IMAGE LINKS
# ----------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------
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


# SESSION STATE

if "predictions" not in st.session_state:
    st.session_state.predictions = None
if "saved_log" not in st.session_state:
    st.session_state.saved_log = []


# STEP 1 — FIELD METADATA

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


# STEP 2 — PHOTO CAPTURE

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

# STEP 3 — PREDICTIONS & REFERENCE COMPARISON

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

    # VISUAL EXPLAINER & REFERENCE BREED COMPARE
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

    # CONFIRMATION & LOGGING
    
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

# ROADMAP PLACEHOLDERS (FUTURE BACKEND INTEGRATIONS)

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

# SESSION LOG SUMMARY

if st.session_state.saved_log:
    with st.expander(f"📋 Session Logged Entries ({len(st.session_state.saved_log)})"):
        st.table(st.session_state.saved_log)

# FOOTER

st.markdown(
    """
    <div class="impact-footer">
        <b>Impact Note:</b> Manual breed misclassification in field logs currently leads to distorted genetic tracking for national breeding schemes. AI second-opinions reduce entry error without removing field judgment.
    </div>
    """,
    unsafe_allow_html=True,
)
