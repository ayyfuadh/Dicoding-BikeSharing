import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Setting Layout
st.set_page_config(layout="wide")

# Add Title and Tabs
st.title("Proyek Analisis Data: Bike Sharing Dataset")
tab1, tab2 = st.tabs(["Pertanyaan 1", "Pertanyaan 2"])

# Import Dataframe
day_df = pd.read_csv("day.csv")

# Change the Data Type of the "dteday" Column 
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Add Content to Tab 1
with tab1:
    st.header("Musim apa yang paling banyak menyewakan sepeda?")
    # Membuat agregasi musiman
    seasonal_agg = day_df.groupby("season").agg({
        "instant": "nunique",  # Jumlah unik dari instant untuk setiap musim
        "cnt": ["mean"]         # Rata-rata dari cnt untuk setiap musim
    })

    # Mengatur ulang indeks agar kolom season menjadi kolom biasa
    seasonal_agg = seasonal_agg.reset_index()

    # Mengganti angka musim dengan nama musim
    seasonal_agg["season"] = ["Spring", "Summer", "Fall", "Winter"]

    # Menyiapkan plot
    plt.figure(figsize=(8, 6))

    # Membuat bar plot
    plt.bar(seasonal_agg["season"],          # Menggunakan nama musim sebagai sumbu x
            seasonal_agg[("cnt", "mean")])   # Menggunakan rata-rata cnt sebagai sumbu y

    # Menambahkan label pada setiap bar
    for i in range(len(seasonal_agg["season"])):
        plt.text(i, seasonal_agg[("cnt", "mean")][i], # Menambahkan teks dengan nilai cnt
                 str(int(seasonal_agg[("cnt", "mean")][i])), # Mengonversi nilai cnt menjadi string
                 ha="center", va="bottom") # Posisi teks pada bar

    # Menambahkan judul dan label sumbu
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Rata-rata Penyewaan")

    # Menampilkan grid
    plt.grid(axis="y")

    # Menampilkan plot
    st.pyplot(plt)

    st.caption("Berdasarkan grafik untuk pertanyaan no.1 Musim dengan penyewaan sepeda tertinggi adalah Musim Gugur.")

# Add Content to Tab 2
with tab2:
    st.header("Pada tahun berapa permintaan penyewaan sepeda terbanyak dan terendah?")
    # Mengelompokkan data harian menjadi data bulanan dan menghitung total penyewaan sepeda setiap bulan
    monthly_df = day_df.resample('M', on='dteday').sum()

    # Visualisasi
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_df.index, monthly_df['cnt'], color='#6499E9')
    plt.xlabel('Bulan dan Tahun')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.title('Penyewaan Sepeda Sepanjang Waktu (Berdasarkan Bulan dan Tahun)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    # Menampilkan kesimpulan
    max_year = monthly_df['cnt'].idxmax().year
    min_year = monthly_df['cnt'].idxmin().year
    st.write(f"Berdasarkan grafik untuk pertanyaan no.2 tahun dengan jumlah penyewaan sepeda terbanyak adalah {max_year}, sementara tahun dengan jumlah penyewaan sepeda terendah adalah {min_year}.")
