import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import re
import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Eco-Forest Valuation KPH Randublatung",
    page_icon="🌳",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>
.block-container { padding-top:1rem; }
[data-testid="stMetric"] {
    border-radius:18px; padding:18px;
    border:1px solid rgba(120,120,120,.2);
    background:rgba(120,120,120,.05);
}
h1,h2,h3 { font-weight:700; }
.identity-card {
    background:#dff0e4; border-radius:12px;
    padding:20px; color:#1f7a3f;
    margin-top:15px; margin-bottom:20px;
}
.identity-card p { margin-bottom:12px; font-size:18px; }
.desc-box {
    background:#dff0e4; border-radius:12px;
    padding:18px 22px; color:#1a5c32; margin-top:10px;
    font-size:15px; line-height:1.7;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD EXCEL
# =====================================================

try:
    raw = pd.read_excel("HUTAN.xlsx", header=None)
except:
    raw = pd.read_excel("HUTAN(1).xlsx", header=None)

# =====================================================
# HELPER
# =====================================================

def extract_number(val):
    if pd.isna(val) or isinstance(val, datetime.datetime):
        return None
    txt = str(val)
    m = re.search(r"[-+]?\d*\.?\d+", txt.replace(",", "."))
    return float(m.group()) if m else None

def fix_value(val):
    """Perbaiki nilai datetime yang salah baca dari Excel."""
    if isinstance(val, datetime.datetime):
        return "2 - 5"
    return val

def table_height(df):
    return min(650, max(200, (len(df) + 1) * 35))

# =====================================================
# EXTRACT TABLES — sesuai posisi spreadsheet
# =====================================================

# --- PROFIL HUTAN: rows 2-20, cols B-F (idx 1-5) ---
profil_hutan = raw.iloc[2:21, 1:6].copy()
profil_hutan.columns = ["Variable", "Value", "Unit", "Year", "Note"]
profil_hutan = profil_hutan.dropna(how="all").reset_index(drop=True)

# --- JASA EKOSISTEM: rows 2-9, cols H-I (idx 7-8) ---
produksi_kayu = raw.iloc[2:10, 7:9].copy()
produksi_kayu.columns = ["Komponen", "Nilai / Rentang"]
produksi_kayu = produksi_kayu.dropna(how="all").reset_index(drop=True)

# --- MASTER DATA: rows 2-36, cols K-O (idx 10-14) ---
# Termasuk: data umum, produksi, karbon, ekosistem,
#           conservation_efficiency, harga kayu, gross value
master_data = raw.iloc[2:37, 10:15].copy()
master_data.columns = ["Variable", "Value", "Unit", "Year", "Note"]
master_data["Value"] = master_data["Value"].apply(fix_value)
master_data = master_data.dropna(how="all").reset_index(drop=True)

# --- PARAMETER: rows 2-15, cols Q-U (idx 16-20) ---
parameter = raw.iloc[2:16, 16:21].copy()
parameter.columns = ["Parameter", "Nilai Dasar", "Min", "Max", "Satuan"]
parameter = parameter.dropna(how="all").reset_index(drop=True)

# =====================================================
# PARAMETER VALUES untuk kalkulasi
# =====================================================

luas_hutan   = float(parameter.loc[parameter["Parameter"] == "Luas Hutan",           "Nilai Dasar"].values[0])
produksi     = int  (parameter.loc[parameter["Parameter"] == "Produksi Kayu Tahunan","Nilai Dasar"].values[0])
harga_kayu   = int  (parameter.loc[parameter["Parameter"] == "Harga Kayu Jati",      "Nilai Dasar"].values[0])
stok_karbon  = float(parameter.loc[parameter["Parameter"] == "Stok Karbon",          "Nilai Dasar"].values[0])
harga_karbon = float(parameter.loc[parameter["Parameter"] == "Harga Karbon",         "Nilai Dasar"].values[0])
kurs_usd     = 16000

nilai_kayu   = produksi * harga_kayu
nilai_karbon = luas_hutan * stok_karbon * harga_karbon * kurs_usd
nilai_total  = nilai_kayu + nilai_karbon

# =====================================================
# LOGO
# =====================================================

try:
    logo = Image.open("Logo Unisbaa.png")
    st.sidebar.image(logo, use_container_width=True)
except:
    pass

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("## 🌳 Eco-Forest Valuation")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "Beranda",
        "Profil Hutan",
        "Produksi Kayu",
        "Master Data",
        "Parameter Simulasi",
        "Dashboard Summary",
    ]
)

