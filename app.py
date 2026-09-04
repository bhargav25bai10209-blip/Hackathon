import streamlit as st

# Set page layout
st.set_page_config(
    page_title="Bharat Pashudhan — AI Field Entry",
    page_icon="🐄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# TAILWIND & CUSTOM GLASSMORPHISM STYLES
# ----------------------------------------------------------------------------
st.markdown(
    """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .main > div {
            max-width: 680px;
            padding-top: 1rem;
        }
        .glass {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.8));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        }
        .text-saffron { color: #FF9933; }
        .text-navy { color: #002B49; }
        .text-forest { color: #1E5631; }
        .text-muted { color: #64748B; }
        .shimmer-text {
            background: linear-gradient(90deg, #002B49, #FF9933, #002B49);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# MOCK STATS (Replaces computeStats & listEntries)
# ----------------------------------------------------------------------------
stats = {
    "total": 124,
    "agreementRate": 87,
    "borderline": 12,
    "districts": 18,
}

tiles = [
    ("Records in module", str(stats["total"])),
    ("AI / enumerator match", f"{stats['agreementRate']}%"),
    ("Borderline cases", str(stats["borderline"])),
    ("Districts covered", str(stats["districts"])),
]

# Build tiles HTML
tiles_html = "".join(
    [
        f"""
        <div class="rounded-xl border border-slate-200/80 bg-gradient-to-b from-white/90 to-white/60 px-3 py-2.5 text-left shadow-sm">
            <dt class="text-[0.58rem] font-bold tracking-[0.09em] text-muted uppercase">{label}</dt>
            <dd class="text-[1.15rem] leading-tight font-extrabold text-forest tabular-nums mt-0.5">{value}</dd>
        </div>
        """
        for label, value in tiles
    ]
)

# ----------------------------------------------------------------------------
# RENDER UI BANNER
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="flex flex-col gap-5">
        <section class="glass p-4 sm:p-5">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <p class="text-[0.64rem] font-extrabold tracking-[0.16em] text-saffron uppercase">
                        AI Field Entry Module
                    </p>
                    <h2 class="mt-1 text-[1.35rem] leading-tight font-extrabold text-navy sm:text-[1.6rem]">
                        Breed identification as a <span class="shimmer-text">second opinion</span>
                    </h2>
                    <p class="mt-1.5 max-w-xl text-[0.82rem] leading-relaxed font-medium text-muted">
                        Capture the animal, let the on-device vision model shortlist three candidate
                        breeds, compare against the standard breed plate, then confirm. Every decision
                        is stamped with the AI suggestion so misclassification can be audited later.
                    </p>
                </div>
            </div>
            <dl class="grid w-full grid-cols-2 gap-2 mt-4 sm:grid-cols-4">
                {tiles_html}
            </dl>
        </section>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ----------------------------------------------------------------------------
# FIELD ENTRY FLOW (Streamlit native widgets)
# ----------------------------------------------------------------------------
st.subheader("Field Entry & Photo Capture")
uploaded_file = st.file_uploader("Upload Animal Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    st.button("🔍 Analyze Breed Characteristics", type="primary", use_container_width=True)
