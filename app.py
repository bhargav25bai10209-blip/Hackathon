"""
PashuVisionAI | Cattle Identification
A single-file Streamlit application with a glassmorphism, React/Tailwind-inspired UI.
Run with: streamlit run app.py
"""

import random
import string
import base64
from datetime import datetime

import streamlit as st

# ──────────────────────────────────────────────────────────────────────────
# header img
# ──────────────────────────────────────────────────────────────────────

def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
hero_image = get_image_base64("assets/cattle-hero.jpg")
# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PashuVisionAI | Cattle Identification",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES (Glassmorphism / Tailwind-inspired design system)
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --bg-slate: #F8FAFC;
        --navy: #002B49;
        --forest: #1E5631;
        --saffron: #FF9933;
        --border-soft: #E2E8F0;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background: var(--bg-slate);
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }}

    /* ---------- Micro label ---------- */
    .micro-label {{
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #64748B;
    }}

    .saffron-tag {{
        display: inline-block;
        background: linear-gradient(135deg, var(--saffron), #FFB366);
        color: #ffffff;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 999px;
        box-shadow: 0 4px 14px rgba(255, 153, 51, 0.35);
        margin-bottom: 14px;
    }}

    /* ---------- Hero ---------- */
    .hero {{
        position: relative;
        min-height: 360px;
        border-radius: 22px;
        overflow: hidden;
        margin-bottom: 28px;

        background-image:
            linear-gradient(
                90deg,
                rgba(0, 43, 73, 0.62),
                rgba(0, 43, 73, 0.38),
                rgba(0, 0, 0, 0.15)
            ),
            url("data:image/jpeg;base64,{hero_image}");

        background-size: cover;
        background-position: center;

        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
        max-width: 760px;
        padding: 50px 30px;
        color: white;
    }}

    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 14px 0 12px;
        letter-spacing: -0.03em;
    }}

    .hero-subtitle {{
        font-size: 1rem;
        line-height: 1.6;
        max-width: 650px;
        margin: 0 auto;
        color: rgba(255,255,255,0.88);
    }}

    /* ---------- Old header styles ---------- */
    .main-heading {{
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--navy);
        line-height: 1.15;
        margin: 4px 0 10px 0;
    }}

    .gradient-text {{
        background: linear-gradient(90deg, var(--forest), var(--saffron));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .header-desc {{
        color: #475569;
        font-size: 0.95rem;
        max-width: 780px;
        line-height: 1.55;
        margin-bottom: 24px;
    }}

    /* ---------- Glass card ---------- */
    .glass-card {{
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid var(--border-soft);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 30px rgba(2, 32, 71, 0.06);
        padding: 20px 22px;
        margin-bottom: 18px;
    }}

    /* ---------- Colorful capture card ---------- */
    .capture-card {{
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(255, 153, 51, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(30, 86, 49, 0.10),
                transparent 30%
            ),
            linear-gradient(135deg, #FFFFFF, #F4FAF6);

        border: 1px solid #CFE3D5;
        box-shadow: 0 12px 35px rgba(30, 86, 49, 0.10);
    }}

    /* ---------- Metric grid ---------- */
    .metric-card {{
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid var(--border-soft);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 24px rgba(2, 32, 71, 0.05);
        padding: 18px 20px;
        text-align: left;
        transition: transform 0.15s ease;
    }}

    .metric-value {{
        font-size: 1.9rem;
        font-weight: 800;
        color: var(--navy);
        margin-top: 4px;
    }}

    .metric-icon {{
        font-size: 1.2rem;
    }}

    /* ---------- Section header ---------- */
    .section-step {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }}

    .step-badge {{
        background: var(--navy);
        color: white;
        font-weight: 800;
        font-size: 0.75rem;
        width: 26px;
        height: 26px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .step-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--navy);
    }}

    /* ---------- Badges ---------- */
    .badge-warning {{
        display: inline-block;
        background: #FFF7E6;
        color: #92600A;
        border: 1px solid #FFD98A;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 10px;
        margin-top: 8px;
    }}

    .badge-ok {{
        display: inline-block;
        background: #ECFDF3;
        color: var(--forest);
        border: 1px solid #B7E4C7;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 10px;
        margin-top: 8px;
    }}

    /* ---------- Empty state ---------- */
    .empty-state {{
        text-align: center;
        padding: 26px 20px;
        border-radius: 14px;
        background: linear-gradient(135deg, #F8FFFA, #FFF9F2);
        border: 1px dashed #C9DCCF;
    }}

    .empty-icon {{
        font-size: 1.8rem;
        margin-bottom: 8px;
    }}

    .empty-title {{
        color: var(--navy);
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 5px;
    }}

    .empty-desc {{
        color: #64748B;
        font-size: 0.78rem;
        line-height: 1.5;
    }}

    /* ---------- Feature tag ---------- */
    .feature-tag {{
        display: inline-block;
        background: #F0FDF4;
        color: var(--forest);
        border: 1px solid #C7EDD3;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 10px;
        margin: 3px 4px 3px 0;
    }}

    /* ---------- Breed profile ---------- */
    .breed-profile {{
        background: linear-gradient(145deg, #FFF7EA, #F0FDF4);
        border: 1px solid #D8E5D9;
        border-radius: 14px;
        padding: 22px 14px;
        text-align: center;
    }}

    .breed-animal {{
        font-size: 2.5rem;
        margin-bottom: 6px;
    }}

    .breed-result-label {{
        color: #64748B;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.12em;
    }}

    .breed-result-name {{
        color: var(--forest);
        font-size: 1.45rem;
        font-weight: 800;
        margin: 3px 0 5px;
    }}

    /* ---------- Breed prediction bar ---------- */
    .breed-row {{
        margin-bottom: 14px;
    }}

    .breed-name-row {{
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--navy);
        margin-bottom: 5px;
    }}

    .progress-track {{
        width: 100%;
        height: 10px;
        background: #EDF2F7;
        border-radius: 999px;
        overflow: hidden;
    }}

    .progress-fill {{
        height: 100%;
        border-radius: 999px;
    }}

    /* ---------- Roadmap ---------- */
    .roadmap-card {{
        background: rgba(255, 255, 255, 0.9);
        border: 1px dashed var(--border-soft);
        border-radius: 16px;
        padding: 16px 18px;
        text-align: center;
        height: 100%;
    }}

    .roadmap-icon {{
        font-size: 1.6rem;
        margin-bottom: 6px;
    }}

    .roadmap-title {{
        font-weight: 700;
        color: var(--navy);
        font-size: 0.88rem;
        margin-bottom: 4px;
    }}

    .roadmap-desc {{
        font-size: 0.75rem;
        color: #64748B;
    }}

    /* ---------- Divider ---------- */
    hr.soft-divider {{
        border: none;
        border-top: 1px solid var(--border-soft);
        margin: 28px 0 20px 0;
    }}

    /* ---------- Buttons ---------- */
    .stButton>button {{
        border-radius: 12px;
        font-weight: 700;
        border: none;
        padding: 0.55rem 1.2rem;
    }}

    div[data-testid="stFormSubmitButton"] button {{
        border-radius: 12px;
        font-weight: 700;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────────────────────────────────
if "tag_id" not in st.session_state:
    st.session_state.tag_id = f"IND-1200-{random.randint(1000, 9999)}"
if "worker_id" not in st.session_state:
    st.session_state.worker_id = "DAHD-EN-2291"
if "predictions" not in st.session_state:
    st.session_state.predictions = None
if "entries" not in st.session_state:
    st.session_state.entries = []

INDIAN_STATES = [
    "Uttar Pradesh", "Rajasthan", "Punjab", "Haryana", "Gujarat", "Maharashtra",
    "Madhya Pradesh", "Bihar", "West Bengal", "Karnataka", "Tamil Nadu",
    "Andhra Pradesh", "Telangana", "Odisha", "Assam", "Kerala",
]

BREED_LIBRARY = [
    ("Gir", "#FF9933"), ("Sahiwal", "#1E5631"), ("Tharparkar", "#002B49"),
    ("Red Sindhi", "#C2410C"), ("Kankrej", "#0F766E"), ("Ongole", "#7C3AED"),
    ("Murrah (Buffalo)", "#B91C1C"), ("Rathi", "#0369A1"),
]

FEATURE_POOL = [
    "Convex forehead", "Pendulous ears", "Prominent hump", "Loose dewlap",
    "Light grey-white coat", "Curved horns", "Compact body frame",
    "Distinct facial markings",
]


def generate_predictions():
    breeds = random.sample(BREED_LIBRARY, 3)
    top = random.uniform(58, 92)
    second = top - random.uniform(4, 30)
    third = second - random.uniform(3, 15)
    scores = [round(max(top, 1), 1), round(max(second, 1), 1), round(max(third, 1), 1)]
    scores = sorted(scores, reverse=True)
    return list(zip([b[0] for b in breeds], [b[1] for b in breeds], scores))


# ──────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<span class="saffron-tag">PASHUVISIONAI</span>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero">
        <div class="hero-content">

            <div class="saffron-tag">
                PASHUVISIONAI
            </div>

            <div class="hero-title">
                See the animal.<br>
                <span style="color:#FFB45C;">Know the breed.</span>
            </div>

            <div class="hero-subtitle">
                Capture or upload a cattle photograph and let
                PashuVisionAI identify the animal type, likely breed,
                confidence and regional information.
            </div>

        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# STEP 1 — FIELD METADATA
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="section-step">
        <div class="step-badge">1</div>
        <div class="step-title">Observation Location</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)    
    with c1:
        st.markdown('<div class="micro-label">State</div>', unsafe_allow_html=True)
        state = st.selectbox("State", INDIAN_STATES, label_visibility="collapsed")
    with c2:
        st.markdown('<div class="micro-label">District</div>', unsafe_allow_html=True)
        district = st.text_input("District", placeholder="e.g. Bharuch", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# STEP 2 — DUAL CAPTURE
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="section-step">
        <div class="step-badge">2</div>
        <div class="step-title">Dual Capture</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="glass-card capture-card">', unsafe_allow_html=True)
    tab_upload, tab_camera = st.tabs(["📁 Upload File", "📷 Live Camera Capture"])
    captured_image = None
    with tab_upload:
        uploaded = st.file_uploader(
            "Upload an animal photo", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
        )
        if uploaded is not None:
            captured_image = uploaded
            st.image(uploaded, caption="Uploaded field photo", width=280)
    with tab_camera:
        cam_photo = st.camera_input("Capture live photo", label_visibility="collapsed")
        if cam_photo is not None:
            captured_image = cam_photo

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("🔍 Analyze Breed Characteristics", type="primary", use_container_width=False)
    if analyze_clicked:
        if captured_image is None:
            st.warning("Please upload a photo or capture one via camera before analyzing.")
        else:
            with st.spinner("Running on-device breed classifier…"):
                st.session_state.predictions = generate_predictions()
                st.session_state.features = random.sample(FEATURE_POOL, 4)
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# STEP 3 — PREDICTIONS & CONFIDENCE
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="section-step">
        <div class="step-badge">3</div>
        <div class="step-title">AI Identification</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.session_state.predictions is None:
        st.markdown(
            '<div class="micro-label">Run analysis above to generate a breed short-list.</div>',
            unsafe_allow_html=True,
        )
    else:
        preds = st.session_state.predictions
        bars_html = ""
        colors = ["#1E5631", "#FF9933", "#002B49"]
        for (breed, _, score), color in zip(preds, colors):
            bars_html += f"""
            <div class="breed-row">
                <div class="breed-name-row"><span>{breed}</span><span>{score}%</span></div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:{score}%; background:{color};"></div>
                </div>
            </div>
            """
        st.markdown(bars_html, unsafe_allow_html=True)

        gap = preds[0][2] - preds[1][2]
        if gap < 15:
            st.markdown(
                f'<span class="badge-warning">⚠️ Borderline case — top gap only {gap:.1f} pts. Recommend manual review.</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span class="badge-ok">✓ Confident prediction — top gap {gap:.1f} pts.</span>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# STEP 4 — REFERENCE MATCH
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="section-step">
        <div class="step-badge">4</div>
        <div class="step-title">Reference Match</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.session_state.predictions is None:
       st.markdown(
    """
    <div class="empty-state">
        <div class="empty-icon">📋</div>
        <div class="empty-title">Reference comparison pending</div>
        <div class="empty-desc">
            Detected features and the matching standard breed plate
            will appear here after AI analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
    
    else:
        rc1, rc2 = st.columns([1.3, 1])
        with rc1:
            st.markdown('<div class="micro-label" style="margin-bottom:8px;">Detected feature tags</div>', unsafe_allow_html=True)
            tags_html = "".join(
                f'<span class="feature-tag">✓ {feat}</span>' for feat in st.session_state.features
            )
            st.markdown(tags_html, unsafe_allow_html=True)
        with rc2:
            st.markdown('<div class="micro-label" style="margin-bottom:8px;">Standard breed plate</div>', unsafe_allow_html=True)
            top_breed = st.session_state.predictions[0][0]
            st.markdown(
                f"""
                <div style="background:#F1F5F9; border:1px solid var(--border-soft);
                            border-radius:12px; padding:26px 14px; text-align:center;">
                    <div style="font-size:2rem;">🐄</div>
                    <div style="font-weight:700; color:var(--navy); margin-top:6px;">{top_breed}</div>
                    <div class="micro-label">Reference plate — DAHD registry</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-step">
        <div class="step-badge">5</div>
        <div class="step-title">Confirmation</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    breed_options = (
        [b for b, _, _ in st.session_state.predictions] + ["Other / Not Listed"]
        if st.session_state.predictions
        else [b[0] for b in BREED_LIBRARY] + ["Other / Not Listed"]
    )
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        st.markdown('<div class="micro-label">Confirmed breed</div>', unsafe_allow_html=True)
        confirmed_breed = st.selectbox("Confirmed breed", breed_options, label_visibility="collapsed")
    with cc2:
        st.markdown('<div class="micro-label">Observation notes</div>', unsafe_allow_html=True)
        notes = st.text_area(
            "Observation notes", placeholder="Any additional field observations…",
            label_visibility="collapsed", height=68,
        )

    if st.button("✅ Confirm & Save Entry", type="primary"):
        if not district.strip():
            st.warning("Please enter a district before saving the entry.")
        else:
            entry = {
                "Tag ID": st.session_state.tag_id,
                "Worker": st.session_state.worker_id,
                "State": state,
                "District": district,
                "Confirmed Breed": confirmed_breed,
                "Top AI Guess": st.session_state.predictions[0][0] if st.session_state.predictions else "—",
                "Confidence": f"{st.session_state.predictions[0][2]}%" if st.session_state.predictions else "—",
                "Notes": notes,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            st.session_state.entries.append(entry)
            st.success(f"Entry saved for {st.session_state.tag_id}.")
            # Prepare a fresh tag for the next animal
            st.session_state.tag_id = f"IND-1200-{random.randint(1000, 9999)}"
            st.session_state.predictions = None
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# SESSION SUMMARY TABLE
# ──────────────────────────────────────────────────────────────────────────
if st.session_state.entries:
    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-step">
            <div class="step-badge">📊</div>
            <div class="step-title">Session Summary</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.dataframe(st.session_state.entries, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# FOOTER — UPCOMING BACKEND MODULES ROADMAP
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
st.markdown('<div class="micro-label" style="margin-bottom:12px;">Upcoming backend modules</div>', unsafe_allow_html=True)

roadmap_items = [
    ("🏷️", "Ear Tag OCR", "Automated tag-number extraction from field photos."),
    ("💉", "Vaccine Verification", "Cross-check vaccination records against the national registry."),
    ("🛰️", "Geospatial Analytics", "District and block-level heat-maps of breed distribution."),
    ("🔄", "Offline Sync Queue", "Queue entries captured without connectivity for later sync."),
]

r1, r2, r3, r4 = st.columns(4)
for col, (icon, title, desc) in zip([r1, r2, r3, r4], roadmap_items):
    with col:
        st.markdown(
            f"""
            <div class="roadmap-card">
                <div class="roadmap-icon">{icon}</div>
                <div class="roadmap-title">{title}</div>
                <div class="roadmap-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div style="text-align:center; margin-top:24px; color:#94A3B8; font-size:0.72rem;">
        Bharat Pashudhan · AI Field Entry Module · Department of Animal Husbandry &amp; Dairying (DAHD)
    </div>
    """,
    unsafe_allow_html=True,
)