# =====================================================
# BERANDA
# =====================================================

if menu == "Beranda":

    st.title("🌳 Eco-Forest Valuation KPH Randublatung")
    st.caption("PBL 6 - Ekonomi Sumber Daya Hutan")

    st.markdown("## Mata Kuliah")
    st.write("Ekonomi Sumber Daya Alam dan Lingkungan")

    st.markdown("## Dosen Pengampu")
    st.write("Yuhka Sundaya, S.E., M.Si.")

    st.markdown("""
        <div class="identity-card">
        <h4>KELOMPOK 5</h4>
        <p>• Brian Yusditama (10090224005)</p>
        <p>• Yolandi Abbas Wibisono (10090224010)</p>
        <p>• Dzulfiqar Didaf (10090224024)</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Ringkasan Data")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌳 Profil Hutan",  len(profil_hutan))
    c2.metric("🪵 Produksi Kayu", len(produksi_kayu))
    c3.metric("📊 Master Data",   len(master_data))
    c4.metric("⚙️ Parameter",     len(parameter))

    st.markdown("---")
    st.subheader("Deskripsi Dashboard")
    st.write("Dashboard ini digunakan untuk analisis dan valuasi ekonomi sumber daya hutan KPH Randublatung.")
    st.markdown("""
- Profil Hutan
- Produksi Kayu
- Master Data
- Parameter Simulasi
- Dashboard Summary
- Visualisasi Data Otomatis
- Analisis Valuasi Ekonomi Hutan
""")

# =====================================================
# PROFIL HUTAN
# =====================================================

elif menu == "Profil Hutan":

    st.title("🌳 Profil Hutan")

    st.dataframe(
        profil_hutan,
        use_container_width=True,
        hide_index=True,
        height=table_height(profil_hutan)
    )

    chart = profil_hutan[["Variable", "Value"]].copy()
    chart["Value"] = chart["Value"].apply(extract_number)
    chart = chart.dropna()

    fig = px.bar(
        chart, x="Variable", y="Value",
        color="Value", text="Value",
        title="Grafik Profil Hutan KPH Randublatung",
        labels={"Variable": "Variable", "Value": "Nilai"}
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(
        height=550, template="plotly_white",
        xaxis_tickangle=-35,
        coloraxis_colorbar=dict(title="Nilai")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class="desc-box">
        Profil hutan menggambarkan karakteristik utama KPH Randublatung yang berlokasi di Kabupaten Blora
        dan Grobogan, Jawa Tengah, dengan luas kawasan 32.425,55 ha. Hutan ini tergolong Hutan Produksi
        dengan kelas perusahaan Jati (Tectona grandis) sebagai komoditas utama dan estimasi tenaga kerja
        ±300 orang. Total produksi kayu tahunan mencapai 37.488 m³/tahun, terdiri dari tebang akhir
        26.242 m³, tebang tak terencana 7.498 m³, dan penjarangan 3.748 m³. Harga kayu jati berkisar
        Rp 3.500.000–5.500.000/m³, menghasilkan nilai bruto antara Rp 131,2 miliar (minimum) hingga
        Rp 206,2 miliar (maksimum) per tahun. Nilai NPV pengelolaan sebesar Rp 225.171.560/ha dengan
        IRR 17,24% dan BCR 3,00 menunjukkan kelayakan ekonomi yang sangat baik.
        </div>
    """, unsafe_allow_html=True)

# =====================================================
# PRODUKSI KAYU
# =====================================================

