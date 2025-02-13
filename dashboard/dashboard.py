import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
all_data_df = pd.read_csv('all_data_bike.csv')

# Streamlit app setup
st.title('Dashboard Data Rental Sepeda :sparkles:')
st.markdown("Pertanyaan : Bagaimana pola penggunaan sepeda berdasarkan musim? KDan kapan waktu paling sering untuk menyewa sepeda?.")

# Sidebar filter for year
st.sidebar.header("Filter Data")
musim_filter = st.sidebar.selectbox(
    'Pilih Musim:',
    ['All', 'Spring', 'Summer', 'Fall', 'Winter']
)

jam_filter = st.sidebar.slider(
    'Pilih Rentang Jam:',
    min_value=0,
    max_value=23,
    value=(0, 23),
    step=1
)

# Filter data based on selections
if musim_filter != 'All':
    jenis_musim = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    all_data_df = all_data_df[all_data_df['season'] == jenis_musim[musim_filter]]

all_data_df = all_data_df[(all_data_df['hr'] >= jam_filter[0]) & (all_data_df['hr'] <= jam_filter[1])]

# Bike Rentals by Season (Bar Chart)
st.subheader('Penyewaan Sepeda Berdasarkan Musim :cloud:')
hitung_musim = all_data_df.groupby("season")["cnt"].mean().reset_index()
hitung_musim['season'] = hitung_musim['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', data=hitung_musim, order=['Fall', 'Spring', 'Summer', 'Winter'], ax=ax)
ax.set_title('Penyewaan Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penyewaan')
ax.grid(axis="y", linestyle="--", alpha=0.5)
st.pyplot(fig)

st.subheader('Tren Penyewaan Sepeda Berdasarkan Jam :calendar:')
jam_tren = all_data_df.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='hr', y='cnt', data=jam_tren, ax=ax)
ax.set_title('Tren Penyewaan Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam dalam Sehari (0-23)')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_xticks(range(0, 24))
ax.grid(True)
st.pyplot(fig)

st.write('Kesimpulan : Bagaimana pola penggunaan sepeda berdasarkan musim? => Musim Panas (season 2) memiliki jumlah pengguna tertinggi, baik untuk casual maupun registered. Musim Dingin (season 4) memiliki jumlah pengguna terendah, mungkin karena cuaca yang lebih dingin mengurangi minat pengguna. Pengguna registered selalu lebih banyak dibandingkan casual, yang menunjukkan bahwa kebanyakan pengguna adalah pelanggan tetap. Musim Semi (season 1) memiliki lebih banyak penyewa dibandingkan Musim Dingin, tetapi masih lebih rendah dibandingkan Musim Gugur dan Musim Panas. Kapan waktu paling sering untuk menyewa sepeda? => Jam paling sibuk untuk menyewa sepeda adalah sekitar jam 7-9 pagi dan 17-19 sore. Penyewaan lebih rendah di malam hari (jam 0-5).')
