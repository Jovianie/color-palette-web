import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import io
import colorsys

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChromaLens · Color Palette Extractor",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & Base */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a0a2e 0%, #0d0d0d 60%) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 760px !important;
}

/* Hero Title */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 7vw, 5rem);
    font-weight: 900;
    color: #ffffff;
    line-height: 1.0;
    letter-spacing: -0.02em;
    margin: 0 0 0.2rem 0;
    text-align: center;
}

.hero-title span {
    background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: rgba(255,255,255,0.45);
    text-align: center;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
    font-weight: 300;
}

/* Upload Zone */
.upload-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 0.4rem;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
    margin: 2rem 0;
}

/* Palette Swatch */
.palette-grid {
    display: flex;
    border-radius: 16px;
    overflow: hidden;
    height: 90px;
    margin: 1.2rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}

.swatch {
    flex: 1;
    cursor: pointer;
    transition: flex 0.3s ease;
    position: relative;
}

.swatch:hover { flex: 1.6; }

/* Color Cards */
.color-cards {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-top: 1rem;
}

.color-card {
    border-radius: 12px;
    overflow: hidden;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.color-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4);
}

.card-swatch {
    width: 100%;
    height: 70px;
}

.card-info {
    padding: 8px 10px 10px;
    font-family: 'DM Sans', sans-serif;
}

.card-hex {
    font-size: 0.72rem;
    font-weight: 500;
    color: #ffffff;
    letter-spacing: 0.05em;
}

.card-rgb {
    font-size: 0.62rem;
    color: rgba(255,255,255,0.35);
    margin-top: 2px;
}

.card-pct {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.25);
    margin-top: 2px;
}

/* Section Labels */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
    margin-bottom: 0.6rem;
    margin-top: 1.8rem;
}

/* Tag badge */
.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.5);
    border: 1px solid rgba(255,255,255,0.1);
    margin: 0 4px 4px 0;
}

/* Image container */
.img-container {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}

/* Hide Streamlit UI chrome */
#MainMenu { display: none; }
footer { display: none !important; }
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border: 1px dashed rgba(255,255,255,0.15);
    border-radius: 14px;
    padding: 0.5rem;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(255,255,255,0.3);
}

/* Slider */
.stSlider > div > div > div > div { background: #ff6b6b !important; }

/* Spinner */
[data-testid="stSpinner"] { color: rgba(255,255,255,0.5) !important; }

/* Info box */
.info-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 16px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.4);
    line-height: 1.6;
    margin-top: 0.8rem;
}

.info-box b {
    color: rgba(255,255,255,0.7);
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ─────────────────────────────────────────────────────────
def rgb_to_hex(r, g, b):
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

def hex_to_rgb_text(hex_color):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgb({r}, {g}, {b})"

def get_luminance(r, g, b):
    """Return relative luminance for contrast checking."""
    def c(x):
        x = x / 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)

def text_color_for_bg(r, g, b):
    """Return black or white text depending on background luminance."""
    return "#000000" if get_luminance(r, g, b) > 0.35 else "#ffffff"

def color_name_hint(r, g, b):
    """Very rough color name from HSV."""
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h_deg = h * 360
    if v < 0.15:
        return "Deep Black"
    if v > 0.9 and s < 0.08:
        return "Near White"
    if s < 0.12:
        return "Neutral Gray"
    if h_deg < 15 or h_deg >= 345:
        return "Red"
    elif h_deg < 40:
        return "Orange"
    elif h_deg < 65:
        return "Yellow"
    elif h_deg < 150:
        return "Green"
    elif h_deg < 185:
        return "Cyan"
    elif h_deg < 260:
        return "Blue"
    elif h_deg < 290:
        return "Violet"
    elif h_deg < 345:
        return "Pink / Magenta"
    return "Color"