elif menu == "Produksi Kayu":

    st.title("🪵 Produksi Kayu")

    st.dataframe(
        produksi_kayu,
        use_container_width=True,
        hide_index=True
    )

    chart_je = produksi_kayu.copy()
    chart_je["Nilai Numerik"] = chart_je["Nilai / Rentang"].apply(extract_number)
    chart_je_num = chart_je.dropna(subset=["Nilai Numerik"])

    if not chart_je_num.empty:
        fig = px.bar(
            chart_je_num,
            x="Komponen", y="Nilai Numerik",
            color="Nilai Numerik", text="Nilai Numerik",
            title="Grafik Produksi Kayu KPH Randublatung",
            labels={"Komponen": "Komponen Produksi Kayu", "Nilai Numerik": "Nilai"}
        )
        fig.update_traces(texttemplate="%{text:,.2f}", textposition="outside")
        fig.update_layout(
            height=500, template="plotly_white",
            xaxis_tickangle=-20,
            coloraxis_colorbar=dict(title="Nilai")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class="desc-box">
        Data produksi kayu pada KPH Randublatung digunakan untuk menggambarkan manfaat ekonomi langsung
        yang diperoleh dari pemanfaatan hasil hutan, khususnya kayu jati sebagai komoditas utama.
        Stok karbon tegakan jati berkisar 144–190 ton CO₂/ha dengan harga karbon 5–15 USD/ton CO₂,
        menjadikan kawasan ini aset potensial dalam pasar karbon internasional. Fungsi regulasi air
        (indeks 0,7–0,9) dan kemampuan infiltrasi yang tinggi mencerminkan peran hidrologi kawasan.
        Tingkat erosi hutan jati rendah (2–5 ton/ha/tahun) dengan efisiensi konservasi tanah 75–90%.
        Keanekaragaman hayati berada pada level sedang dengan Indeks Shannon 1,2–1,8. Kombinasi antara
        nilai ekonomi hasil kayu dan nilai jasa lingkungan memberikan gambaran komprehensif manfaat
        total KPH Randublatung.
        </div>
    """, unsafe_allow_html=True)

# =====================================================
# MASTER DATA
# =====================================================

elif menu == "Master Data":

    st.title("📊 Master Data")

    st.dataframe(
        master_data,
        use_container_width=True,
        hide_index=True,
        height=table_height(master_data)
    )

    # Grafik: semua baris yang memiliki nilai numerik
    chart_md = master_data[["Variable", "Value"]].copy()
    chart_md["Value"] = chart_md["Value"].apply(extract_number)
    chart_md = chart_md.dropna()

    fig = px.bar(
        chart_md,
        x="Variable", y="Value",
        color="Value", text="Value",
        title="Grafik Master Data KPH Randublatung",
        labels={"Variable": "Variable", "Value": "Nilai"}
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(
        height=620, template="plotly_white",
        xaxis_tickangle=-40,
        coloraxis_colorbar=dict(title="Nilai")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class="desc-box">
        Master data memuat seluruh variabel kunci pengelolaan KPH Randublatung secara lengkap.
        Kawasan seluas 32.425,55 ha dikelola Perum Perhutani Divisi Regional Jawa Tengah di Kabupaten
        Blora dan Grobogan, terbagi dalam 2 wilayah, 6 Bagian Hutan (BH), 12 BKPH, dan 44 RPH
        dengan 296 karyawan. Luas produksi 28.082,8 ha, perlindungan 3.318,3 ha, dan penggunaan
        lain 1.037,6 ha. Produksi 2025: jati 35.045 m³ dan mahoni 2.443 m³ (total 37.488 m³/tahun).
        Stok karbon 144–190 ton CO₂/ha dengan total serapan 1.893.000 ton CO₂. Data ekosistem
        mencakup efisiensi konservasi 75–90%, erosi hutan 2–5 ton/ha/tahun, erosi lahan terbuka
        20–80 ton/ha/tahun, dan regulasi air 0,7–0,9. Harga kayu referensi: Rp 3.500.000 (min),
        Rp 4.500.000 (rata-rata), Rp 5.500.000 (maks)/m³, menghasilkan nilai produksi Rp 131,2–206,2
        miliar/tahun.
        </div>
    """, unsafe_allow_html=True)

