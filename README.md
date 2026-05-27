# ChromaLens 🎨
**Dominant Color Palette Extractor** — powered by K-Means Clustering

Upload any image and get the 3–10 most dominant colors extracted automatically using unsupervised machine learning (K-Means).

---

## 🚀 Deploy ke Streamlit Cloud (GRATIS, step by step)

### Step 1 — Buat akun GitHub (kalau belum punya)
1. Buka [github.com](https://github.com) → klik **Sign Up**
2. Daftar pakai email, verifikasi, selesai

---

### Step 2 — Upload project ke GitHub

#### Cara A: Lewat website GitHub (paling mudah)
1. Login ke GitHub → klik tombol **"+"** di pojok kanan atas → **New repository**
2. Isi nama repo: `color-palette-app` (atau bebas)
3. Pilih **Public** ✅
4. Klik **Create repository**
5. Di halaman repo yang baru dibuat, klik **"uploading an existing file"**
6. Drag & drop **kedua file** ini: `app.py` dan `requirements.txt`
7. Klik **Commit changes** → selesai!

#### Cara B: Lewat GitHub Desktop (juga mudah)
1. Download [GitHub Desktop](https://desktop.github.com/) dan install
2. Login dengan akun GitHub
3. **File → New Repository** → isi nama, klik Create
4. Copy `app.py` dan `requirements.txt` ke folder repo yang dibuat
5. Klik **Commit to main** → **Publish repository** → pastikan **Public**

---

### Step 3 — Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Klik **"Sign in with GitHub"** → authorize
3. Klik **"New app"**
4. Isi form:
   - **Repository**: pilih repo yang baru kamu buat tadi
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Klik **"Deploy!"**
6. Tunggu ~2–3 menit (ada loading bar)
7. ✅ Website kamu live! Link-nya berbentuk: `https://namakamu-color-palette-app-xxxx.streamlit.app`

---

## 📁 Struktur File
```
color-palette-app/
├── app.py            ← kode utama aplikasi
└── requirements.txt  ← daftar library yang dibutuhkan
```

## 🛠️ Cara Jalankan Lokal (opsional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📚 Teknologi
- **Streamlit** — framework web app Python
- **K-Means Clustering** (scikit-learn) — algoritma ML untuk ekstraksi warna
- **Pillow** — pemrosesan gambar
- **NumPy** — operasi array/matrix pixel
