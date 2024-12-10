"""
Proje Başlığı: Ülkelere Göre İntihar Verileri Analizi
Yazarlar: Tuna DURUKAN (Laksy) ve Umut Kerim ACAR (ukerma)
Tarih: Aralık 2024
Kullanılan Data Seti: https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016
Kullanılan Programlama Dili: Python
Veri Referansları: 
- United Nations Development Program (2018)
- World Bank (2018)
- World Health Organization (2018)
Açıklama:
Bu proje, ülkelerin intihar verilerini analiz etmek için tasarlanmıştır. Özellikle seçilen
ülkeye ait veriler üzerinde istatistiksel analizler yapılmakta, görselleştirme yöntemleriyle
veriler detaylandırılmaktadır. pandas, seaborn, matplotlib ve scipy kütüphaneleri kullanılarak
veri işleme, analiz ve dağılım testleri gerçekleştirilmiştir.
"""

import pandas as pd # Veri işleme ve analiz                                     (pip install pandas)
import seaborn as sns # Gelişmiş veri görselleştirme                            (pip install seaborn)
import matplotlib.pyplot as plt # Grafik çizimi                                 (pip install matplotlib)
import numpy as np # Sayısal işlemler                                           (pip install numpy)
from scipy.stats import kstest # İstatistiksel testler                          (pip install scipy)

# Veri setinin yüklenmesi
dataPath = 'master.csv'
data = pd.read_csv(dataPath)

# Analiz yapılacak ülkenin belirlenmesi
country = 'Porto Rico'

# Veri setinden sadece seçilen ülkeye ait verilerin alınması ve orijinal veri setini bozmamak için kopya oluşturulması
countryData = data[data['country'] == country]
countryData = countryData.copy()

# Yeni bir sütun ekleyerek 'suicides/100k pop' değerlerini kopyalama
countryData.loc[:, 'suicides/100K pop'] = countryData['suicides/100k pop'] 

# Veri Temizleme: 'gdp_for_year ($)', virgüller kaldırılır ve değerleri float türüne çevirir
countryData.loc[:, ' gdp_for_year ($) '] = countryData[' gdp_for_year ($) '].replace(',', '', regex=True).astype(float)

# İstatistiksel Analiz Fonksiyonları
def calculateStatistics(data, column):
    mean = data[column].mean() # Ortalama hesaplama
    median = data[column].median() # Medyan hesaplama
    mode = data[column].mode()[0] if not data[column].mode().empty else None # Mod hesaplama (varsa)
    variance = data[column].var() # Varyans hesaplama
    std_dev = data[column].std() # Standart sapma hesaplama
    skewness = data[column].skew() # Çarpıklık hesaplama
    kurtosis = data[column].kurt() # Basıklık hesaplama

    return {
        'Mean': mean,
        'Median': median,
        'Mode': mode,
        'Variance': variance,
        'Standard Deviation': std_dev,
        'Skewness': skewness,
        'Kurtosis': kurtosis
    }

# İntihar oranları için istatistiklerin hesaplanması (100K üzerinden)
suicideStatsCountry = calculateStatistics(countryData, 'suicides/100K pop')

# Genel Bilgi ve Sonuçlar
print("\n═══════════════════════════════════ Genel Bilgi ve Sonuçlar ═══════════════════════════════════")
print(f"Veri Setindeki Toplam {country} Verisi: {len(countryData)}")

# İstatistikleri Yazdırma
print(f"\n═════════════════ {country} İntihar Oranı İstatistikleri (100K Üzerinden) ════════════════")
for statName, statValue in suicideStatsCountry.items():
    print(f"{statName:<20}: {statValue:.5f}")

# Kadın ve erkek intihar sayılarının yıllık toplamlarını hesaplama
genderData = countryData.groupby(['year', 'sex'])['suicides_no'].sum().unstack()

print("\n═════════════════════════════════ Kadın-Erkek Karşılaştırması ═════════════════════════════════\n", genderData)

# Yıllık bazda ortalama ve toplam verilerin hesaplanması
countryYearly = countryData.groupby('year').agg({
    'suicides/100K pop': 'mean', # Ortalama intihar oranı
    'suicides_no': 'sum', # Toplam intihar sayısı
    ' gdp_for_year ($) ': 'mean' # Ortalama GDP
}).reset_index()

