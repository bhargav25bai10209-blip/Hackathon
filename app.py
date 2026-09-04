import streamlit as st
from PIL import Image

# Temporary mock function until Person A provides the real model
def predict_breed(image):
    return [
        {"breed": "Gir", "confidence": 0.85},
        {"breed": "Sahiwal", "confidence": 0.10},
        {"breed": "Murrah", "confidence": 0.05},
    ]

st.set_page_config(page_title="Breed Assist", layout="centered")
st.title("🐄 Cattle & Buffalo Breed Assist")
st.caption("A second opinion for field data entry — not a replacement for expert judgment.")

uploaded = st.file_uploader("Upload or take a photo", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded photo", use_container_width=True)

    with st.spinner("Analyzing..."):
        results = predict_breed(image)  # Plugs in real model when ready

    st.subheader("Top predictions")
    for r in results:
        st.write(f"**{r['breed']}** ({int(r['confidence'] * 100)}%)")
        st.progress(r['confidence'])
