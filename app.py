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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: #513229 !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stFileUploaderDropzoneInstructions"] > div > span,
[data-testid="stFileUploaderDropzoneInstructions"] > div > small { display: none !important; }
#MainMenu, footer { display: none !important; }

.block-container {
    padding: 64px 48px 80px !important;
    max-width: 600px !important;
}

/* ── Header ── */
.header { margin-bottom: 48px; }

.header-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #FCE6B7;
    margin-bottom: 10px;
}

.header-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 600;
    color: #F4F1E2;
    line-height: 1.0;
    letter-spacing: -0.01em;
}

.header-title em {
    font-style: italic;
    font-weight: 400;
    color: #F4F1E2;
}

/* ── Divider ── */
.rule {
    height: 1px;
    background: #e8e0d5;
    margin: 0 0 40px;
}

/* ── Labels ── */
.lbl {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.6rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #513229;
    margin-bottom: 10px;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #FFF8EC !important;
    border: 1.5px solid #e8dfd3 !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #FCE6B7 !important;
    background: #f5f9fc !important;
}
[data-testid="stFileUploader"] section {
    padding: 20px 16px !important;
    min-height: unset !important;
}
[data-testid="stFileUploader"] button {
    background: #513229 !important;
    color: #FFF1B5 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em !important;
    padding: 8px 20px !important;
}
[data-testid="stFileUploader"] button:hover {
    background: #5a3f3c !important;
}
[data-testid="stFileUploaderFileName"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    color: #7a6356 !important;
}

/* ── Slider ── */
.stSlider { margin-top: 28px !important; }

.stSlider p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.6rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: #fce6b7 !important;
    margin-bottom: 10px !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #F4F1E2 !important;
    border: 2px solid #513229 !important;
    box-shadow: 0 1px 6px rgba(67,48,46,0.2) !important;
    width: 18px !important;
    height: 18px !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stTickBarMin"],
.stSlider [data-baseweb="slider"] [data-testid="stTickBarMax"],
div[data-testid="stSliderTickBarMin"],
div[data-testid="stSliderTickBarMax"] { display: none !important; }

/* ── Palette strip ── */
.palette-strip {
    display: flex;
    border-radius: 16px;
    overflow: hidden;
    height: 72px;
    margin-bottom: 16px;
    box-shadow: 0 2px 16px rgba(67,48,46,0.10);
}
.strip-sw {
    flex: 1;
    transition: flex 0.35s ease;
}
.strip-sw:hover { flex: 2; }

/* ── Color cards ── */
.cards {
    display: flex;
    gap: 10px;
}
.card {
    flex: 1;
    border-radius: 12px;
    overflow: hidden;
    background: #fff;
    border: 1px solid #ece5dc;
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(67,48,46,0.10);
}
.card-sw { height: 60px; }
.card-info { padding: 9px 11px 11px; }
.card-hex {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 400;
    color: #F4F1E2;
    letter-spacing: 0.04em;
}
.card-pct {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.58rem;
    color: #c2b0a2;
    margin-top: 2px;
}

/* ── Image preview ── */
.img-wrap {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #ece5dc;
}

/* ── Empty state ── */
.empty {
    padding: 52px 0 20px;
    text-align: center;
}
.empty-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 1.5px solid #e0d5ca;
    margin: 0 auto 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #d4c8be;
    font-size: 1.2rem;
}
.empty-txt {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c2b0a2;
}

/* ── Gap util ── */
.gap { margin-top: 36px; }
.gap-sm { margin-top: 20px; }
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
    return [{"hex": rgb_to_hex(*centers[i]), "pct": counts[i]/total*100} for i in order]


# ── Header
st.markdown("""
<div class="header">
    <p class="header-eyebrow">Color Palette Extractor</p>
     <h1 class="header-title"><em>Find the colors</em><br><em>in your image.<em/></h1>
</div>
<div class="rule"></div>
""", unsafe_allow_html=True)

# ── Upload
st.markdown('<p class="lbl">Upload image</p>', unsafe_allow_html=True)
uploaded = st.file_uploader(
    "Upload", type=["jpg","jpeg","png","webp","bmp"],
    label_visibility="collapsed"
)

# ── Slider
st.markdown('<p class="lbl" style="margin-top:28px">Colors to extract</p>', unsafe_allow_html=True)
n = st.slider("n", 3, 10, 5, label_visibility="collapsed")

# ── Results
if uploaded:
    image = Image.open(uploaded)

    with st.spinner(""):
        palette = extract_palette(image, n)

    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lbl">Palette</p>', unsafe_allow_html=True)

    strip = '<div class="palette-strip">'
    for c in palette:
        strip += f'<div class="strip-sw" style="background:{c["hex"]}"></div>'
    strip += '</div>'
    st.markdown(strip, unsafe_allow_html=True)

    cards = '<div class="cards">'
    for c in palette:
        cards += f'''<div class="card">
            <div class="card-sw" style="background:{c["hex"]}"></div>
            <div class="card-info">
                <div class="card-hex">{c["hex"]}</div>
                <div class="card-pct">{c["pct"]:.0f}%</div>
            </div>
        </div>'''
    cards += '</div>'
    st.markdown(cards, unsafe_allow_html=True)

    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lbl">Image</p>', unsafe_allow_html=True)
    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty">
        <div class="empty-circle">◌</div>
        <p class="empty-txt">Upload an image to begin</p>
    </div>
    """, unsafe_allow_html=True)