# =====================================================
# PARAMETER SIMULASI
# =====================================================

elif menu == "Parameter Simulasi":

    st.title("⚙️ Parameter Simulasi")

    st.dataframe(
        parameter,
        use_container_width=True,
        hide_index=True
    )

    chart_param = parameter.copy()
    chart_param["Nilai Dasar"] = pd.to_numeric(
        chart_param["Nilai Dasar"], errors="coerce"
    )
    chart_param = chart_param.dropna(subset=["Nilai Dasar"])

    st.subheader("Grafik Parameter Simulasi")

    fig_param = px.bar(
        chart_param,
        x="Parameter", y="Nilai Dasar",
        color="Nilai Dasar",
        color_continuous_scale="Blues",
        text="Nilai Dasar",
        title="Grafik Parameter Simulasi KPH Randublatung",
        labels={"Parameter": "Parameter", "Nilai Dasar": "Nilai Dasar"}
    )
    fig_param.update_traces(texttemplate="%{text:,.2f}", textposition="outside")
    fig_param.update_layout(
        height=600, template="plotly_white",
        xaxis_tickangle=-35,
        coloraxis_colorbar=dict(title="Nilai Awal")
    )
    st.plotly_chart(fig_param, use_container_width=True)

    st.markdown("""
        <div class="desc-box">
        Terdapat 13 parameter simulasi dalam model valuasi KPH Randublatung: Luas Hutan (32.425,55 ha),
        Produksi Kayu Tahunan (37.488 m³/tahun), Harga Kayu Jati (Rp 4.500.000/m³), Stok Karbon
        (167 ton CO₂/ha), Harga Karbon (USD 10/ton CO₂), Regulasi Air (0,8), Erosi Hutan
        (3,5 ton/ha/tahun), Erosi Lahan Terbuka (50 ton/ha/tahun), Efisiensi Konservasi (82,5%),
        Indeks Shannon (1,5), Serapan CO₂ Total (1.893.000 ton CO₂), Luas Hutan Produksi
        (28.082,8 ha), dan Luas Hutan Lindung (3.318,3 ha). Gunakan slider di bawah untuk
        mensimulasikan berbagai skenario dan melihat dampaknya terhadap nilai ekonomi hutan.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    luas = st.slider(
        "Luas Hutan (ha)", 30000, 33000,
        int(luas_hutan), key="luas_hutan_slider"
    )
    produksi_sim = st.slider(
        "Produksi Kayu Tahunan (m³/tahun)", 35000, 39000,
        produksi, key="produksi_slider"
    )
    harga_sim = st.slider(
        "Harga Kayu Jati (Rp/m³)", 3500000, 5500000,
        harga_kayu, key="harga_kayu_slider"
    )
    karbon_sim = st.slider(
        "Harga Karbon (USD/ton CO₂)", 5, 15,
        int(harga_karbon), key="harga_karbon_slider"
    )

    nilai_kayu_sim   = produksi_sim * harga_sim
    nilai_karbon_sim = luas * stok_karbon * karbon_sim * kurs_usd
    total_sim        = nilai_kayu_sim + nilai_karbon_sim

    c1, c2, c3 = st.columns(3)
    c1.metric("Nilai Kayu",   f"Rp {nilai_kayu_sim:,.0f}")
    c2.metric("Nilai Karbon", f"Rp {nilai_karbon_sim:,.0f}")
    c3.metric("Nilai Total",  f"Rp {total_sim:,.0f}")

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

elif menu == "Dashboard Summary":

    st.title("📈 Dashboard Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("🌳 Luas Hutan",    f"{luas_hutan:,.2f} Ha")
    c2.metric("🪵 Produksi Kayu", f"{produksi:,.0f} m³/tahun")
    c3.metric("💰 Nilai Total",   f"Rp {nilai_total:,.0f}")

    st.markdown("---")

    # =============================================
    # KALKULASI NILAI
    # =============================================

    nilai_kayu_bruto   = produksi * harga_kayu          # gross_value_mid
    pes_karbon_tengah  = luas_hutan * stok_karbon * harga_karbon * kurs_usd
    hutan_pes_karbon   = nilai_kayu_bruto + pes_karbon_tengah
    konversi_jagung    = 648_510_000_000                # nilai alternatif konversi lahan jagung
    selisih_tradeoff   = hutan_pes_karbon - konversi_jagung
    status_str         = "Hutan + PES Karbon lebih tinggi secara ekonomi"

    # =============================================
    # TABEL SUMMARY — sesuai gambar
    # =============================================

    st.subheader("SUMMARY")

    summary_df = pd.DataFrame({
        "Indikator": [
            "Nilai Kayu Bruto",
            "PES Karbon Tengah",
            "Hutan + PES Karbon",
            "Konversi Jagung",
            "Selisih Trade-off",
            "Status",
        ],
        "Nilai": [
            f"Rp{nilai_kayu_bruto/1e9:,.2f}\nMiliar/tahun",
            f"Rp{pes_karbon_tengah/1e9:,.2f}\nMiliar/tahun",
            f"Rp{hutan_pes_karbon/1e12:,.3f}\nTriliun/tahun",
            f"Rp{konversi_jagung/1e9:,.2f}\nMiliar/tahun",
            f"Rp{selisih_tradeoff/1e9:,.2f}\nMiliar/tahun",
            status_str,
        ]
    })

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        height=280
    )

    st.markdown("---")

    # =============================================
    # GRAFIK TRADE-OFF
    # =============================================

    st.subheader("Grafik Trade-Off Analysis")

    tradeoff_chart = pd.DataFrame({
        "Indikator": [
            "Nilai Kayu Bruto",
            "PES Karbon Tengah",
            "Hutan + PES Karbon",
            "Konversi Jagung",
            "Selisih Trade-off",
        ],
        "Nilai (Miliar Rp)": [
            nilai_kayu_bruto  / 1_000_000_000,
            pes_karbon_tengah / 1_000_000_000,
            hutan_pes_karbon  / 1_000_000_000,
            konversi_jagung   / 1_000_000_000,
            selisih_tradeoff  / 1_000_000_000,
        ]
    })

    fig = px.bar(
        tradeoff_chart,
        x="Indikator", y="Nilai (Miliar Rp)",
        color="Nilai (Miliar Rp)",
        color_continuous_scale="Blues",
        text="Nilai (Miliar Rp)",
        title="Trade-Off Analysis Valuasi Ekonomi KPH Randublatung"
    )
    fig.update_traces(
        texttemplate="%{text:,.2f} M",
        textposition="outside"
    )
    fig.update_layout(
        height=550, template="plotly_white",
        showlegend=False,
        xaxis_tickangle=-15,
        xaxis_title="",
        yaxis_title="Miliar Rupiah",
        coloraxis_colorbar=dict(title="Miliar Rp")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class="desc-box">
        Dashboard Summary menyajikan hasil akhir valuasi ekonomi KPH Randublatung secara menyeluruh.
        Nilai Kayu Bruto dihitung dari produksi 37.488 m³/tahun × harga rata-rata Rp 4.500.000/m³
        = Rp 168,70 miliar/tahun. PES Karbon Tengah dihitung dari luas hutan × stok karbon 167 ton CO₂/ha
        × harga karbon USD 10/ton CO₂ × kurs Rp 16.000 = Rp 866,74 miliar/tahun. Total Hutan + PES Karbon
        mencapai Rp 1,035 triliun/tahun. Dibandingkan dengan nilai alternatif konversi lahan jagung
        sebesar Rp 648,51 miliar/tahun, terdapat selisih trade-off Rp 386,75 miliar/tahun yang
        menunjukkan bahwa mempertahankan fungsi hutan + PES Karbon lebih menguntungkan secara ekonomi
        dibanding konversi lahan.
        </div>
    """, unsafe_allow_html=True)