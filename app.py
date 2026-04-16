import streamlit as st
import pandas as pd
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Tracking Pengiriman Puskesmas", layout="wide")

st.title("🚚 Monitoring Pengiriman Barang")

# 1. Link CSV dari Google Sheets (Ganti dengan link kamu)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/XXXXX/pub?output=csv"

# Fungsi untuk mengambil data
def load_data():
    # Menambahkan cache agar tidak berat saat 1500 baris diproses
    df = pd.read_csv(SHEET_URL)
    return df

# 2. Fitur Refresh Otomatis (Setiap 5 detik)
# Streamlit akan menjalankan ulang script ini secara berkala
if "load_count" not in st.session_state:
    st.session_state.load_count = 0

placeholder = st.empty()

# Mengambil data terbaru
df = load_data()

# 3. Membuat Sidebar untuk Filter
st.sidebar.header("Filter Data")
kode_filter = st.sidebar.selectbox("Pilih Kode Puskesmas", options=["Semua"] + list(df['Kode Puskesmas'].unique()))

# Logika Filter
if kode_filter != "Semua":
    df_filtered = df[df['Kode Puskesmas'] == kode_filter]
else:
    df_filtered = df

# 4. Menampilkan Data di UI
with placeholder.container():
    col1, col2 = st.columns(2)
    col1.metric("Total Alamat", len(df_filtered))
    col2.metric("Terakhir Update", time.strftime("%H:%M:%S"))

    # Menampilkan tabel dengan 1500 data (scrollable)
    st.dataframe(df_filtered, use_container_width=True, height=500)

# Trigger refresh otomatis (Simulasi 5 detik)
time.sleep(5)
st.rerun()