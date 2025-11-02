# Dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================
# Konfigurasi dasar
# ==========================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    page_icon="🚴"
)

st.title("🚴 Bike Sharing Dashboard")
st.caption("Analisis Tren Penyewaan Sepeda berdasarkan Data Harian dan Jam")

# ==========================
# Load Data
# ==========================
@st.cache_data
def load_data():
    day_url = "https://raw.githubusercontent.com/valdydrifto/Submission-1/refs/heads/main/Data/day.csv"
    hour_url = "https://raw.githubusercontent.com/valdydrifto/Submission-1/refs/heads/main/Data/hour.csv"
    day_df = pd.read_csv(day_url)
    hour_df = pd.read_csv(hour_url)
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar Filter
st.sidebar.header("⚙️ Filter")
year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=[2011, 2012],
    default=[2011, 2012]
)
month_filter = st.sidebar.slider("Pilih Bulan", 1, 12, (1, 12))

# Filter data
filtered_day = day_df[(day_df['yr'].replace({0: 2011, 1: 2012}).isin(year_filter)) &
                      (day_df['mnth'].between(month_filter[0], month_filter[1]))]

# ==========================
# EDA: Tren Tahunan & Bulanan
# ==========================
st.subheader("📊 Pertumbuhan Rata-rata Harian Penyewaan Sepeda")

avg_per_year = filtered_day.groupby('yr', observed=True)['cnt'].mean().reset_index()
avg_per_year['yr'] = avg_per_year['yr'].replace({0: 2011, 1: 2012})
growth_percent = ((avg_per_year.loc[avg_per_year['yr'] == 2012, 'cnt'].values[0] -
                   avg_per_year.loc[avg_per_year['yr'] == 2011, 'cnt'].values[0]) /
                   avg_per_year.loc[avg_per_year['yr'] == 2011, 'cnt'].values[0]) * 100

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Rata-rata Harian 2011", value=f"{avg_per_year.loc[avg_per_year['yr']==2011, 'cnt'].values[0]:.0f}")
with col2:
    st.metric(label="Rata-rata Harian 2012", value=f"{avg_per_year.loc[avg_per_year['yr']==2012, 'cnt'].values[0]:.0f}",
              delta=f"{growth_percent:.2f}%")

plt.figure(figsize=(8, 5))
sns.barplot(data=avg_per_year, x='yr', y='cnt', palette=['#5DADE2', '#F1948A'], alpha=0.8)
plt.title('Rata-rata Harian Penyewaan Sepeda per Tahun', fontsize=14, weight='bold')
plt.xlabel('Tahun')
plt.ylabel('Rata-rata Penyewaan (cnt)')
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
st.pyplot(plt)


# ==========================
# Analisis Jam Puncak
# ==========================
st.subheader("⏰ Jam Puncak Penyewaan (Casual vs Registered)")

hourly_usage = (
    hour_df.groupby('hr')[['casual', 'registered', 'cnt']]
    .mean()
    .reset_index()
)
peak_casual = hourly_usage.loc[hourly_usage['casual'].idxmax(), 'hr']
peak_registered = hourly_usage.loc[hourly_usage['registered'].idxmax(), 'hr']

plt.figure(figsize=(10, 5))
sns.lineplot(data=hourly_usage, x='hr', y='registered', marker='o', label='Registered', color='#2874A6')
sns.lineplot(data=hourly_usage, x='hr', y='casual', marker='o', label='Casual', color='#F39C12')

plt.title('⏰ Rata-rata Penyewaan Sepeda per Jam (Registered vs Casual)', fontsize=14, weight='bold')
plt.xlabel('Jam (0–23)')
plt.ylabel('Rata-rata Penyewaan')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Tipe Pengguna')

plt.axvline(x=peak_casual, color='#F39C12', linestyle='--', alpha=0.6)
plt.axvline(x=peak_registered, color='#2874A6', linestyle='--', alpha=0.6)

plt.tight_layout()
st.pyplot(plt)

# ==========================
# Insight & Kesimpulan
# ==========================
st.subheader("🧠 Insight & Kesimpulan")
st.markdown("""
- Terjadi peningkatan **sekitar 64.43%** rata-rata penyewaan harian dari tahun 2011 ke 2012.
- Pengguna **Registered** dominan di jam sibuk (08.00 dan 17.00), menandakan penggunaan untuk transportasi rutin.
- Pengguna **Casual** lebih aktif di siang hari dan akhir pekan.
- Aktivitas penyewaan mencapai puncak pada **musim panas dan gugur**.
- Faktor cuaca, musim, dan hari kerja berpengaruh kuat terhadap pola penyewaan.
""")

st.success("Analisis ini menunjukkan bahwa tren penyewaan sepeda meningkat tajam dari tahun ke tahun, dengan perbedaan pola antara pengguna rutin dan rekreasi yang dapat dimanfaatkan untuk strategi operasional dan pemasaran.")
