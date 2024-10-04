import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.write(
    """
    # Dashboard Submission
    Belajar analisis data dengan Python oleh M. Muslih Attoyibi
    """
)

st.write("Di sini, kita akan mencoba menganalisis data Air-quality-dataset : https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view")
st.write("Analisis ini dilakukan untuk menjawab dua buah pertanyaan, yakni : ")
st.write("1. Bagaimana perbandingan kualitas udara di setiap station berdasarkan konsentrasi rata-rata NO2/Nitrogennya?")
st.write("2. Bagaimana perkembangan suhu rata-rata di station Gucheng dari tahun 2013 sampai tahun 2017?")

# Load datasets
df_1 = pd.read_csv("PRSA_Data_Tiantan_20130301-20170228.csv", delimiter=",")
df_2 = pd.read_csv("PRSA_Data_Gucheng_20130301-20170228.csv", delimiter=",")
df_3 = pd.read_csv("PRSA_Data_Aotizhongxin_20130301-20170228.csv", delimiter=",")
df_4 = pd.read_csv("PRSA_Data_Changping_20130301-20170228.csv", delimiter=",")
df_5 = pd.read_csv("PRSA_Data_Dingling_20130301-20170228.csv", delimiter=",")
df_6 = pd.read_csv("PRSA_Data_Dongsi_20130301-20170228.csv", delimiter=",")
df_7 = pd.read_csv("PRSA_Data_Guanyuan_20130301-20170228.csv", delimiter=",")
df_8 = pd.read_csv("PRSA_Data_Huairou_20130301-20170228.csv", delimiter=",")
df_9 = pd.read_csv("PRSA_Data_Nongzhanguan_20130301-20170228.csv", delimiter=",")
df_10 = pd.read_csv("PRSA_Data_Shunyi_20130301-20170228.csv", delimiter=",")
df_11 = pd.read_csv("PRSA_Data_Wanliu_20130301-20170228.csv", delimiter=",")
df_12 = pd.read_csv("PRSA_Data_Wanshouxigong_20130301-20170228.csv", delimiter=",")

dataframes = [df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10, df_11, df_12]

# Merge dataframes
df_merged = pd.concat(dataframes, ignore_index=True)

st.write("Menghitung Missing values :")
st.write(df_merged.isnull().sum())
st.write("------------------------------------")
st.write("Menghitung data duplikat :")
st.write(df_merged.duplicated().sum())
st.write("------------------------------------")
st.write("Menghitung outlier")

# Calculate outliers
numeric_column = df_merged.select_dtypes(include=[np.number]).drop(columns=["No"], errors='ignore')

q25 = numeric_column.quantile(0.25)
q75 = numeric_column.quantile(0.75)

iqr = q75 - q25

lower_bound = q25 - 1.5 * iqr
upper_bound = q75 + 1.5 * iqr

outliers = (numeric_column < lower_bound) | (numeric_column > upper_bound)

st.write("Nilai ambang bawah :")
st.write(lower_bound)
st.write("Nilai ambang atas :")
st.write(upper_bound)
st.write("Jumlah outlier pada masing-masing kolom :")
st.write(outliers.sum())

st.write("Pada tahap di atas, kita telah meng-handle kecacatan data yang ditemukan pada tahap assessing data. Karena dataframe tidak memiliki data duplikat, maka yang harus kita bersihkan berupa missing values dan outliers dengan cara : ")
st.write("Row data dengan missing values akan di drop/ dihilangkan")
st.write("Nilai outlier akan didrop")

# Clean the dataframe
df_clean = df_merged.dropna(axis=0, how='any')
st.write("Jumlah missing value setelah dibersihkan : ")
st.write(df_clean.isnull().sum())
st.write("---------------------")

numeric_column = df_clean.select_dtypes(include=[np.number]).drop(columns=["No"], errors='ignore')

q25 = numeric_column.quantile(0.25)
q75 = numeric_column.quantile(0.75)

iqr = q75 - q25

lower_bound = q25 - 1.5 * iqr
upper_bound = q75 + 1.5 * iqr

outliers = (numeric_column < lower_bound) | (numeric_column > upper_bound)
df_clean = df_clean[~outliers.any(axis=1)]

mean_no2_station = df_clean.groupby("station")["NO2"].mean()

for station, mean_no2 in mean_no2_station.items():
    st.write(f"Mean NO2 value for {station}: {mean_no2}")

mean_no2_dict = df_clean.groupby("station")["NO2"].mean().to_dict()

plt.figure(figsize=(10, 6))
plt.bar(mean_no2_dict.keys(), mean_no2_dict.values(), color='b')
plt.title("Nilai Rata-Rata NO2 per Station")
plt.xlabel("Station")
plt.ylabel("Rata-Rata nilai NO2")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
st.pyplot(plt)

st.write("Data NO2 dikelompokkan berdasarkan station lalu diambil nilai rata-ratanya berdasarkan kelompok tersebut. Setelah itu, kita ubah menjadi tipe data dictionary dengan Nama station sebagai 'key' dan rata-rata NO2 sebagai 'value'nya. Kemudian kita visualisasikan bar chart untuk melihat tingkat konsentrasi NO2 di setiap station.")

mean_temp_gucheng = df_clean[df_clean["station"] == "Gucheng"].groupby("year")["TEMP"].mean()

st.write(mean_temp_gucheng)

plt.figure(figsize=(10, 6))
plt.plot(mean_temp_gucheng.index, mean_temp_gucheng.values, marker="o", linestyle="-", color="b", label="Mean Temperature")
plt.title("Temperature rata-rata di station Gucheng dari tahun 2013 s/d 2017")
plt.xlabel("Tahun")
plt.ylabel("Mean Temperature (°C)")
plt.xticks(mean_temp_gucheng.index)  
plt.grid()
plt.legend()
plt.tight_layout()
st.pyplot(plt)

st.write("Di sini, kita hanya mengambil data dengan value station = 'Gucheng'. Data tersebut kemudian kita kelompokkan berdasarkan tahunnya lalu kita ambil nilai rata-rata temperature di station Gucheng berdasarkan tahun. Kemudian datanya kita visualisasikan dengan line chart untuk melihat perkembangan suhu rata-rata setiap tahunnya.")

st.write("Konklusi akhir")
st.write("Conclution pertanyaan 1 Berdasarkan visualisasi data, dapat dilihat bahwa setiap station memiliki nilai NO2 yang beragam. Semakin tinggi nilai NO2, maka semakin buruk kualitas udara di daerah tersebut. Bisa kita lihat pada chart bahwa station Dingling memiliki tingkat konsentrasi NO2 yang paling kecil. Maka station Dingling memiliki kualitas udara terbaik jika dilihat dari konsentrasi NO2 nya saja. Sebaliknya, station Wanliu memiliki konsentrasi NO2 yang sangat tinggi yang mana menyebabkannya memiliki kualitas udara terburuk.")
st.write("Conclution pertanyaan 2 Berdasarkan chart, temperature rata-rata di stasiun Gucheng menurun setiap tahunnya, penurunan paling signifikan terjadi pada tahun 2016 menuju 2017 yang asalnya 13,8 derajat menjadi 0,27 derajat saja.")