print(f"\n══════════════════════ {country} Yıllık Ortalama ve Toplam Veriler ═══════════════════════")
print(countryYearly)

# Yaş gruplarına göre ortalama intihar oranlarının hesaplanması
countryAge = countryData.groupby(['year', 'age'])['suicides/100K pop'].mean().unstack()

print(f"\n════════ {country} Yaş Gruplarına Göre Ortalama İntihar Oranları (100K Üzerinden) ════════")
print(countryAge)

# Jenerasyonlara göre intihar sayıları ve GDP hesaplama
generationData = countryData.groupby('generation').agg({
    'suicides_no': 'sum',
    ' gdp_for_year ($) ': 'mean'
}).reset_index()

print(f"\n══════════════════ {country} Jenerasyonlara Göre İntihar Sayısı ve GDP ══════════════════")
print(generationData)

# Dağılım Testleri

# Normal dağılım testleri için veri hazırlanması
columnToAnalyze = 'suicides/100K pop'
dataToTest = countryData[columnToAnalyze] #.dropna()  # Kolonlar analiz edilip null olan veriler kaldırılır


# 1- Kolmogorov-Smirnov Testi (Normal Dağılıma Karşı)
ksStatNorm, ksPNorm = kstest(dataToTest, 'norm', args=(np.mean(dataToTest), np.std(dataToTest)))
print("\n═══════════════════════════ Kolmogorov-Smirnov Test (Normal Dağılım) ══════════════════════════")
print(f"  Test İstatistiği: {ksStatNorm:.5f}, P-Değeri: {ksPNorm:.5f}")
if ksPNorm > 0.05:
    print("  Sonuç: Veri normal dağılıma uygundur.")
else:
    print("  Sonuç: Veri normal dağılıma uygun değildir.")

# 2- Kolmogorov-Smirnov Testi (Poisson Dağılıma Karşı)
lambdaPoisson = np.mean(dataToTest)
ksStatPoisson, ksPPoisson = kstest(dataToTest, 'poisson', args=(lambdaPoisson,))
print("\n══════════════════════════ Kolmogorov-Smirnov Test (Poisson Dağılım) ══════════════════════════")
print(f"  Test İstatistiği: {ksStatPoisson:.5f}, P-Değeri: {ksPPoisson:.5f}")
if ksPPoisson > 0.05:
    print("  Sonuç: Veri Poisson dağılıma uygundur.")
else:
    print("  Sonuç: Veri Poisson dağılıma uygun değildir.")

# 3- Eksponansiyel Dağılım Testi
ksStatExpon, ksPExpon = kstest(dataToTest, 'expon', args=(np.min(dataToTest), np.mean(dataToTest)))
print("\n═══════════════════════ Kolmogorov-Smirnov Test (Eksponansiyel Dağılım) ═══════════════════════")
print(f"  Test İstatistiği: {ksStatExpon:.5f}, P-Değeri: {ksPExpon:.5f}")
if ksPExpon > 0.05:
    print("  Sonuç: Veri eksponansiyel dağılıma uygundur.")
else:
    print("  Sonuç: Veri eksponansiyel dağılıma uygun değildir.\n")

# Görselleştirme
genderData['total'] = genderData['male'] + genderData['female']

