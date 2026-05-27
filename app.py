import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(
    page_title="Color Palette",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #faf8f6 !important;
    color: #1a1a1a;
}

[data-testid="stHeader"] { display: none; }
#MainMenu, footer { display: none !important; }

.block-container {
    padding: 3.5rem 2rem 5rem !important;
    max-width: 640px !important;
}

h1.site-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    font-weight: 400;
    color: #1a1a1a;
    letter-spacing: -0.02em;
    line-height: 1;
}

p.site-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: #b0a9a2;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.35rem;
    font-weight: 300;
}

.upload-hint {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: #c4bbb5;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 2.5rem 0 0.5rem;
}

[data-testid="stFileUploader"] {
    background: #fff !important;
    border: 1.5px solid #ede9e5 !important;
    border-radius: 18px !important;
    padding: 0.25rem !important;
    transition: border-color 0.2s;
}

[data-testid="stFileUploader"]:hover {
    border-color: #e0d0cc !important;
}

[data-testid="stFileUploader"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: #b0a9a2 !important;
}

.stSlider { margin-top: 1.2rem; }
.stSlider label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    color: #c4bbb5 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #1a1a1a !important;
    border: none !important;
}
.stSlider [data-baseweb="slider"] div[data-testid="stTickBar"] { display: none; }

.palette-strip {
    display: flex;
    border-radius: 20px;
    overflow: hidden;
    height: 96px;
    margin: 2rem 0 1.2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
}
.swatch { flex: 1; transition: flex 0.3s ease; cursor: default; }
.swatch:hover { flex: 1.8; }

.cards {
    display: flex;
    gap: 10px;
    margin-bottom: 2rem;
}
.card {
    flex: 1;
    border-radius: 14px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.card-color { height: 64px; width: 100%; }
.card-body {
    padding: 8px 10px 10px;
    font-family: 'DM Sans', sans-serif;
}
.card-hex {
    font-size: 0.7rem;
    font-weight: 500;
    color: #1a1a1a;
    letter-spacing: 0.03em;
}
.card-pct {
    font-size: 0.62rem;
    color: #c4bbb5;
    margin-top: 2px;
}

.img-wrap {
    border-radius: 18px;
    overflow: hidden;
    margin: 1.5rem 0 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.empty-state {
    text-align: center;
    padding: 4rem 1rem;
    font-family: 'DM Sans', sans-serif;
}
.empty-state .icon { font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.3; }
.empty-state p {
    font-size: 0.8rem;
    color: #c4bbb5;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

hr.divider {
    border: none;
    border-top: 1px solid #ede9e5;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


def rgb_to_hex(r, g, b):
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

def get_luminance(r, g, b):
    def c(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)

def extract_palette(image, n):
    img = image.convert("RGB").resize((200, 200), Image.LANCZOS)
    pixels = np.array(img).reshape(-1, 3).astype(np.float32)
    km = KMeans(n_clusters=n, n_init=10, max_iter=300, random_state=42)
    labels = km.fit_predict(pixels)
    centers = km.cluster_centers_
    counts = np.bincount(labels, minlength=n)
    total = counts.sum()
    order = np.argsort(-counts)
    return [{
        "hex": rgb_to_hex(*centers[i]),
        "r": int(centers[i][0]), "g": int(centers[i][1]), "b": int(centers[i][2]),
        "pct": counts[i] / total * 100,
    } for i in order]


# ── Header
st.markdown('<h1 class="site-title">Color Palette</h1>', unsafe_allow_html=True)
st.markdown('<p class="site-sub">Extract dominant colors from any image</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Upload
st.markdown('<p class="upload-hint">Upload image</p>', unsafe_allow_html=True)
uploaded = st.file_uploader("img", type=["jpg","jpeg","png","webp","bmp"], label_visibility="collapsed")
n = st.slider("Colors to extract", 3, 10, 5, label_visibility="visible")

if uploaded:
    image = Image.open(uploaded)

    with st.spinner(""):
        palette = extract_palette(image, n)

    # Palette strip
    strip = '<div class="palette-strip">'
    for c in palette:
        strip += f'<div class="swatch" style="background:{c["hex"]}"></div>'
    strip += '</div>'
    st.markdown(strip, unsafe_allow_html=True)

    # Color cards
    cards = '<div class="cards">'
    for c in palette:
        cards += f'''<div class="card">
            <div class="card-color" style="background:{c["hex"]}"></div>
            <div class="card-body">
                <div class="card-hex">{c["hex"]}</div>
                <div class="card-pct">{c["pct"]:.0f}%</div>
            </div>
        </div>'''
    cards += '</div>'
    st.markdown(cards, unsafe_allow_html=True)

    # Image preview
    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('''
    <div class="empty-state">
        <div class="icon">◌</div>
        <p>Upload an image to begin</p>
    </div>''', unsafe_allow_html=True)
