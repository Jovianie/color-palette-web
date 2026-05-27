# TUGAS PERTEMUAN 11 PRAKTIKUM AI
Nama  : Jovianie Felisia Suryadi

NPM   : 140810240010

# Color Palette
Web app untuk mengekstrak 5 warna dominan dari sebuah gambar menggunakan K-Means Clustering.

**Tech:** Python · Streamlit · scikit-learn · Pillow · NumPy

---

## Deploy (Streamlit Cloud)

1. Buat repository **Public** di [github.com](https://github.com)
2. Upload `app.py` dan `requirements.txt` ke repo
3. Buka [share.streamlit.io](https://share.streamlit.io) → login dengan GitHub
4. Klik **New app** → pilih repo, branch `main`, main file `app.py`
5. Klik **Deploy!** → tunggu 2–3 menit → link sudah daoat diakses public

## Cara Pakai

1. Buka link Streamlit yang sudah di-deploy
2. Upload gambar (JPG, PNG, WEBP, BMP)
3. Atur jumlah warna dengan slider (3–10)
4. Palet warna muncul otomatis dengan kode HEX dan persentase dominansi

## Jalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```