plt.figure(figsize=(10, 6))
plt.bar(genderData.index, genderData['total'], color='purple', alpha=0.7, edgecolor='black', label='Toplam İntihar Sayısı')
plt.title(f'{country} Toplam İntihar Sayısı', fontsize=14)
plt.xlabel('Yıl', fontsize=12)
plt.ylabel('İntihar Sayısı', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# Kadın ve erkek intihar sayılarının karşılaştırılması
plt.figure(figsize=(10, 6))
plt.plot(genderData.index, genderData['male'], marker='o', label='Erkek', color='blue')
plt.plot(genderData.index, genderData['female'], marker='o', label='Kadın', color='pink')
plt.title(f'{country} Kadın ve Erkek İntihar Sayıları Karşılaştırması', fontsize=14)
plt.xlabel('Yıl', fontsize=12)
plt.ylabel('İntihar Sayısı', fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# GDP ve intihar sayısı arasındaki ilişki için grafik
fig, ax1 = plt.subplots(figsize=(12, 8))

# GDP için çizgi grafiği
ax1.plot(countryYearly['year'], countryYearly[' gdp_for_year ($) '], color='black', marker='o', label='GDP')
ax1.set_xlabel('Yıl', fontsize=12)
ax1.set_ylabel('GDP ($)', fontsize=12, color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# İntihar sayısı için çubuk grafiği
ax2 = ax1.twinx()
ax2.bar(countryYearly['year'], countryYearly['suicides_no'], alpha=0.6, color='skyblue', label='İntihar Sayısı')
ax2.set_ylabel('İntihar Sayısı', fontsize=12, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Başlık
fig.suptitle(f'{country} GDP ve İntihar Sayısı Arasındaki Bağlantı', fontsize=14)
fig.tight_layout()
plt.show()

# Jenerasyon ve İntihar Sayısı
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(generationData['generation'], generationData['suicides_no'], color='skyblue', edgecolor='black', label='İntihar Sayısı')
ax.set_xlabel('Jenerasyon', fontsize=12)
ax.set_ylabel('İntihar Sayısı', fontsize=12, color='blue')
ax2 = ax.twinx()
plt.title(f'{country} Jenerasyonlara Göre İntihar Sayısı', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Yaş Gruplarına Göre İntihar Oranları
plt.figure(figsize=(12, 8))
for age_group in countryAge.columns:
    plt.plot(countryAge.index, countryAge[age_group], marker='o', label=age_group)
plt.title(f'{country} Yaş Gruplarına Göre İntihar Oranları (100K Üzerinden)', fontsize=14)
plt.xlabel('Yıl', fontsize=12)
plt.ylabel('İntihar Oranı (100K)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title="Yaş Grupları", fontsize=12)
plt.tight_layout()
plt.show()

# İntihar Oranı ve GDP Arasındaki Dağılım
plt.figure(figsize=(10, 6))
plt.scatter(countryData[' gdp_for_year ($) '], countryData['suicides/100K pop'], alpha=0.7, color='purple')
plt.title(f'{country} GDP ve İntihar Oranı Arasındaki Dağılım', fontsize=14)
plt.xlabel('GDP ($)', fontsize=12)
plt.ylabel('İntihar Oranı (100K)', fontsize=12)
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Mean, Median, Mode, Variance ve Standard Deviation Görselleştirme
plt.figure(figsize=(12, 6))

# Histogram ve KDE
sns.histplot(countryData['suicides/100K pop'], bins=20, kde=True, color='skyblue', label='Histogram ve KDE')

# Ortalama (Mean)
plt.axvline(x=suicideStatsCountry['Mean'], color='blue', linestyle='--', label=f"Mean (Ortalama): {suicideStatsCountry['Mean']:.2f}")

# Medyan (Median)
plt.axvline(x=suicideStatsCountry['Median'], color='orange', linestyle='--', label=f"Median (Medyan): {suicideStatsCountry['Median']:.2f}")

# Mod (Mode)
if suicideStatsCountry['Mode'] is not None:
    plt.axvline(x=suicideStatsCountry['Mode'], color='green', linestyle='--', label=f"Mode (Mod): {suicideStatsCountry['Mode']:.2f}")

# Varyans (Variance)
plt.axvline(x=suicideStatsCountry['Mean'] + suicideStatsCountry['Variance'], color='purple', linestyle='--', label=f"Variance (Varyans): {suicideStatsCountry['Variance']:.2f}")

# Standart Sapma (Standard Deviation) - Pozitif Yönde
plt.axvline(x=suicideStatsCountry['Mean'] + suicideStatsCountry['Standard Deviation'], color='red', linestyle='--', label=f"Std Dev (+): {suicideStatsCountry['Standard Deviation']:.2f}")

# Standart Sapma (Standard Deviation) - Negatif Yönde
plt.axvline(x=suicideStatsCountry['Mean'] - suicideStatsCountry['Standard Deviation'], color='red', linestyle='--', label=f"Std Dev (-): {suicideStatsCountry['Standard Deviation']:.2f}")

# Başlık ve Eksen Etiketleri
plt.title(f"{country} İntihar Oranları İçin İstatistiksel Ölçütler", fontsize=14)
plt.xlabel('İntihar Oranı (100K Üzerinden)', fontsize=12)
plt.ylabel('Yoğunluk', fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()