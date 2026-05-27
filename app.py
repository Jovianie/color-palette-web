import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Color Palette",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: #f0f2f5 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
#MainMenu, footer { display: none !important; }

/* ── Main card container ── */
.block-container {
    padding: 0 !important;
    max-width: 780px !important;
    margin: 0 auto;
}

/* ── Top nav bar ── */
.nav-bar {
    background: #fff;
    border-bottom: 1px solid #e8eaed;
    padding: 0 40px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #1a2332;
    letter-spacing: -0.01em;
}
.nav-badge {
    background: #1a2332;
    color: #fff;
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 20px;
}

/* ── Hero section ── */
.hero {
    background: #1a2332;
    padding: 56px 40px 52px;
}
.hero-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7c9cbf;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 14px;
}
.hero-title span { color: #4fa3e0; }
.hero-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: #8a9bb5;
    line-height: 1.7;
    max-width: 480px;
    font-weight: 300;
}

/* ── Main content area ── */
.content-area {
    background: #fff;
    padding: 36px 40px 48px;
    border-bottom: 1px solid #e8eaed;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9aa5b4;
    margin-bottom: 10px;
}

/* ── Streamlit file uploader override ── */
[data-testid="stFileUploader"] {
    background: #f8f9fb !important;
    border: 1.5px dashed #d1d9e0 !important;
    border-radius: 12px !important;
    padding: 4px 8px !important;
    transition: border-color 0.2s, background 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #4fa3e0 !important;
    background: #f0f7fd !important;
}
[data-testid="stFileUploader"] section {
    padding: 10px !important;
}
[data-testid="stFileUploader"] * {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    color: #6b7a8d !important;
}
[data-testid="stFileUploader"] button {
    background: #1a2332 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 6px 18px !important;
}

/* ── Slider ── */
.stSlider {
    padding-top: 8px !important;
}
.stSlider [data-baseweb="slider"] {
    margin-top: 8px;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #1a2332 !important;
    border: 3px solid #fff !important;
    box-shadow: 0 2px 8px rgba(26,35,50,0.25) !important;
    width: 20px !important;
    height: 20px !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
    display: none;
}
.stSlider [data-baseweb="slider"] div[class*="Track"] {
    height: 4px !important;
    background: #e8eaed !important;
    border-radius: 2px !important;
}
.stSlider [data-baseweb="slider"] div[class*="Track"]:first-child {
    background: #1a2332 !important;
}
.stSlider p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #9aa5b4 !important;
}
div[data-testid="stSliderTickBarMin"],
div[data-testid="stSliderTickBarMax"] { display: none !important; }

/* ── Palette strip ── */
.palette-strip {
    display: flex;
    border-radius: 14px;
    overflow: hidden;
    height: 80px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(26,35,50,0.12);
}
.strip-swatch {
    flex: 1;
    transition: flex 0.35s cubic-bezier(.4,0,.2,1);
    cursor: default;
}
.strip-swatch:hover { flex: 2; }

/* ── Color cards ── */
.cards-grid {
    display: flex;
    gap: 12px;
}
.color-card {
    flex: 1;
    border-radius: 12px;
    overflow: hidden;
    background: #fff;
    border: 1px solid #e8eaed;
    box-shadow: 0 2px 8px rgba(26,35,50,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.color-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(26,35,50,0.13);
}
.card-swatch {
    height: 72px;
    width: 100%;
}
.card-body {
    padding: 10px 12px 12px;
}
.card-hex {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: #1a2332;
    letter-spacing: 0.02em;
}
.card-pct {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    color: #9aa5b4;
    margin-top: 3px;
    font-weight: 400;
}

/* ── Divider ── */
.hr {
    border: none;
    border-top: 1px solid #e8eaed;
    margin: 28px 0;
}

/* ── Image preview ── */
.img-preview {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e8eaed;
    box-shadow: 0 2px 12px rgba(26,35,50,0.07);
}

/* ── Empty state ── */
.empty {
    background: #f8f9fb;
    border: 1.5px dashed #d1d9e0;
    border-radius: 14px;
    padding: 56px 24px;
    text-align: center;
    margin-top: 28px;
}
.empty-icon {
    font-size: 2rem;
    margin-bottom: 12px;
    opacity: 0.25;
}
.empty-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    color: #9aa5b4;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Footer ── */
.footer {
    background: #f0f2f5;
    padding: 20px 40px;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #b0bac8;
    letter-spacing: 0.06em;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    color: #6b7a8d !important;
}
</style>
""", unsafe_allow_html=True)


def rgb_to_hex(r, g, b):
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

def extract_palette(image, n):
    img = image.convert("RGB").resize((200, 200), Image.LANCZOS)
    pixels = np.array(img).reshape(-1, 3).astype(np.float32)
    km = KMeans(n_clusters=n, n_init=10, max_iter=300, random_state=42)
    labels = km.fit_predict(pixels)
    centers = km.cluster_centers_
    counts = np.bincount(labels, minlength=n)
    order = np.argsort(-counts)
    total = counts.sum()
    return [{
        "hex": rgb_to_hex(*centers[i]),
        "pct": counts[i] / total * 100,
    } for i in order]


# ── Nav bar
st.markdown("""
<div class="nav-bar">
    <span class="nav-logo">ColorPalette</span>
    <span class="nav-badge">K-Means · AI</span>
</div>
""", unsafe_allow_html=True)

# ── Hero
st.markdown("""
<div class="hero">
    <p class="hero-eyebrow">Image Color Extractor</p>
    <h1 class="hero-title">Extract <span>dominant</span><br>colors from any image.</h1>
    <p class="hero-desc">Upload a photo and get a clean color palette powered by K-Means clustering — an unsupervised machine learning algorithm.</p>
</div>
""", unsafe_allow_html=True)

# ── Content area
st.markdown('<div class="content-area">', unsafe_allow_html=True)

st.markdown('<p class="section-label">Upload Image</p>', unsafe_allow_html=True)
uploaded = st.file_uploader("img", type=["jpg","jpeg","png","webp","bmp"], label_visibility="collapsed")

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-label">Colors to Extract</p>', unsafe_allow_html=True)
n = st.slider("n", 3, 10, 5, label_visibility="collapsed")

if uploaded:
    image = Image.open(uploaded)

    with st.spinner("Analyzing..."):
        palette = extract_palette(image, n)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Color Palette</p>', unsafe_allow_html=True)

    # Strip
    strip = '<div class="palette-strip">'
    for c in palette:
        strip += f'<div class="strip-swatch" style="background:{c["hex"]}"></div>'
    strip += '</div>'
    st.markdown(strip, unsafe_allow_html=True)

    # Cards
    cards = '<div class="cards-grid">'
    for c in palette:
        cards += f'''<div class="color-card">
            <div class="card-swatch" style="background:{c["hex"]}"></div>
            <div class="card-body">
                <div class="card-hex">{c["hex"]}</div>
                <div class="card-pct">{c["pct"]:.0f}% dominant</div>
            </div>
        </div>'''
    cards += '</div>'
    st.markdown(cards, unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Source Image</p>', unsafe_allow_html=True)
    st.markdown('<div class="img-preview">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('''
    <div class="empty">
        <div class="empty-icon">◎</div>
        <p class="empty-text">Upload an image to begin</p>
    </div>''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close content-area

# ── Footer
st.markdown("""
<div class="footer">
    K-Means Clustering &nbsp;·&nbsp; Artificial Intelligence &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)
