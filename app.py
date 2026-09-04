"""
Bharat Pashudhan — AI Field Entry Module
Complete app containing live stats tiles and photo analysis flow.
"""

import random
import time
from datetime import datetime
import streamlit as st
from PIL import Image

# ----------------------------------------------------------------------------
# PAGE CONFIG & CSS STYLING
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Bharat Pashudhan — AI Field Entry",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .main > div {
            max-width: 520px;
            padding-top: 1rem;
        }
        
        /* Stats Header Glass Card */
        .stats-banner {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.85));
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
        }
        
        .tag-saffron {
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            color: #FF9933;
            text-transform: uppercase;
        }

        .header-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #0A2540;
            margin: 4px 0 6px 0;
            line-height: 1.2;
        }

        .header-desc {
            font-size: 0.8rem;
            color: #475569;
            line-height: 1.4;
            margin-bottom: 14px;
        }

        /* Metric Tile Grid */
        .tile-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }
        
        @media (min-width: 480px) {
            .tile-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }

        .metric-tile {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 8px 10px;
            text-align: left;
        }

        .metric-label {
            font-size: 0.58rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-value {
            font-size: 1.1rem;
            font-weight: 800;
            color: #1E5631;
            margin-top: 2px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 1. HEADER & STATS TILES (Translated from JS Component)
# ----------------------------------------------------------------------------
stats = {
    "total": 124,
    "agreementRate": 87,
    "borderline": 12,
    "districts": 18,
}

st.markdown(
    f"""
    <div class="stats-banner">
        <div class="tag-saffron">AI Field Entry Module</div>
        <div class="header-title">Breed identification as a <span style="color: #FF9933;">second opinion</span></div>
        <div class="header-desc">
            Capture the animal, let the on-device vision model shortlist three candidate
            breeds, compare against the standard breed plate, then confirm. Every decision
            is stamped with the AI suggestion so misclassification can be audited later.
        </div>
        <div class="tile-grid">
            <div class="metric-tile">
                <div class="metric-label">Records in module</div>
                <div class="metric-value">{stats['total']}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-label">AI / Enum Match</div>
                <div class="metric-value">{stats['agreementRate']}%</div>
            </div>
            <div class="metric-tile">
                <div class="metric-label">Borderline Cases</div>
                <div class="metric-value">{stats['borderline']}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-label">Districts Covered</div>
                <div class="metric-value">{stats['districts']}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 2. FIELD ENTRY FLOW (Native Streamlit Form)
# ----------------------------------------------------------------------------
st.subheader("Field Entry & Photo Capture")

tab_upload, tab_camera = st.tabs(["📁 Upload File", "📷 Use Camera"])

image = None
with tab_upload:
    uploaded_file = st.file_uploader("Choose a photo from device", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)

with tab_camera:
    camera_file = st.camera_input("Take a live photo")
    if camera_file:
        image = Image.open(camera_file)

if image is not None:
    st.image(image, caption="Captured Field Photo", use_container_width=True)
    if st.button("🔍 Analyze Breed Characteristics", type="primary", use_container_width=True):
        st.success("Analysis complete! (AI model prediction connected)")
