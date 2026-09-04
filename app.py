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
NAVY = "#003366"
SAFFRON = "#E67E22"
SAGE_BG = "#EDF2ED"
CARD_BG = "#FFFFFF"
DANGER = "#B3261E"
TEXT_MUTED = "#5A6B5D"

# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        /* ---- App shell: constrain to a mobile-width column, centered ---- */
        .main > div {{
            max-width: 480px;
            margin: 0 auto;
            padding-top: 0.5rem;
        }}
        html, body, [class*="css"] {{
            font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        }}
        .stApp {{
            background-color: {SAGE_BG};
        }}

        /* ---- Government header banner ---- */
        .gov-header {{
            background: linear-gradient(135deg, {NAVY} 0%, {FOREST_GREEN} 100%);
            border-radius: 14px;
            padding: 18px 20px;
            color: white;
            margin-bottom: 18px;
            box-shadow: 0 2px 10px rgba(0, 51, 102, 0.25);
        }}
        .gov-header .emblem-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .gov-header h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.2px;
        }}
        .gov-header .subtitle {{
            font-size: 0.78rem;
            color: #DCE6DF;
            margin-top: 2px;
        }}
        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.35);
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.72rem;
            font-weight: 600;
            white-space: nowrap;
        }}

        /* ---- Section label ---- */
        .step-label {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
            font-weight: 700;
            color: {NAVY};
            margin: 22px 0 8px 0;
        }}
        .step-badge {{
            background: {NAVY};
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.68rem;
        }}

        /* ---- Card ---- */
        .field-card {{
            background: {CARD_BG};
            border: 1px solid #DCE3DC;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }}

        /* ---- Metadata badges ---- */
        .meta-badge {{
            background: {SAGE_BG};
            border: 1px solid #CBD8CC;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 0.78rem;
            color: {NAVY};
            margin-bottom: 6px;
        }}
        .meta-badge b {{ color: #14331e; }}

        /* ---- Prediction rows ---- */
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
            background: #E4EAE4;
            border-radius: 6px;
            overflow: hidden;
        }}
        .bar-fill-1 {{
            height: 100%;
            background: {FOREST_GREEN};
            border-radius: 6px;
        }}
        .bar-fill-other {{
            height: 100%;
            background: {NAVY};
            opacity: 0.55;
            border-radius: 6px;
        }}

        /* ---- Warning badge ---- */
        .warn-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #FDF1E3;
            border: 1px solid {SAFFRON};
            color: #8A4B0B;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 0.78rem;
            font-weight: 600;
            margin: 8px 0 4px 0;
        }}

        /* ---- Trait tags ---- */
        .trait-tag {{
            display: inline-block;
            background: #E7EFE8;
            color: {FOREST_GREEN};
            border: 1px solid #BFD6C4;
            border-radius: 999px;
            padding: 5px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin: 0 6px 6px 0;
        }}

        /* ---- Buttons ---- */
        div.stButton > button {{
            width: 100%;
            border-radius: 10px;
            padding: 0.65rem 0.5rem;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        div.stButton > button[kind="primary"] {{
            background-color: {FOREST_GREEN};
            border: none;
        }}

        /* ---- Impact footer ---- */
        .impact-footer {{
            background: {CARD_BG};
            border-left: 4px solid {SAFFRON};
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 0.76rem;
            color: {TEXT_MUTED};
            margin-top: 22px;
            margin-bottom: 12px;
        }}
        .impact-footer b {{ color: {NAVY}; }}

        /* ---- Confirmation toast card ---- */
        .confirm-card {{
            background: #EAF5EC;
            border: 1px solid {FOREST_GREEN};
            border-radius: 10px;
            padding: 12px 14px;
            color: #14331e;
            font-size: 0.85rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# MOCK PREDICTION FUNCTION
# Swap the body of this function for a real model call — keep the same
# return shape so nothing else in the app needs to change.
# ----------------------------------------------------------------------------
BREED_TRAIT_LIBRARY = {
    "Gir": ["Convex forehead", "Long drooping ears", "Prominent dewlap"],
    "Sahiwal": ["Loose skin", "Medium dewlap", "Reddish-brown coat"],
    "Tharparkar": ["White-grey coat", "Compact body", "Medium-sized ears"],
    "Red Sindhi": ["Deep red coat", "Broad forehead", "Short horns"],
    "Murrah (Buffalo)": ["Tightly curled horns", "Jet black coat", "Large udder"],
    "Jaffarabadi (Buffalo)": ["Massive drooping horns", "Broad forehead", "Heavy dewlap"],
    "Kankrej": ["Lyre-shaped horns", "Silver-grey coat", "Deep chest"],
    "Ongole": ["Large hump", "Loose skin folds", "White coat"],
}


def predict_breed(image):
    """
    Mock breed classifier.
    Replace this implementation with a real model call (e.g. CLIP zero-shot
    or a fine-tuned HF model). Keep the return shape identical:

    Returns: list of up to 3 dicts, sorted by confidence descending:
        [{"breed": str, "confidence": float (0-1), "traits": list[str]}, ...]
    """
    time.sleep(0.6)  # simulate inference latency for a realistic demo feel

    all_breeds = list(BREED_TRAIT_LIBRARY.keys())
    random.seed(hash(image.size) % (10**6))  # stable-ish per uploaded image

    top = random.choice(all_breeds)
    remaining = [b for b in all_breeds if b != top]
    second, third = random.sample(remaining, 2)

    # Occasionally simulate a "hard case" with a close top-2 split
    hard_case = random.random() < 0.4
    if hard_case:
        c1 = round(random.uniform(0.42, 0.55), 2)
        c2 = round(c1 - random.uniform(0.03, 0.09), 2)
    else:
        c1 = round(random.uniform(0.68, 0.91), 2)
        c2 = round(random.uniform(0.08, 0.20), 2)
    c3 = round(max(0.03, 1 - c1 - c2), 2)

    results = [
        {"breed": top, "confidence": c1, "traits": BREED_TRAIT_LIBRARY[top]},
        {"breed": second, "confidence": c2, "traits": BREED_TRAIT_LIBRARY[second]},
        {"breed": third, "confidence": c3, "traits": BREED_TRAIT_LIBRARY[third]},
    ]
    return results


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="gov-header">
        <div class="emblem-row">
            <div>
                <h1>🐄 Bharat Pashudhan — AI Field Entry Module</h1>
                <div class="subtitle">Department of Animal Husbandry &amp; Dairying (DAHD)</div>
            </div>
        </div>
        <div style="margin-top:10px;">
            <span class="status-pill">🟢 Online / Sync Active</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "AI-assisted decision support for breed entry. This tool provides a "
    "second opinion — the enumerator's judgment is always final."
)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "predictions" not in st.session_state:
    st.session_state.predictions = None
if "saved_log" not in st.session_state:
    st.session_state.saved_log = []

# ----------------------------------------------------------------------------
# STEP 1 — FIELD METADATA HEADER
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="step-label"><span class="step-badge">1</span> Field Metadata</div>',
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="field-card">', unsafe_allow_html=True)

    ear_tag = f"IND-{random.randint(100000, 999999)}"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="meta-badge">Ear Tag ID<br><b>{ear_tag}</b></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="meta-badge">Worker ID<br><b>DAHD-EN-2291</b></div>',
            unsafe_allow_html=True,
        )

    state = st.selectbox(
        "State",
        ["Madhya Pradesh", "Rajasthan", "Gujarat", "Uttar Pradesh", "Punjab", "Haryana", "Bihar"],
    )
    district = st.text_input("District", value="Bhopal")

    st.markdown(
        f'<div class="meta-badge">📍 Logged at: {datetime.now().strftime("%d %b %Y, %I:%M %p")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# STEP 2 — DUAL PHOTO CAPTURE
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="step-label"><span class="step-badge">2</span> Capture Animal Photo</div>',
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="field-card">', unsafe_allow_html=True)
    tab_upload, tab_camera = st.tabs(["📁 Upload Photo", "📷 Use Camera"])

    image = None
    with tab_upload:
        uploaded_file = st.file_uploader(
            "Choose a photo from device", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
        )
        if uploaded_file:
            image = Image.open(uploaded_file)

    with tab_camera:
        camera_file = st.camera_input("Take a live photo", label_visibility="collapsed")
        if camera_file:
            image = Image.open(camera_file)

    if image is not None:
        st.image(image, caption="Captured photo", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# RUN PREDICTION
# ----------------------------------------------------------------------------
if image is not None:
    if st.button("🔍 Analyze Breed", type="primary"):
        with st.spinner("Analyzing morphological features..."):
            st.session_state.predictions = predict_breed(image)

# ----------------------------------------------------------------------------
# STEP 3 — TOP-3 PREDICTION VISUALIZATION
# ----------------------------------------------------------------------------
if st.session_state.predictions:
    preds = st.session_state.predictions

    st.markdown(
        '<div class="step-label"><span class="step-badge">3</span> AI Breed Suggestions</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="field-card">', unsafe_allow_html=True)

        # Borderline / hard-case warning
        top_conf = preds[0]["confidence"]
        second_conf = preds[1]["confidence"]
        is_close_split = (top_conf - second_conf) < 0.15
        is_low_confidence = top_conf < 0.55

        if is_close_split or is_low_confidence:
            st.markdown(
                '<div class="warn-badge">⚠️ Borderline confidence — visually similar breeds detected. '
                "Please verify manually before confirming.</div>",
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
                        <span class="{rank_class}">#{i+1}  {p['breed']}</span>
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

    # ------------------------------------------------------------------
    # STEP 4 — "WHY THIS BREED" TRAIT EXPLAINER
    # ------------------------------------------------------------------
    st.markdown(
        '<div class="step-label"><span class="step-badge">4</span> Why This Breed?</div>',
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="field-card">', unsafe_allow_html=True)
        st.markdown(
            f"Key visual traits matched for **{preds[0]['breed']}**:",
        )
        tags_html = "".join(
            f'<span class="trait-tag">✓ {t}</span>' for t in preds[0]["traits"]
        )
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # STEP 5 — ENUMERATOR DECISION & ACTION FLOW
    # ------------------------------------------------------------------
    st.markdown(
        '<div class="step-label"><span class="step-badge">5</span> Confirm Breed Entry</div>',
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="field-card">', unsafe_allow_html=True)

        breed_options = [p["breed"] for p in preds] + ["Other (manual entry)"]
        final_breed = st.selectbox(
            "Select final breed for record (defaults to top AI suggestion — override if needed)",
            breed_options,
            index=0,
        )
        if final_breed == "Other (manual entry)":
            final_breed = st.text_input("Enter breed manually")

        notes = st.text_input("Additional notes (optional)")

        if st.button("✅ Confirm & Save to Pashudhan Log", type="primary"):
            st.session_state.saved_log.append(
                {
                    "ear_tag": ear_tag,
                    "state": state,
                    "district": district,
                    "breed": final_breed,
                    "ai_top_suggestion": preds[0]["breed"],
                    "ai_confidence": f"{int(preds[0]['confidence']*100)}%",
                    "notes": notes,
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                }
            )
            st.markdown(
                f"""
                <div class="confirm-card">
                    ✅ <b>Record saved.</b> Ear Tag {ear_tag} logged as <b>{final_breed}</b>
                    for {district}, {state}.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SESSION LOG (for demo purposes — shows submitted entries this session)
# ----------------------------------------------------------------------------
if st.session_state.saved_log:
    with st.expander(f"📋 Session log ({len(st.session_state.saved_log)} entries)"):
        st.table(st.session_state.saved_log)

# ----------------------------------------------------------------------------
# STEP 6 — IMPACT BANNER FOOTER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="impact-footer">
        <b>Why this matters:</b> Manual breed misclassification during field data
        entry is a recognized source of error in national livestock databases.
        AI-assisted second-opinion tools aim to reduce entry errors without
        replacing enumerator judgment — every suggestion here requires human
        confirmation before being logged.
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Prototype build for hackathon demonstration. Not an official DAHD product.")