def extract_palette(image: Image.Image, n_colors: int = 5):
    """Use K-Means clustering to find dominant colors."""
    # Resize for speed — doesn't affect quality much
    img = image.convert("RGB")
    img_small = img.resize((200, 200), Image.LANCZOS)
    pixels = np.array(img_small).reshape(-1, 3).astype(np.float32)

    kmeans = KMeans(
        n_clusters=n_colors,
        n_init=10,
        max_iter=300,
        random_state=42
    )
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_

    # Sort by frequency (most dominant first)
    counts = np.bincount(labels, minlength=n_colors)
    total = counts.sum()
    order = np.argsort(-counts)

    palette = []
    for idx in order:
        r, g, b = centers[idx]
        pct = counts[idx] / total * 100
        palette.append({
            "hex": rgb_to_hex(r, g, b),
            "r": int(r), "g": int(g), "b": int(b),
            "pct": pct,
            "name": color_name_hint(r, g, b),
            "text": text_color_for_bg(r, g, b),
        })

    return palette


# ─── App Layout ──────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">Chroma<span>Lens</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Dominant Color Palette Extractor · Powered by K-Means</p>', unsafe_allow_html=True)

# Upload
st.markdown('<p class="upload-label">Upload an image to begin</p>', unsafe_allow_html=True)
uploaded = st.file_uploader(
    label="Upload",
    type=["jpg", "jpeg", "png", "webp", "bmp"],
    label_visibility="collapsed",
)

n_colors = st.slider("Number of colors to extract", min_value=3, max_value=10, value=5, step=1)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if uploaded is not None:
    image = Image.open(uploaded)

    # Show uploaded image
    st.markdown('<p class="section-label">Source Image</p>', unsafe_allow_html=True)
    st.markdown('<div class="img-container">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Extract palette
    with st.spinner("Analyzing colors with K-Means clustering..."):
        palette = extract_palette(image, n_colors)

    # ── Palette strip ──
    st.markdown('<p class="section-label">Color Palette</p>', unsafe_allow_html=True)

    swatch_html = '<div class="palette-grid">'
    for c in palette:
        swatch_html += f'<div class="swatch" style="background:{c["hex"]}" title="{c["hex"]}"></div>'
    swatch_html += '</div>'
    st.markdown(swatch_html, unsafe_allow_html=True)

    # ── Color cards ──
    cards_html = '<div class="color-cards">'
    for c in palette:
        cards_html += f"""
        <div class="color-card">
            <div class="card-swatch" style="background:{c['hex']}"></div>
            <div class="card-info">
                <div class="card-hex">{c['hex']}</div>
                <div class="card-rgb">rgb({c['r']}, {c['g']}, {c['b']})</div>
                <div class="card-pct">{c['pct']:.1f}% dominant</div>
            </div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── Color tags (names) ──
    st.markdown('<div style="margin-top:1rem">', unsafe_allow_html=True)
    tags_html = ""
    for c in palette:
        tags_html += f'<span class="tag" style="border-color:{c["hex"]}55">{c["name"]}</span>'
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Info box ──
    st.markdown(f"""
    <div class="info-box">
        <b>How it works:</b> This app uses the <b>K-Means Clustering</b> algorithm
        (unsupervised machine learning) to group the pixels of your image into
        <b>{n_colors} clusters</b> based on color similarity.
        Each cluster centroid becomes one of the dominant colors in the palette.
        Colors are sorted from most to least dominant.
    </div>
    """, unsafe_allow_html=True)

    # ── Export ──
    st.markdown('<p class="section-label">Export</p>', unsafe_allow_html=True)
    hex_list = " | ".join([c["hex"] for c in palette])
    css_vars = "\n".join([f"  --color-{i+1}: {c['hex']};" for i, c in enumerate(palette)])
    export_text = f"HEX Values:\n{hex_list}\n\nCSS Variables:\n:root {{\n{css_vars}\n}}"
    st.code(export_text, language="css")

else:
    # Placeholder state
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem; color: rgba(255,255,255,0.2); font-family: 'DM Sans', sans-serif;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🖼️</div>
        <div style="font-size: 0.85rem; letter-spacing: 0.1em; text-transform: uppercase;">
            Upload an image above to extract its color palette
        </div>
        <div style="font-size: 0.75rem; margin-top: 0.5rem; opacity: 0.6">
            Supports JPG, PNG, WEBP, BMP
        </div>
    </div>
    """, unsafe_allow_html=True)
