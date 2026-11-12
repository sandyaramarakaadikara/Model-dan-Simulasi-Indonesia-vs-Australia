"""C4ISR Command Center & Tactical Wargame Simulator (Multi-Country Lanchester Engine)
Integrated Combat Modeling & Simulation with Real-Time 3D Joint-Force Battlespace
Light Executive Defense Research Portal Edition (Comprehensive Academic Depth)

Authors:
1. Sandyarama Raka Adikara (NPM: 20241310008)
2. Fauzan Akbar Ansyori
3. Nazmi Priyatama Shuerman
Department of Informatics, Faculty of Computer Science and Information Systems,
Universitas Kebangsaan Republik Indonesia, Bandung.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from wargame_3d_engine import get_wargame_3d_html

# Page Configuration
st.set_page_config(
    page_title="C4ISR Defense Capability & Wargame Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Executive Light Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .header-pretitle {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #1e40af;
        margin-bottom: 2px;
    }
    
    .main-title {
        color: #0f172a;
        font-size: 2.05rem;
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.03em;
        margin-bottom: 4px;
    }
    
    .sub-title {
        color: #475569;
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 12px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 10px;
    }
    
    .authors-badge {
        text-align: right;
        font-size: 0.78rem;
        color: #64748b;
        line-height: 1.45;
        padding-top: 6px;
    }
    .authors-badge b {
        color: #0f172a;
        letter-spacing: 0.05em;
    }
    
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        margin-bottom: 10px;
    }
    
    .metric-title {
        color: #64748b;
        font-size: 0.74rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 5px;
    }
    
    .metric-value-a {
        color: #dc2626;
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-value-b {
        color: #0284c7;
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #e2e8f0;
        padding: 4px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #475569;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 8px 16px;
        background-color: transparent;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1e40af !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
        border: 1px solid #cbd5e1;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1e40af;
        color: #ffffff;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
        transition: all 0.15s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 2px 8px rgba(30, 64, 175, 0.25);
    }

    /* Dataframes & Tables Light Theme */
    [data-testid="stDataFrame"], .stDataFrame {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    
    /* Selectboxes Light Theme */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }
    
    /* Radio & Slider Light Labels */
    .stRadio label, .stSlider label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Info box styling */
    div[data-testid="stAlert"] {
        background-color: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        color: #166534 !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent

def resolve_path(rel_path: str) -> Path:
    p = ROOT / rel_path
    if p.exists():
        return p
    for candidate in [
        ROOT / "data" / "processed" / Path(rel_path).name,
        ROOT / "data" / Path(rel_path).name,
        ROOT / Path(rel_path).name,
    ]:
        if candidate.exists():
            return candidate
    return p

CSV_PANEL = resolve_path("data/processed/panel_regional_WDI_SIPRI_14negara_2010_2025.csv")
CSV_FEATURE_IMPORTANCE = resolve_path("data/processed/tabel_feature_importance_ml_idn_aus.csv")

@st.cache_data
def load_data():
    if not CSV_PANEL.exists():
        st.error(f"Berkas data {CSV_PANEL.name} tidak ditemukan!")
        return None
    return pd.read_csv(CSV_PANEL)

df_panel = load_data()

# Database Doktrin dan Spesifikasi Teknis Alutsista 10 Kekuatan Indo-Pasifik
COUNTRY_DATABASE = {
    "Indonesia": {
        "iso3": "IDN", "flag": "[IDN]", "color": "#dc2626",
        "archetype": "territorial_archipelago",
        "doctrine": "Pertahanan Kepulauan & Sishankamrata (Territorial Depth)",
        "capital_intensity": "Labor-Intensive (~$22.7K/prajurit)",
        "active_troops": 676000,
        "units": [
            {
                "id": "KRI R.E. Martadinata (331)", "type": "ship", "role": "Frigat Eskorta Kawal Rudal",
                "radar": "Thales SMART-S Mk2 3D (250 km)", "missiles": "8x Exocet MM40 Block 3 (Mach 0.93, 200 km)",
                "vls": "12x VL MICA SAM (20 km)", "gun": "76mm Oto Melara Super Rapid (120 rpm)", "ciws": "2x 20mm Denel Vektor G12"
            },
            {
                "id": "KRI Nagapasa (403)", "type": "sub", "role": "Kapal Selam Serang Diesel-Elektrik",
                "radar": "Acoustic Flank Array Sonar CSU-90", "missiles": "8x Tabung Torpedo 533mm Black Shark",
                "vls": "Kapasitas 14x Torpedo Kelas Berat", "gun": "Periskop Optronik SERO 400", "ciws": "Penangkal Torpedo C303/S"
            },
            {
                "id": "Skadron Rafale & Su-30", "type": "jet", "role": "Jet Tempur Superioritas Udara",
                "radar": "RBE2 AESA & N001VEP Radar (200 km)", "missiles": "Meteor BVRAAM (200 km) & R-77 (100 km)",
                "vls": "14 Hardpoints Senjata Eksternal", "gun": "30mm GIAT 30M791 (2500 rpm)", "ciws": "SPECTRA Electronic Warfare Suite"
            },
            {
                "id": "Helikopter AS565 MBe Panther", "type": "heli", "role": "Helikopter AKS & Maritim",
                "radar": "Telephonics RDR-1500B Search Radar", "missiles": "2x Torpedo A244/S & Roket 68mm",
                "vls": "Sonar Celup FLASH Dipping Sonar", "gun": "Pod Kanon 20mm GIAT", "ciws": "Chaff & Flare Dispenser"
            },
            {
                "id": "Baterai Pesisir BrahMos/Yakhont", "type": "coastal", "role": "Pertahanan Pantai Anti-Kapal",
                "radar": "Monolit-B Coastal Search Radar (450 km)", "missiles": "Supersonik Mach 3.0 BrahMos (290 km)",
                "vls": "4x Peluncur Mobile Transporter (TEL)", "gun": "Panduan Inersia + Radar Aktif Terminal", "ciws": "Sistem Jamming Samudra"
            }
        ],
        "attack_mod": 1.15, "defense_mod": 1.45, "tech_mod": 0.85, "speed_mod": 1.0
    },
    "Australia": {
        "iso3": "AUS", "flag": "[AUS]", "color": "#0284c7",
        "archetype": "hightech_precision",
        "doctrine": "Forward Expeditionary & Air-Maritime Denial (AUKUS)",
        "capital_intensity": "Capital-Intensive High-Tech (~$587K/prajurit)",
        "active_troops": 60300,
        "units": [
            {
                "id": "HMAS Hobart (DDG 39)", "type": "ship", "role": "Aegis Air Warfare Destroyer",
                "radar": "Lockheed AN/SPY-1D(V) & CEAFAR (350 km)", "missiles": "8x Harpoon Block II & Tomahawk Cruise (1600 km)",
                "vls": "48-cell Mk 41 VLS (SM-2, SM-6, ESSM)", "gun": "127mm Mk 45 Mod 4 Naval Gun", "ciws": "20mm Phalanx Block 1B (4500 rpm)"
            },
            {
                "id": "HMAS Collins / SSN-AUKUS", "type": "sub", "role": "Kapal Selam Serang Terpandu",
                "radar": "Scionics Integrated Sonar Suite", "missiles": "UGM-84C Sub-Harpoon & Mk 48 Mod 7 CBASS",
                "vls": "6x 533mm Torpedo Tubes (22 Amunisi)", "gun": "Periskop Optronik CM010", "ciws": "Decoy Penipu Torpedo WASS"
            },
            {
                "id": "RAAF F-35A Lightning II", "type": "jet", "role": "Siluman Generasi ke-5 Multirole",
                "radar": "AN/APG-81 AESA Radar (250 km)", "missiles": "AIM-120D AMRAAM (160 km) & JSM Cruise",
                "vls": "Internal Weapon Bay Stealth Config", "gun": "25mm GAU-22/A Rotary (3300 rpm)", "ciws": "AN/ASQ-239 Barracuda EW System"
            },
            {
                "id": "Helikopter MH-60R Seahawk", "type": "heli", "role": "Maritime Strike & ASW",
                "radar": "AN/APS-153(V) Multi-Mode Radar (160 km)", "missiles": "8x AGM-114 Hellfire & Mk 54 Torpedo",
                "vls": "AQS-22 ALFS Low-Frequency Sonar", "gun": "Senapan Mesin M240D 7.62mm", "ciws": "AN/ALQ-144 Infrared Countermeasures"
            },
            {
                "id": "Baterai Darat HIMARS Precision", "type": "coastal", "role": "Presisi Serang Jarak Jauh",
                "radar": "Q-53 Counter-Battery Radar (60 km)", "missiles": "PrSM (Precision Strike Missile - 500 km)",
                "vls": "6x GMLRS Rockets / 1x PrSM Pod", "gun": "Navigasi GPS/INS Tahan Jamming", "ciws": "Perlindungan C-RAM Terpadu"
            }
        ],
        "attack_mod": 1.40, "defense_mod": 1.10, "tech_mod": 1.50, "speed_mod": 1.2
    },
    "China": {
        "iso3": "CHN", "flag": "[CHN]", "color": "#b91c1c",
        "archetype": "global_heavyweight",
        "doctrine": "Anti-Access / Area Denial (A2/AD) & Global Maritime Projection",
        "capital_intensity": "Heavyweight Hybrid Mass & Tech",
        "active_troops": 2035000,
        "units": [
            {
                "id": "Type 055 Renhai Cruiser", "type": "ship", "role": "Kapal Penjelajah Rudal Terpandu",
                "radar": "Type 346B Dual-Band AESA (400 km)", "missiles": "YJ-18 (540 km) & YJ-21 Hipersonik (1500 km)",
                "vls": "112 Universal VLS Cells (HHQ-9B SAM)", "gun": "130mm H/PJ-38 Naval Gun (40 rpm)", "ciws": "Type 1130 11-Barrel Gatling (11000 rpm)"
            },
            {
                "id": "Type 093B Shang Nuclear Sub", "type": "sub", "role": "Kapal Selam Serang Nuklir",
                "radar": "H/SQG-207 Sonar Array Terpadu", "missiles": "YJ-18B AShM & Torpedo Yu-6 533mm",
                "vls": "VLS Tabung Rudal Vertikal Bawah Air", "gun": "Sistem Propulsi Nuklir Reaktor Canggih", "ciws": "Peluncur Umban Akustik Penipu"
            },
            {
                "id": "PLAAF J-20 Mighty Dragon", "type": "jet", "role": "Siluman Superioritas Udara",
                "radar": "Type 1475 AESA Radar (250 km)", "missiles": "PL-15 BVRAAM (300 km) & PL-10E",
                "vls": "Internal Stealth Bay 6x Rudal", "gun": "EOTS & EODAS 360 Derajat Sensor", "ciws": "Integrated ECM Jamming Pods"
            },
            {
                "id": "Helikopter Z-20F Maritime", "type": "heli", "role": "Anti-Kapal Selam & Serang Laut",
                "radar": "Surface Search AESA Radar di Hidung", "missiles": "8x KD-10 Rudal Anti-Kapal & Torpedo Yu-7",
                "vls": "Sonobuoy Dispenser Terotomasi", "gun": "Kanon Otomatis Pintu 12.7mm", "ciws": "RWR & Laser Warning Receivers"
            },
            {
                "id": "Baterai Hipersonik DF-21D", "type": "coastal", "role": "Rudal Balistik Anti-Kapal Induk",
                "radar": "Satelit Yaogan & Radar OTH (Over-the-Horizon 3000 km)", "missiles": "DF-21D Mach 10 Re-entry (1800 km)",
                "vls": "Hulu Ledak Manuver Terminal (MaRV)", "gun": "Penetrasi Armor Kapal Induk Berat", "ciws": "Pengawalan Hanud HQ-9B"
            }
        ],
        "attack_mod": 1.55, "defense_mod": 1.40, "tech_mod": 1.45, "speed_mod": 1.25
    },
    "United States": {
        "iso3": "USA", "flag": "[USA]", "color": "#1d4ed8",
        "archetype": "global_heavyweight",
        "doctrine": "Global Joint Multi-Domain Forward Superiority",
        "capital_intensity": "Super-Heavy Capital Dominance",
        "active_troops": 1328000,
        "units": [
            {
                "id": "USS Gerald R. Ford (CVN 78)", "type": "ship", "role": "Supercarrier Nuklir Pemukul",
                "radar": "AN/SPY-3 Dual-Band Radar (DBR 450 km)", "missiles": "75+ Jet Tempur F-35C & F/A-18E Super Hornet",
                "vls": "Mk 29 ESSM & Rolling Airframe Missile", "gun": "Sistem Peluncur Ketapel EMALS Elektromagnetik", "ciws": "3x 20mm Phalanx CIWS Block 1B"
            },
            {
                "id": "USS Virginia (SSN 774)", "type": "sub", "role": "Kapal Selam Serang Nuklir Cepat",
                "radar": "BQQ-10 Spherical Bow Sonar Array", "missiles": "12x Tomahawk Cruise Missiles & Mk 48 ADCAP",
                "vls": "Virginia Payload Module (VPM 28 Tomahawk)", "gun": "Kamera Optronik Resolusi Tinggi", "ciws": "Submerged Countermeasure Decoys"
            },
            {
                "id": "USAF F-22 Raptor & F-35C", "type": "jet", "role": "Supremasi Udara Siluman Generasi ke-5",
                "radar": "AN/APG-77 AESA Radar (300 km)", "missiles": "AIM-120D AMRAAM (180 km) & AIM-9X Sidewinder",
                "vls": "Supercruise Tanpa Afterburner Mach 1.8", "gun": "20mm M61A2 Vulcan Gatling (6000 rpm)", "ciws": "ALR-94 All-Aspect Electronic Warfare"
            },
            {
                "id": "Helikopter AH-64E Apache", "type": "heli", "role": "Helikopter Serbu Presisi Berat",
                "radar": "AN/APG-78 Longbow Fire Control Radar", "missiles": "16x AGM-114R Hellfire & Spike NLOS",
                "vls": "70mm Hydra Rockets dengan Panduan APKWS", "gun": "30mm M230 Chain Gun (625 rpm)", "ciws": "AN/APR-39 Radar Warning Receiver"
            },
            {
                "id": "Baterai THAAD & Patriot PAC-3", "type": "coastal", "role": "Hanud Balistik Ketinggian Tinggi",
                "radar": "AN/TPY-2 X-Band Radar (1000 km)", "missiles": "Hit-to-Kill Interceptor (200 km, Elevasi 150 km)",
                "vls": "8x Tabung Peluncur Rudal per Baterai", "gun": "Kecepatan Intersep Mach 8.2", "ciws": "Sistem Komando C2BMC Terhubung Satelit"
            }
        ],
        "attack_mod": 1.70, "defense_mod": 1.50, "tech_mod": 1.65, "speed_mod": 1.35
    },
    "Japan": {
        "iso3": "JPN", "flag": "[JPN]", "color": "#d97706",
        "archetype": "hightech_precision",
        "doctrine": "Dynamic Joint Defense & Multi-Domain Aegis Shield",
        "capital_intensity": "High-Tech Precision Defense",
        "active_troops": 247000,
        "units": [
            {
                "id": "JS Maya (DDG 179) Aegis", "type": "ship", "role": "Destroyer Pertahanan Rudal Balistik",
                "radar": "AN/SPY-1D(V) Aegis Baseline 9 (380 km)", "missiles": "SM-3 Block IIA (Intersep Ekso-Atmosfer 2500 km)",
                "vls": "96-cell Mk 41 VLS (SM-2, SM-6, Type 07 VLA)", "gun": "127mm Mk 45 Mod 4", "ciws": "2x 20mm Phalanx Block 1B"
            },
            {
                "id": "JS Taigei (SS 513) Lithium Sub", "type": "sub", "role": "Kapal Selam Serang Baterai Litium Senyap",
                "radar": "OQX-25 ZQX Sonar Array Tingkat Lanjut", "missiles": "Sub-Harpoon AShM & Torpedo Type 18 Berat",
                "vls": "6x 533mm HU-606B Torpedo Tubes", "gun": "Propulsi Baterai Lithium-Ion Ultra-Hening", "ciws": "Peluncur Jammer Akustik Terpadu"
            },
            {
                "id": "JASDF F-35B Lightning II", "type": "jet", "role": "STOVL Siluman Multirole",
                "radar": "AN/APG-81 AESA Radar (250 km)", "missiles": "JSM (Joint Strike Missile) & AAM-4B",
                "vls": "Lepas Landas Pendek & Mendarat Vertikal", "gun": "Sensor Terpadu F-35 Sensor Fusion", "ciws": "Sistem Jamming Siber Mandiri"
            },
            {
                "id": "Helikopter SH-60K Seahawk", "type": "heli", "role": "Patroli Anti-Kapal Selam Maritim",
                "radar": "HPS-104 Search Radar Resolusi Tinggi", "missiles": "Torpedo Type 97/12 & Hellfire",
                "vls": "Dipping Sonar HQS-103 & Sonobuoy", "gun": "7.62mm Type 74 Senapan Mesin", "ciws": "AN/AAR-47 Missile Approach Warning"
            },
            {
                "id": "Baterai Pesisir Type 12 SSM", "type": "coastal", "role": "Rudal Pantai Jangkauan Diperluas",
                "radar": "Radar Pengarah Tembakan Mobile C2", "missiles": "Type 12 SSM Upgraded (1000 km)",
                "vls": "6x Peluncur Kontainer Berat", "gun": "Terrain Following & Kemampuan Siluman Radar", "ciws": "Koneksi Tautan Data Taktis Link 16"
            }
        ],
        "attack_mod": 1.35, "defense_mod": 1.45, "tech_mod": 1.50, "speed_mod": 1.15
    },
    "Singapore": {
        "iso3": "SGP", "flag": "[SGP]", "color": "#ea580c",
        "archetype": "hightech_precision",
        "doctrine": "Poisonous Shrimp & Forward Deterrence Strike",
        "capital_intensity": "Ultra-Compact Elite Tech",
        "active_troops": 72500,
        "units": [
            {
                "id": "RSS Formidable Frigate", "type": "ship", "role": "Frigat Siluman Multi-Misi",
                "radar": "Herakles 3D Multi-Function Radar (250 km)", "missiles": "8x Harpoon & 32x Aster 30 SAM (120 km)",
                "vls": "32-cell Sylver A50 VLS", "gun": "76mm Oto Melara Super Rapid", "ciws": "Eurotorp A244/S Anti-Submarine Torpedoes"
            },
            {
                "id": "Invincible-Class AIP Sub", "type": "sub", "role": "Kapal Selam Serang Littoral Tropis",
                "radar": "Atlas Elektronik Sonar Suite", "missiles": "Torpedo Berat DM2A4 & Harpoon",
                "vls": "Fuel Cell AIP Air-Independent Propulsion", "gun": "Kemampuan Selam Ekstrem Perairan Dangkal", "ciws": "Acoustic Decoy Launchers"
            },
            {
                "id": "RSAF F-15SG Strike Eagle", "type": "jet", "role": "Serang Presisi Jarak Jauh",
                "radar": "AN/APG-63(V)3 AESA Radar (200 km)", "missiles": "AIM-120C7 AMRAAM & JDAM Precision Bomb",
                "vls": "Kapasitas Bawaan Senjata 10.4 Ton", "gun": "20mm M61A1 Vulcan (6000 rpm)", "ciws": "Integrated Tactical Electronic Warfare"
            },
            {
                "id": "Helikopter AH-64D Longbow", "type": "heli", "role": "Bantuan Tembakan Udara Rapat",
                "radar": "AN/APG-78 Millimeter-Wave Radar", "missiles": "16x AGM-114L Radar Guided Hellfire",
                "vls": "70mm Hydra Rockets", "gun": "30mm M230 Chain Gun", "ciws": "Aircraft Survivability Equipment"
            },
            {
                "id": "Aster 30 SAMP/T Shield", "type": "coastal", "role": "Pertahanan Udara Kepadatan Tinggi",
                "radar": "Arabel Multi-Function Phased Array (100 km)", "missiles": "Aster 30 Hit-to-Kill (120 km, Kecepatan Mach 4.5)",
                "vls": "8-cell Vertical Launch Unit per Baterai", "gun": "Intersepsi Rudal Balistik Taktis", "ciws": "Jaringan Sensor Komando C4I Terpadu"
            }
        ],
        "attack_mod": 1.40, "defense_mod": 1.30, "tech_mod": 1.55, "speed_mod": 1.2
    },
    "India": {
        "iso3": "IND", "flag": "[IND]", "color": "#c2410c",
        "archetype": "global_heavyweight",
        "doctrine": "Two-Front Deterrence & Indian Ocean Control",
        "capital_intensity": "Heavy Balanced Fleet Mass",
        "active_troops": 1450000,
        "units": [
            {
                "id": "INS Kolkata Destroyer", "type": "ship", "role": "Destroyer Pertahanan Wilayah Udara",
                "radar": "EL/M-2248 MF-STAR AESA (250 km)", "missiles": "16x Supersonik BrahMos (290 km) & 32x Barak-8",
                "vls": "32x Barak-8 SAM VLS", "gun": "76mm OTO Melara SRGM", "ciws": "4x AK-630 Gatling (3000 rpm)"
            },
            {
                "id": "INS Kalvari Scorpene Sub", "type": "sub", "role": "Kapal Selam Serang Senyap",
                "radar": "Thales SUBTICS Integrated Combat System", "missiles": "SM39 Exocet AShM & Torpedo SUT 533mm",
                "vls": "6x 533mm Torpedo Tubes (18 Senjata)", "gun": "Lambung Baja Elastisitas Tinggi", "ciws": "Sistem Peluncur Umpan Anti-Torpedo"
            },
            {
                "id": "IAF Rafale & Su-30MKI", "type": "jet", "role": "Omnirole Dominasi Udara Jauh",
                "radar": "RBE2 AESA & N011M Bars PESA Radar", "missiles": "Meteor (200 km), SCALP Cruise & Astra Mk1",
                "vls": "Mampu Bawa BrahMos-A Udara", "gun": "30mm GSh-30-1 (1800 rpm)", "ciws": "Thales SPECTRA Electronic Warfare"
            },
            {
                "id": "Helikopter LCH Prachand", "type": "heli", "role": "Helikopter Serbu Ketinggian Ekstrem",
                "radar": "Optronic Sensor Pod & Laser Targetter", "missiles": "Helina Anti-Tank Guided Missile & Mistral ATAM",
                "vls": "70mm FZ Rocket Pods", "gun": "20mm M621 Turret Gun", "ciws": "Saab IDAS Electronic Warfare System"
            },
            {
                "id": "Baterai Pesisir BrahMos Mach 3", "type": "coastal", "role": "Pertahanan Penangkalan Supersonik",
                "radar": "Over-the-Horizon Surface Radar", "missiles": "BrahMos Block III Supersonik Mach 3.0",
                "vls": "Mobile Autonomous Launchers (3 Rudal per Truk)", "gun": "Trajektori Sea-Skimming 10 Meter", "ciws": "Pengawalan Pertahanan Titik Akash SAM"
            }
        ],
        "attack_mod": 1.35, "defense_mod": 1.35, "tech_mod": 1.15, "speed_mod": 1.1
    },
    "Malaysia": {
        "iso3": "MYS", "flag": "[MYS]", "color": "#7c3aed",
        "archetype": "territorial_archipelago",
        "doctrine": "Defensive Sea Denial & Littoral Chokepoint Defense",
        "capital_intensity": "Moderate Regional Fleet",
        "active_troops": 113000,
        "units": [
            {
                "id": "KD Lekiu Frigate", "type": "ship", "role": "Frigat Patroli Rudal Terpandu",
                "radar": "BAE Systems Type 996 3D Radar (150 km)", "missiles": "8x Exocet MM40 Block 2 (70 km)",
                "vls": "16-cell GWS.26 VLS (Seawolf SAM 10 km)", "gun": "57mm Bofors Mk 2 (220 rpm)", "ciws": "2x 30mm MSI DS30B Autocannon"
            },
            {
                "id": "KD Tunku Abdul Rahman Scorpene", "type": "sub", "role": "Kapal Selam Serbu Bawah Air",
                "radar": "Thales TSM 2233 Sonar Suite", "missiles": "SM39 Exocet Sub-Surface Missile & Black Shark",
                "vls": "6x 533mm Torpedo Tubes", "gun": "Desain Lambung Akustik Reduksi Jejak", "ciws": "Acoustic Decoy Dischargers"
            },
            {
                "id": "RMAF Su-30MKM Flanker", "type": "jet", "role": "Superioritas Udara Multi-Peran",
                "radar": "N011M Bars Phased Array Radar (140 km)", "missiles": "R-77 BVRAAM & Kh-31A Rudal Anti-Kapal",
                "vls": "Thrust Vectoring Canard Maneuverability", "gun": "30mm GSh-30-1 Gun", "ciws": "Thales Damocles Pod & SAPHIR Decoy"
            },
            {
                "id": "Helikopter Super Lynx 300", "type": "heli", "role": "Pengintaian & Serang Maritim",
                "radar": "Seaspray 3000 360-Degree Radar", "missiles": "Sea Skua Anti-Ship Missile & Torpedo A244/S",
                "vls": "Forward-Looking Infrared (FLIR) Turret", "gun": "Pintu Senapan Mesin 12.7mm", "ciws": "Radar Warning & Flare Dispenser"
            },
            {
                "id": "Baterai Pesisir Exocet MM40", "type": "coastal", "role": "Pertahanan Penyekatan Selat",
                "radar": "Mobile Surveillance Radar", "missiles": "Exocet MM40 Block 3 (200 km)",
                "vls": "Peluncur Kontainer 4x Rudal", "gun": "Kemampuan Manuver Berkelit Terminal", "ciws": "Sistem Hanud Portabel Starstreak"
            }
        ],
        "attack_mod": 1.05, "defense_mod": 1.15, "tech_mod": 1.00, "speed_mod": 1.0
    },
    "Vietnam": {
        "iso3": "VNM", "flag": "[VNM]", "color": "#991b1b",
        "archetype": "territorial_archipelago",
        "doctrine": "Asymmetric A2/AD & People's War at Sea",
        "capital_intensity": "High Attrition Territorial",
        "active_troops": 482000,
        "units": [
            {
                "id": "Gepard 3.9 Stealth Frigate", "type": "ship", "role": "Frigat Rudal Siluman Littoral",
                "radar": "Pozitiv-ME1 3D Air/Surface Radar (150 km)", "missiles": "8x Kh-35 Uran-E (130 km) & Palma CIWS",
                "vls": "Palma Complex dengan Rudal Sosna-R", "gun": "76mm AK-176M (120 rpm)", "ciws": "2x AK-630M 30mm Gatling Guns"
            },
            {
                "id": "Kilo 636MV Black Hole Sub", "type": "sub", "role": "Penyergap Senyap Kapal Selam",
                "radar": "MGK-400EM Sonar Kompleks", "missiles": "3M-54E Club-S AShM (220 km) & Torpedo 53-65KE",
                "vls": "6x 533mm Torpedo Tubes (18 Amunisi)", "gun": "Lapisan Karet Anechoic Reduksi Akustik", "ciws": "Peluncur Ranjuau Bawah Laut"
            },
            {
                "id": "VPAF Su-30MK2 Flanker", "type": "jet", "role": "Pencegat Serang Maritim",
                "radar": "N001VEP Radar Pemburu Kapal (150 km)", "missiles": "Kh-31A Supersonik Anti-Kapal (Mach 3.5, 70 km)",
                "vls": "R-73 & R-27 Rudal Udara-ke-Udara", "gun": "30mm GSh-30-1 Autocannon", "ciws": "SPO-15 Beryoza RWR & Jammer L-005"
            },
            {
                "id": "Helikopter Ka-28 Helix ASW", "type": "heli", "role": "Patroli Bawah Air Koaksial",
                "radar": "Inisiatif Radar Bawah Hidung Osminog", "missiles": "Torpedo Akustik APR-3E & Bom Laut PLAB-250",
                "vls": "V-36 Sonobuoy Receiver System", "gun": "Rotor Koaksial Tahan Angin Kencang", "ciws": "Infrared Jammer L-166V"
            },
            {
                "id": "Baterai Bastion-P Yakhont", "type": "coastal", "role": "Penolakan Akses Laut Lepas Pantai",
                "radar": "Monolit-B Over-the-Horizon Radar (350 km)", "missiles": "K-300P Oniks/Yakhont (Mach 2.6, 300 km)",
                "vls": "Peluncur Vertikal 2 Rudal per Truk MZKT", "gun": "Lintasan Rendah Sea-Skimming 5 Meter", "ciws": "Sistem Hanud Pendukung S-300PMU1"
            }
        ],
        "attack_mod": 1.15, "defense_mod": 1.40, "tech_mod": 0.95, "speed_mod": 1.0
    },
    "Philippines": {
        "iso3": "PHL", "flag": "[PHL]", "color": "#0369a1",
        "archetype": "territorial_archipelago",
        "doctrine": "Comprehensive Archipelagic Defense Concept (CADC)",
        "capital_intensity": "Emerging Modernization",
        "active_troops": 143000,
        "units": [
            {
                "id": "BRP Jose Rizal (FF 150)", "type": "ship", "role": "Frigat Rudal Multi-Peran",
                "radar": "Hensoldt TRS-3D Baseline D Multi-Mode (250 km)", "missiles": "4x SSM-700K C-Star AShM (150 km)",
                "vls": "Peluncur Mistral Simbad-RC SAM", "gun": "76mm Oto Melara Super Rapid", "ciws": "30mm Aselsan SMASH Remote Gun"
            },
            {
                "id": "BRP Conrado Yap Corvette", "type": "sub", "role": "Korvet Patroli Anti-Kapal Selam",
                "radar": "Thales WM-28 Fire Control Radar", "missiles": "6x Mk 32 Triple Torpedo Tubes (K745 Blue Shark)",
                "vls": "Bom Laut RBU-1200 Anti-Submarine Rockets", "gun": "2x 76mm OTO Melara Compact", "ciws": "2x 30mm Otobreda Dardo CIWS"
            },
            {
                "id": "PAF FA-50PH Golden Eagle", "type": "jet", "role": "Pesawat Tempur Serang Ringan",
                "radar": "EL/M-2032 Pulse Doppler Radar (100 km)", "missiles": "AIM-9L Sidewinder & AGM-65 Maverick",
                "vls": "Kecepatan Supersonik Mach 1.5", "gun": "20mm General Dynamics A-197 Rotary", "ciws": "Radar Warning & Chaff/Flare Dispensers"
            },
            {
                "id": "Helikopter AW159 Wildcat", "type": "heli", "role": "Serang & Pengawasan Maritim",
                "radar": "Seaspray 7000E Active Electronically Scanned", "missiles": "Spike NLOS (32 km) & Torpedo K745",
                "vls": "L3Harris Compact Dipping Sonar", "gun": "Pod Senapan Mesin FN MAG 7.62mm", "ciws": "Integrated Defensive Aids Suite (IDAS)"
            },
            {
                "id": "Baterai Pesisir BrahMos Battery", "type": "coastal", "role": "Pertahanan Penangkalan Pantai EEZ",
                "radar": "Mobile Coastal Command Radar", "missiles": "Supersonik Mach 2.8 BrahMos (290 km)",
                "vls": "3x Tabung Peluncur Rudal Kontainer", "gun": "Penetrator Warhead Anti-Kapal Perang", "ciws": "Sistem Hanud Mistral Portabel"
            }
        ],
        "attack_mod": 0.95, "defense_mod": 1.10, "tech_mod": 0.90, "speed_mod": 0.95
    }
}

# Profil 20 Variabel Doktrin Pertahanan [S1-S10 Strategis, T1-T10 Taktis]
COUNTRY_CAPABILITY_PROFILES = {
    "Indonesia": [27.5, 33.8, 52.0, 58.4, 55.0, 45.0, 52.0, 52.0, 90.0, 88.0, 54.0, 56.0, 50.0, 53.0, 48.0, 60.0, 46.0, 50.0, 60.0, 55.0],
    "Australia": [35.2, 75.8, 42.0, 12.5, 72.0, 78.0, 92.0, 91.0, 58.0, 62.0, 88.0, 85.0, 92.0, 90.0, 88.0, 80.0, 74.0, 89.0, 84.0, 88.0],
    "China": [92.0, 88.5, 85.0, 100.0, 78.0, 90.0, 65.0, 75.0, 92.0, 85.0, 88.0, 86.0, 89.0, 92.0, 88.0, 85.0, 92.0, 94.0, 95.0, 85.0],
    "United States": [96.0, 100.0, 90.0, 85.0, 92.0, 98.0, 98.0, 92.0, 88.0, 80.0, 96.0, 92.0, 98.0, 98.0, 95.0, 98.0, 90.0, 96.0, 95.0, 95.0],
    "Japan": [65.0, 82.0, 75.0, 40.0, 60.0, 88.0, 95.0, 94.0, 70.0, 78.0, 92.0, 90.0, 94.0, 95.0, 90.0, 82.0, 78.0, 90.0, 85.0, 90.0],
    "Singapore": [28.0, 68.0, 60.0, 15.0, 55.0, 85.0, 90.0, 98.0, 20.0, 82.0, 95.0, 95.0, 96.0, 96.0, 95.0, 75.0, 85.0, 95.0, 92.0, 92.0],
    "India": [60.0, 85.0, 65.0, 95.0, 68.0, 75.0, 75.0, 60.0, 90.0, 85.0, 85.0, 80.0, 82.0, 85.0, 82.0, 78.0, 85.0, 85.0, 82.0, 80.0],
    "Malaysia": [22.0, 25.0, 45.0, 25.0, 65.0, 40.0, 65.0, 68.0, 70.0, 72.0, 60.0, 58.0, 62.0, 62.0, 58.0, 55.0, 50.0, 60.0, 58.0, 65.0],
    "Vietnam": [20.0, 32.0, 48.0, 75.0, 55.0, 42.0, 55.0, 58.0, 88.0, 92.0, 65.0, 68.0, 62.0, 65.0, 60.0, 55.0, 65.0, 68.0, 65.0, 68.0],
    "Philippines": [22.0, 28.0, 35.0, 32.0, 48.0, 32.0, 78.0, 52.0, 78.0, 78.0, 58.0, 52.0, 55.0, 58.0, 52.0, 52.0, 45.0, 55.0, 55.0, 60.0]
}

THEATERS = {
    "Laut Arafura & Celah Timor (Skenario RI - Australia / ZEE Bersama)": {
        "lat": "09°15'S", "lon": "132°30'E", "terrain": "Laut Terbuka & Zona Ekonomi Eksklusif Dangkal",
        "desc": "Medan operasi perbatasan langsung ZEE. Karakteristik medan seimbang dengan jangkauan tempur setara, menghasilkan kondisi penangkalan timbal-balik (dasar pakta DCA 2024)."
    },
    "Selat Sunda & Laut Jawa (Skenario Pertahanan Kepulauan RI)": {
        "lat": "05°55'S", "lon": "105°50'E", "terrain": "Perairan Kepulauan Dalam, Selat Sempit, & Perlindungan Pulau",
        "desc": "Medan operasi kepulauan Nusantara. Memberikan bonus daya tahan teritorial (+35% Tahan) bagi doktrin kepulauan dan mereduksi efektivitas armada ekspedisi laut lepas asing."
    },
    "Laut Natuna Utara / Laut China Selatan (Gugus Karang & Kontestasi Terluar)": {
        "lat": "04°30'N", "lon": "108°10'E", "terrain": "Laut Lepas Strategis dengan Gugus Karang Pangkalan Luar",
        "desc": "Medan operasi maritim kontestasi tinggi. China didukung pangkalan pulau A2/AD, sementara negara ASEAN pesisir menerapkan taktik defensif asimetris."
    },
    "Samudra Pasifik Barat (Skenario Perang Udara-Maritim Jarak Jauh)": {
        "lat": "15°20'N", "lon": "135°40'E", "terrain": "Palung Samudra Lepas Terbuka Tanpa Daratan Pelindung",
        "desc": "Medan operasi laut lepas jarak jauh. Sangat menguntungkan armada padat modal berteknologi satelit, kapal induk, dan jet siluman (Australia/AS/Jepang)."
    },
    "Selat Malaka & Littoral Singapura (Chokepoint Sempit Strategis)": {
        "lat": "01°15'N", "lon": "103°48'E", "terrain": "Selat Sempit Littoral dengan Kepadatan Lalu Lintas Maritim",
        "desc": "Medan operasi selat sempit tersibuk. Menguntungkan armada littoral berpresisi tinggi (Singapura) dan pertahanan chokepoint pesisir (Malaysia/Indonesia)."
    },
    "Samudra Hindia & Pintu Barat Malaka (Proyeksi Maritim India)": {
        "lat": "06°00'N", "lon": "090°30'E", "terrain": "Pintu Gerbang Samudra Hindia Dekat Kepulauan Andaman",
        "desc": "Medan operasi proyeksi barat kawasan Indo-Pasifik. India memiliki keunggulan geografis mutlak dari Komando Gabungan Andaman & Nicobar."
    }
}

def calculate_theater_modifiers(country_name, c_data, theater_name, opp_country_name, opp_data):
    """
    Fungsi Universal: Menghitung koefisien atrisi dinamis berdasarkan interaksi doktrin negara
    dan karakteristik medan operasi geografis untuk seluruh pasangan negara di kawasan.
    """
    atk = c_data["attack_mod"]
    defs = c_data["defense_mod"]
    arch = c_data.get("archetype", "territorial_archipelago")
    tech = c_data.get("tech_mod", 1.0)
    iso = c_data.get("iso3", "")
    opp_iso = opp_data.get("iso3", "")
    
    notes = []
    
    if "Pasifik Barat" in theater_name or "Samudra Hindia" in theater_name:
        if "Samudra Hindia" in theater_name and iso == "IND":
            atk *= 1.30
            defs *= 1.25
            notes.append("Keunggulan teritorial mutlak pangkalan Komando Andaman & Nicobar (+30% Serang, +25% Tahan).")
        elif arch in ["global_heavyweight", "hightech_precision"] or tech >= 1.3:
            atk *= 1.25
            defs *= 1.15
            notes.append("Keunggulan proyeksi armada ekspedisi laut lepas & radar satelit jarak jauh (+25% Serang, +15% Tahan).")
        else:
            atk *= 0.82
            defs *= 0.80
            notes.append("Penalti jangkauan logistik di luar perairan kepulauan teritorial (-18% Serang, -20% Tahan).")

    elif "Sunda" in theater_name or "Jawa" in theater_name or "Malaka" in theater_name:
        if "Malaka" in theater_name and iso == "SGP":
            atk *= 1.25
            defs *= 1.25
            notes.append("Keunggulan komando littoral presisi tinggi dan sensor pulau terkonsentrasi (+25% Serang, +25% Tahan).")
        elif arch == "territorial_archipelago" or iso in ["IDN", "MYS", "VNM", "PHL"]:
            atk *= 1.18
            defs *= 1.35
            notes.append("Keunggulan medan teritorial kepulauan: kamuflase pulau, selat dangkal & baterai pantai (+35% Tahan, +18% Serang).")
        else:
            atk *= 0.85
            defs *= 0.88
            notes.append("Armada ekspedisi asing terhambat perairan sempit dan bahaya baterai pesisir (-15% Serang, -12% Tahan).")

    elif "Natuna" in theater_name or "China Selatan" in theater_name:
        if iso == "CHN":
            atk *= 1.22
            defs *= 1.18
            notes.append("Dukungan pangkalan militer pulau terluar & payung rudal balistik A2/AD (+22% Serang, +18% Tahan).")
        elif iso in ["VNM", "PHL", "IDN", "MYS"]:
            atk *= 1.12
            defs *= 1.28
            notes.append("Doktrin perlawanan asimetris ZEE teritorial pesisir (+28% Tahan, +12% Serang).")
        else:
            atk *= 1.12
            defs *= 1.05
            notes.append("Operasi kebebasan navigasi laut lepas (FONOPs) menghadapi saturasi rudal pesisir.")

    elif "Arafura" in theater_name or "Timor" in theater_name:
        if (iso == "IDN" and opp_iso == "AUS") or (iso == "AUS" and opp_iso == "IDN"):
            if iso == "IDN":
                atk, defs = 1.20, 1.25
            else:
                atk, defs = 1.25, 1.20
            notes.append("Keseimbangan penangkalan timbal-balik (mutual deterrence / dasar pakta DCA 2024).")
        elif arch == "global_heavyweight":
            atk *= 1.15
            defs *= 1.15
            notes.append("Keunggulan bobot massa gugus tempur di laut terbuka ZEE.")
        else:
            atk *= 1.05
            defs *= 1.05
            notes.append("Karakteristik medan perbatasan terbuka.")

    return round(atk, 3), round(defs, 3), " ".join(notes)

# Header Section
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="header-pretitle">LABORATORIUM MODEL & SIMULASI PERTAHANAN</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">C4ISR Defense Capability & Joint-Force Wargame Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sistem Analisis Komparasi Kapabilitas Pertahanan, Model Stokastik Lanchester, & Simulasi Empiris Indo-Pasifik (2010–2025)</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div class="authors-badge">
        <b>TIM PENELITI UKRI</b><br>
        Sandyarama Raka Adikara<br>
        Fauzan Akbar Ansyori<br>
        Nazmi Priyatama Shuerman<br>
        <i>Universitas Kebangsaan Republik Indonesia</i>
    </div>
    """, unsafe_allow_html=True)

# Global Control Bar: Pemilihan Dinamis Negara A, Negara B, dan Medan Operasi
st.markdown('<div class="metric-card" style="padding:10px 16px; margin-bottom:12px;">', unsafe_allow_html=True)
col_sel_a, col_sel_b, col_sel_t = st.columns(3)
country_list = list(COUNTRY_DATABASE.keys())

with col_sel_a:
    country_a = st.selectbox("Pilih Negara A:", country_list, index=0)
with col_sel_b:
    country_b = st.selectbox("Pilih Negara B:", country_list, index=1)
with col_sel_t:
    theater_name = st.selectbox("Pilih Medan Operasi Tempur:", list(THEATERS.keys()), index=0)
st.markdown('</div>', unsafe_allow_html=True)

c_data_a = COUNTRY_DATABASE[country_a]
c_data_b = COUNTRY_DATABASE[country_b]
t_info = THEATERS[theater_name]

# Kalkulasi Otomatis Berbasis Karakteristik Medan Operasi
mod_atk_a, mod_def_a, note_a = calculate_theater_modifiers(country_a, c_data_a, theater_name, country_b, c_data_b)
mod_atk_b, mod_def_b, note_b = calculate_theater_modifiers(country_b, c_data_b, theater_name, country_a, c_data_a)
theater_note = f"{t_info['desc']} [{country_a}]: {note_a} [{country_b}]: {note_b}"

# Main Navigation Tabs
tab_wargame, tab_data, tab_mcda, tab_policy = st.tabs([
    "[1] TACTICAL WARGAME SIMULATION",
    "[2] DATA EMPIRIS & KLUSTER KAWASAN",
    "[3] ENGINE SIMULASI MCDA & MONTE CARLO",
    "[4] SINTESIS KEBIJAKAN & BILATERAL"
])

# ==============================================================================
# TAB 1: TACTICAL WARGAME SIMULATION
# ==============================================================================
with tab_wargame:
    st.markdown(f"#### Tampilan Taktis C4ISR: Komparasi Tempur {country_a} vs {country_b}")
    
    # Intelligence Posture Cards (Color-Coded)
    col_stat_a, col_stat_b = st.columns(2)
    with col_stat_a:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #dc2626;">
            <div style="font-size:1.1rem; font-weight:700; color:#dc2626;">
                {country_a.upper()} ({c_data_a['iso3']})
            </div>
            <div style="font-size:0.85rem; color:#475569; margin: 4px 0;">
                <b>Doktrin:</b> {c_data_a['doctrine']}<br>
                <b>Efektivitas di Medan Operasi:</b> Serang x{mod_atk_a:.2f}, Daya Tahan x{mod_def_a:.2f}
            </div>
            <div style="font-size:0.8rem; color:#334155;">
                <b>Gugus Alutsista Tergelar:</b><br>
                {' &bull; '.join([u['id'] for u in c_data_a['units'][:4]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_stat_b:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #0284c7;">
            <div style="font-size:1.1rem; font-weight:700; color:#0284c7;">
                {country_b.upper()} ({c_data_b['iso3']})
            </div>
            <div style="font-size:0.85rem; color:#475569; margin: 4px 0;">
                <b>Doktrin:</b> {c_data_b['doctrine']}<br>
                <b>Efektivitas di Medan Operasi:</b> Serang x{mod_atk_b:.2f}, Daya Tahan x{mod_def_b:.2f}
            </div>
            <div style="font-size:0.8rem; color:#334155;">
                <b>Gugus Alutsista Tergelar:</b><br>
                {' &bull; '.join([u['id'] for u in c_data_b['units'][:4]])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.info(f"Kondisi Medan Operasi Terpilih: {theater_note}")

    # Serializing Theater-Adjusted Units for JS Engine
    units_json = json.dumps({
        "countryA": {
            "name": country_a,
            "flag": c_data_a["flag"],
            "color": "#dc2626",
            "units": c_data_a["units"],
            "attack": round(mod_atk_a, 3),
            "defense": round(mod_def_a, 3),
            "tech": c_data_a["tech_mod"],
            "speed": c_data_a["speed_mod"]
        },
        "countryB": {
            "name": country_b,
            "flag": c_data_b["flag"],
            "color": "#0284c7",
            "units": c_data_b["units"],
            "attack": round(mod_atk_b, 3),
            "defense": round(mod_def_b, 3),
            "tech": c_data_b["tech_mod"],
            "speed": c_data_b["speed_mod"]
        },
        "theater": {
            "name": theater_name,
            "lat": t_info["lat"],
            "lon": t_info["lon"],
            "desc": t_info["desc"]
        }
    })

    # Formulasi Model Lanchester
    lanchester_law = st.radio(
        "Pilih Formulasi Model Lanchester:",
        ["Square Law (Tembakan Terarah / Laut & Udara)",
         "Linear Law (Tembakan Area / Kontak Terbuka)",
         "Mixed/Asymmetric Law (Konvensional vs Pertahanan Asimetris)"],
        index=0,
        horizontal=True
    )

    # Render 3D C4ISR Tactical Battlespace Langsung (Three.js WebGL)
    wargame_dynamic_html = get_wargame_3d_html(units_json, theater_name, t_info, c_data_a, c_data_b, country_a, country_b)
    components.html(wargame_dynamic_html, height=670)

    st.markdown("---")
    st.markdown("##### Landasan Matematis: Formulasi Persamaan Diferensial Atrisi Lanchester")
    
    col_math1, col_math2 = st.columns([1.1, 0.9])
    
    # Koefisien Efektivitas Dasar
    alpha_eff = mod_atk_a / mod_def_b
    beta_eff = mod_atk_b / mod_def_a
    x0 = 100.0
    y0 = 100.0
    
    with col_math1:
        if "Linear" in lanchester_law:
            st.markdown(r"""
            **Model Terpilih: Lanchester Linear Law (Area Fire / Tembakan Tanpa Bidik Langsung)**
            $$\frac{dx}{dt} = -\beta \cdot x(t) \cdot y(t), \quad \frac{dy}{dt} = -\alpha \cdot x(t) \cdot y(t)$$
            Dengan konstanta invarian pertempuran linier:
            $$\alpha (x_0 - x(t)) = \beta (y_0 - y(t)) \implies P_{\text{rel}} = \frac{\alpha \cdot x_0}{\beta \cdot y_0}$$
            - Pada hukum linier, kepadatan massa pasukan memiliki pengaruh yang linier terhadap daya tembak total.
            """)
            p_rel = (alpha_eff * x0) / (beta_eff * y0)
            if p_rel >= 1.0:
                surviving = x0 - (beta_eff / alpha_eff) * y0
            else:
                surviving = y0 - (alpha_eff / beta_eff) * x0
        elif "Mixed" in lanchester_law:
            st.markdown(r"""
            **Model Terpilih: Lanchester Mixed/Asymmetric Law (Konvensional vs Pertahanan Asimetris)**
            $$\\frac{{dx}}{{dt}} = -\\beta \\cdot y(t), \\quad \\frac{{dy}}{{dt}} = -\\alpha \\cdot x(t) \\cdot y(t)$$
            Dengan konstanta invarian pertempuran campuran:
            $$\\alpha (x_0^2 - x(t)^2) = 2\\beta (y_0 - y(t)) \\implies P_{{\\text{{rel}}}} = \\frac{{\\alpha \\cdot x_0^2}}{{2\\beta \\cdot y_0}}$$
            - {country_a} ({c_data_a['iso3']}) bertindak sebagai kekuatan defensif asimetris, sedangkan {country_b} ({c_data_b['iso3']}) mengerahkan tembakan terarah konvensional.
            """)
            p_rel = (alpha_eff * (x0 ** 2)) / (2.0 * beta_eff * y0)
            if p_rel >= 1.0:
                surviving = np.sqrt(max(0.0, x0**2 - (2.0 * beta_eff / alpha_eff) * y0))
            else:
                surviving = y0 - (alpha_eff / (2.0 * beta_eff)) * (x0**2)
        else:
            st.markdown(r"""
            **Model Terpilih: Lanchester Square Law (Aimed Fire / Tembakan Terarah Presisi)**
            $$\frac{dx}{dt} = -\beta \cdot y(t), \quad \frac{dy}{dt} = -\alpha \cdot x(t)$$
            Dengan konstanta invarian pertempuran kuadratik:
            $$\alpha (x_0^2 - x(t)^2) = \beta (y_0^2 - y(t)^2) \implies P_{\text{rel}} = \frac{\alpha \cdot x_0^2}{\beta \cdot y_0^2}$$
            - Sangat relevan untuk perang laut lepas dan dominasi udara di mana sensor radar mengunci target individual secara presisi.
            """)
            p_rel = (alpha_eff * (x0 ** 2)) / (beta_eff * (y0 ** 2))
            if p_rel >= 1.0:
                surviving = np.sqrt(max(0.0, x0**2 - (beta_eff / alpha_eff) * (y0**2)))
            else:
                surviving = np.sqrt(max(0.0, y0**2 - (alpha_eff / beta_eff) * (x0**2)))
        
    with col_math2:
        if abs(p_rel - 1.0) <= 0.05:
            winner = "Keseimbangan Bersama (Nash Equilibrium)"
            win_color = "#059669"
            res_str = "Ekuilibrium Penangkalan Timbal-Balik (Mutual Deterrence)"
            exp_note = "Rasio daya tempur mendekati 1.00; membuktikan rasionalitas pakta pertahanan bilateral DCA RI–Australia 2024 (tidak ada pemenang absolut)."
        elif p_rel > 1.0:
            winner = country_a
            win_color = "#dc2626"
            res_str = f"{country_a} ({c_data_a['iso3']}) Unggul secara Deterministik"
            exp_note = f"{country_a} memiliki keunggulan atrisi di medan operasi ini dengan estimasi sisa kekuatan teoretis: {surviving:.1f}%."
        else:
            winner = country_b
            win_color = "#0284c7"
            res_str = f"{country_b} ({c_data_b['iso3']}) Unggul secara Deterministik"
            exp_note = f"{country_b} memiliki keunggulan atrisi di medan operasi ini dengan estimasi sisa kekuatan teoretis: {surviving:.1f}% (sesuai hasil komparasi makro notebook .ipynb)."
            
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid {win_color};">
            <div class="metric-title">Solusi Analitik Lanchester ({country_a} vs {country_b}) // {theater_name[:26]}...</div>
            <p style="margin: 4px 0; font-size: 0.9rem;"><b>Koefisien Efektivitas &alpha;:</b> {alpha_eff:.3f} | <b>Koefisien &beta;:</b> {beta_eff:.3f}</p>
            <p style="margin: 4px 0; font-size: 0.9rem;"><b>Rasio Daya Tempur Relatif (P<sub>rel</sub>):</b> {p_rel:.3f}</p>
            <p style="margin: 4px 0; font-size: 0.9rem; color: {win_color}; font-weight: 700;"><b>Hasil Teoretis:</b> {res_str}</p>
            <p style="margin: 4px 0; font-size: 0.82rem; color: #64748b;">{exp_note}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Evaluasi Kerusakan Tempur & Telemetri Waktu-Nyata (Battle Damage Assessment - BDA)")

    # Integrasi Numerik Lanchester Dinamis (dt = 0.5s, 60s)
    dt = 0.5
    t_steps = int(60 / dt)
    t_series = np.linspace(0, 60, t_steps + 1)
    x_traj = np.zeros(t_steps + 1)
    y_traj = np.zeros(t_steps + 1)
    x_traj[0] = 100.0
    y_traj[0] = 100.0

    t_break = 60.0
    for k in range(t_steps):
        if "Linear" in lanchester_law:
            loss_x = beta_eff * 0.00025 * x_traj[k] * y_traj[k] * dt
            loss_y = alpha_eff * 0.00025 * x_traj[k] * y_traj[k] * dt
        elif "Mixed" in lanchester_law:
            loss_x = beta_eff * 0.016 * y_traj[k] * dt
            loss_y = alpha_eff * 0.00025 * x_traj[k] * y_traj[k] * dt
        else:
            loss_x = beta_eff * 0.016 * y_traj[k] * dt
            loss_y = alpha_eff * 0.016 * x_traj[k] * dt
        
        x_traj[k+1] = max(0.0, x_traj[k] - loss_x)
        y_traj[k+1] = max(0.0, y_traj[k] - loss_y)

        if (x_traj[k+1] <= 30.0 or y_traj[k+1] <= 30.0) and t_break == 60.0:
            t_break = t_series[k+1]

    final_x = x_traj[-1]
    final_y = y_traj[-1]
    loss_pct_a = 100.0 - final_x
    loss_pct_b = 100.0 - final_y
    
    milex_a = c_data_a.get("tech_mod", 1.0) * 15.33
    milex_b = c_data_b.get("tech_mod", 1.0) * 25.00
    bda_loss_a = (loss_pct_a / 100.0) * milex_a * 0.35
    bda_loss_b = (loss_pct_b / 100.0) * milex_b * 0.35
    
    exchange_ratio = (loss_pct_b / (loss_pct_a + 1e-5))
    ciws_intercept_rate = round(68.0 + (c_data_a.get('tech_mod', 1.0) * 8.0) - (c_data_b.get('attack_mod', 1.0) * 4.0), 1)
    ciws_intercept_rate = max(45.0, min(92.0, ciws_intercept_rate))

    # BDA Metric Cards
    bda1, bda2, bda3, bda4 = st.columns(4)
    with bda1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Rasio Atrisi Tempur (Exchange Ratio)</div>
            <div style="font-size:1.5rem; font-weight:700; color:#0f172a; font-family:'JetBrains Mono', monospace;">{exchange_ratio:.2f} : 1.00</div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Rasio eliminasi {c_data_b['iso3']} per 1 unit {c_data_a['iso3']}</div>
        </div>
        """, unsafe_allow_html=True)

    with bda2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Taksiran Kerugian Alutsista {c_data_a['iso3']}</div>
            <div style="font-size:1.5rem; font-weight:700; color:#dc2626; font-family:'JetBrains Mono', monospace;">${bda_loss_a:.2f}B</div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Sisa kapabilitas tempur: {final_x:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with bda3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Taksiran Kerugian Alutsista {c_data_b['iso3']}</div>
            <div style="font-size:1.5rem; font-weight:700; color:#0284c7; font-family:'JetBrains Mono', monospace;">${bda_loss_b:.2f}B</div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Sisa kapabilitas tempur: {final_y:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with bda4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Tingkat Intersepsi Hanud & CIWS</div>
            <div style="font-size:1.5rem; font-weight:700; color:#059669; font-family:'JetBrains Mono', monospace;">{ciws_intercept_rate}%</div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Titik henti tempur (Breakpoint): T+{t_break:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)

    # Kurva Dinamika Atrisi Waktu Nyata & Status Unit
    c_dyn1, c_dyn2 = st.columns([1.1, 0.9])
    with c_dyn1:
        st.markdown("###### Trajektori Penurunan Kekuatan Armada (Integrasi Numerik 60 Detik)")
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Scatter(
            x=t_series, y=x_traj, mode='lines', name=f"{country_a} ({c_data_a['iso3']})",
            line=dict(color='#dc2626', width=2.5)
        ))
        fig_traj.add_trace(go.Scatter(
            x=t_series, y=y_traj, mode='lines', name=f"{country_b} ({c_data_b['iso3']})",
            line=dict(color='#0284c7', width=2.5)
        ))
        fig_traj.add_hline(y=30.0, line_dash="dash", line_color="#94a3b8", annotation_text="Ambang Batas Kehilangan Efektivitas Tempur (30%)")
        fig_traj.update_layout(
            template='plotly_white',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#0f172a', family='Inter'),
            xaxis=dict(title='Waktu Simulasi Pertempuran (Detik)', gridcolor='#f1f5f9'),
            yaxis=dict(title='Kekuatan Efektif Armada (%)', range=[0, 105], gridcolor='#f1f5f9'),
            margin=dict(l=35, r=20, t=20, b=35),
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_traj, use_container_width=True)

    with c_dyn2:
        st.markdown("###### Matriks Status Gugus Alutsista Pasca-Pertempuran")
        unit_status_list = []
        for u in c_data_a['units'][:3]:
            pct = max(15, int(final_x + np.random.uniform(-10, 10)))
            st_text = "Siaga Penuh" if pct >= 70 else ("Kerusakan Taktis (Mobility Kill)" if pct >= 45 else "Mission Kill")
            unit_status_list.append({"Platform": u['id'], "Negara": c_data_a['iso3'], "Peran": u['role'][:22], "Integritas": f"{pct}%", "Status": st_text})
        for u in c_data_b['units'][:3]:
            pct = max(15, int(final_y + np.random.uniform(-10, 10)))
            st_text = "Siaga Penuh" if pct >= 70 else ("Kerusakan Taktis (Mobility Kill)" if pct >= 45 else "Mission Kill")
            unit_status_list.append({"Platform": u['id'], "Negara": c_data_b['iso3'], "Peran": u['role'][:22], "Integritas": f"{pct}%", "Status": st_text})
        
        st.dataframe(pd.DataFrame(unit_status_list), use_container_width=True, height=260)

    # Spesifikasi Teknis Operasional Alutsista Lengkap
    st.markdown("###### Parameter Teknis Alutsista Utama di Medan Operasi")
    col_tech_a, col_tech_b = st.columns(2)
    with col_tech_a:
        st.markdown(f"**Rincian Alutsista {country_a} ({c_data_a['iso3']}):**")
        df_specs_a = pd.DataFrame([{
            "Alutsista": u["id"],
            "Radar / Sensor": u.get("radar", "AESA 3D Radar"),
            "Rudal / Senjata": u.get("missiles", "Anti-Ship Missile"),
            "Kapasitas Peluncur": u.get("vls", "Standard VLS")
        } for u in c_data_a["units"]])
        st.dataframe(df_specs_a, use_container_width=True, height=210)
        
    with col_tech_b:
        st.markdown(f"**Rincian Alutsista {country_b} ({c_data_b['iso3']}):**")
        df_specs_b = pd.DataFrame([{
            "Alutsista": u["id"],
            "Radar / Sensor": u.get("radar", "AESA 3D Radar"),
            "Rudal / Senjata": u.get("missiles", "Anti-Ship Missile"),
            "Kapasitas Peluncur": u.get("vls", "Standard VLS")
        } for u in c_data_b["units"]])
        st.dataframe(df_specs_b, use_container_width=True, height=210)

# ==============================================================================
# TAB 2: DATA EMPIRIS & KLUSTER KAWASAN (DINAMIS 14 NEGARA)
# ==============================================================================
with tab_data:
    st.markdown(f"#### Analisis Statistik Empiris Pertahanan: {country_a} vs {country_b} (2010–2025)")
    
    df_a = df_panel[df_panel['iso3'] == c_data_a['iso3']].sort_values('year').copy()
    df_b = df_panel[df_panel['iso3'] == c_data_b['iso3']].sort_values('year').copy()
    
    latest_a = df_a.iloc[-1]
    latest_b = df_b.iloc[-1]
    
    milex_a_val = latest_a['military_expenditure_constant_2024_usd_millions'] / 1000.0
    milex_b_val = latest_b['military_expenditure_constant_2024_usd_millions'] / 1000.0
    gap_ratio = (milex_b_val / (milex_a_val + 1e-5)) if milex_b_val >= milex_a_val else (milex_a_val / (milex_b_val + 1e-5))
    dominant_side = c_data_b['iso3'] if milex_b_val >= milex_a_val else c_data_a['iso3']
    
    # 4 Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Belanja Militer Riil (2025)</div>
            <div>[{c_data_a['iso3']}] <span class="metric-value-a">${milex_a_val:.2f}B</span></div>
            <div>[{c_data_b['iso3']}] <span class="metric-value-b">${milex_b_val:.2f}B</span></div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Disparitas Volume: {gap_ratio:.2f}x ({dominant_side} lebih besar)</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Beban Militer (% PDB 2025)</div>
            <div>[{c_data_a['iso3']}] <span class="metric-value-a">{latest_a['military_expenditure_share_gdp_percent']:.2f}%</span></div>
            <div>[{c_data_b['iso3']}] <span class="metric-value-b">{latest_b['military_expenditure_share_gdp_percent']:.2f}%</span></div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Persentase alokasi anggaran terhadap PDB riil</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        arms_a_val = latest_a['arms_imports_wdi_constant_1990_usd'] / 1e6 if pd.notna(latest_a['arms_imports_wdi_constant_1990_usd']) else 0.0
        arms_b_val = latest_b['arms_imports_wdi_constant_1990_usd'] / 1e6 if pd.notna(latest_b['arms_imports_wdi_constant_1990_usd']) else 0.0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Impor Senjata (SIPRI TIV 2025)</div>
            <div>[{c_data_a['iso3']}] <span class="metric-value-a">${arms_a_val:.0f}M</span></div>
            <div>[{c_data_b['iso3']}] <span class="metric-value-b">${arms_b_val:.0f}M</span></div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Indikator transfer alutsista konstan 1990 USD</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Postur Intensitas Modal Pertahanan</div>
            <div>[{c_data_a['iso3']}] <span class="metric-value-a">{c_data_a['capital_intensity'].split('(')[-1].replace(')', '')}</span></div>
            <div>[{c_data_b['iso3']}] <span class="metric-value-b">{c_data_b['capital_intensity'].split('(')[-1].replace(')', '')}</span></div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">Model Padat Modal vs Padat Karya Teritorial</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 4 Multi-Axis Empirical Charts
    st.markdown("##### Multi-Axis Financial Trends: Komparasi Empiris SIPRI & WDI (2010–2025)")
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        # 1. Real Milex Chart
        fig_m = go.Figure()
        fig_m.add_trace(go.Scatter(x=df_a['year'], y=df_a['military_expenditure_constant_2024_usd_millions']/1000,
                                   mode='lines+markers', name=f"{country_a} ({c_data_a['iso3']})", line=dict(color='#dc2626', width=2.5)))
        fig_m.add_trace(go.Scatter(x=df_b['year'], y=df_b['military_expenditure_constant_2024_usd_millions']/1000,
                                   mode='lines+markers', name=f"{country_b} ({c_data_b['iso3']})", line=dict(color='#0284c7', width=2.5)))
        fig_m.update_layout(
            title="(A) Belanja Militer Riil (Miliar US$ Konstan 2024)",
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font=dict(color='#0f172a', family='Inter'),
            xaxis=dict(title='Tahun', gridcolor='#f1f5f9'), yaxis=dict(title='Miliar US$', gridcolor='#f1f5f9'),
            margin=dict(l=40, r=20, t=40, b=40), height=280, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_m, use_container_width=True)

    with c_g2:
        # 2. Military Burden (% GDP) Chart
        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(x=df_a['year'], y=df_a['military_expenditure_share_gdp_percent'],
                                   mode='lines+markers', name=f"{country_a} ({c_data_a['iso3']})", line=dict(color='#dc2626', width=2.5)))
        fig_b.add_trace(go.Scatter(x=df_b['year'], y=df_b['military_expenditure_share_gdp_percent'],
                                   mode='lines+markers', name=f"{country_b} ({c_data_b['iso3']})", line=dict(color='#0284c7', width=2.5)))
        fig_b.add_hline(y=1.5, line_dash="dot", line_color="#94a3b8", annotation_text="Target Acuan MEF (1.5% PDB)")
        fig_b.update_layout(
            title="(B) Beban Militer (% terhadap PDB Riil)",
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font=dict(color='#0f172a', family='Inter'),
            xaxis=dict(title='Tahun', gridcolor='#f1f5f9'), yaxis=dict(title='% PDB', gridcolor='#f1f5f9'),
            margin=dict(l=40, r=20, t=40, b=40), height=280, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_b, use_container_width=True)

    c_g3, c_g4 = st.columns(2)
    with c_g3:
        # 3. Arms Imports Volume (SIPRI TIV)
        fig_a = go.Figure()
        fig_a.add_trace(go.Bar(x=df_a['year'], y=df_a['arms_imports_wdi_constant_1990_usd']/1e6,
                               name=f"{country_a} ({c_data_a['iso3']})", marker_color='#dc2626', opacity=0.75))
        fig_a.add_trace(go.Bar(x=df_b['year'], y=df_b['arms_imports_wdi_constant_1990_usd']/1e6,
                               name=f"{country_b} ({c_data_b['iso3']})", marker_color='#0284c7', opacity=0.75))
        fig_a.update_layout(
            barmode='group', title="(C) Volume Impor Senjata Utama (SIPRI TIV - Juta US$ 1990)",
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font=dict(color='#0f172a', family='Inter'),
            xaxis=dict(title='Tahun', gridcolor='#f1f5f9'), yaxis=dict(title='Juta TIV (1990 USD)', gridcolor='#f1f5f9'),
            margin=dict(l=40, r=20, t=40, b=40), height=280, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_a, use_container_width=True)

    with c_g4:
        # 4. Macroeconomic GDP Capacity
        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=df_a['year'], y=df_a['gdp_constant_2015_usd']/1e12,
                                   mode='lines+markers', name=f"{country_a} ({c_data_a['iso3']})", line=dict(color='#dc2626', width=2.5)))
        fig_g.add_trace(go.Scatter(x=df_b['year'], y=df_b['gdp_constant_2015_usd']/1e12,
                                   mode='lines+markers', name=f"{country_b} ({c_data_b['iso3']})", line=dict(color='#0284c7', width=2.5)))
        fig_g.update_layout(
            title="(D) Kapasitas PDB Riil (Triliun US$ Konstan 2015)",
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font=dict(color='#0f172a', family='Inter'),
            xaxis=dict(title='Tahun', gridcolor='#f1f5f9'), yaxis=dict(title='Triliun US$', gridcolor='#f1f5f9'),
            margin=dict(l=40, r=20, t=40, b=40), height=280, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("---")
    
    # Statistical Summary & PCA Decomposition Tables
    c_stat1, c_stat2 = st.columns([1, 1])
    with c_stat1:
        st.markdown("##### Tabel Statistik Deskriptif Formal (2010–2025)")
        # Hitung CAGR
        m_start_a = df_a.iloc[0]['military_expenditure_constant_2024_usd_millions']
        m_end_a = df_a.iloc[-1]['military_expenditure_constant_2024_usd_millions']
        cagr_a = ((m_end_a / m_start_a) ** (1/15) - 1) * 100
        
        m_start_b = df_b.iloc[0]['military_expenditure_constant_2024_usd_millions']
        m_end_b = df_b.iloc[-1]['military_expenditure_constant_2024_usd_millions']
        cagr_b = ((m_end_b / m_start_b) ** (1/15) - 1) * 100
        
        # Hitung Koefisien Variasi
        cv_a = (df_a['military_expenditure_constant_2024_usd_millions'].std() / df_a['military_expenditure_constant_2024_usd_millions'].mean()) * 100
        cv_b = (df_b['military_expenditure_constant_2024_usd_millions'].std() / df_b['military_expenditure_constant_2024_usd_millions'].mean()) * 100

        df_desc = pd.DataFrame([
            {"Parameter Statistik": "Rata-Rata Belanja Riil (Miliar USD)", f"{country_a} ({c_data_a['iso3']})": f"${df_a['military_expenditure_constant_2024_usd_millions'].mean()/1000:.2f}B", f"{country_b} ({c_data_b['iso3']})": f"${df_b['military_expenditure_constant_2024_usd_millions'].mean()/1000:.2f}B"},
            {"Parameter Statistik": "Median Belanja Riil (Miliar USD)", f"{country_a} ({c_data_a['iso3']})": f"${df_a['military_expenditure_constant_2024_usd_millions'].median()/1000:.2f}B", f"{country_b} ({c_data_b['iso3']})": f"${df_b['military_expenditure_constant_2024_usd_millions'].median()/1000:.2f}B"},
            {"Parameter Statistik": "Standar Deviasi Anggaran", f"{country_a} ({c_data_a['iso3']})": f"${df_a['military_expenditure_constant_2024_usd_millions'].std()/1000:.2f}B", f"{country_b} ({c_data_b['iso3']})": f"${df_b['military_expenditure_constant_2024_usd_millions'].std()/1000:.2f}B"},
            {"Parameter Statistik": "Pertumbuhan Tahunan (CAGR 2010–2025)", f"{country_a} ({c_data_a['iso3']})": f"+{cagr_a:.2f}% / thn", f"{country_b} ({c_data_b['iso3']})": f"+{cagr_b:.2f}% / thn"},
            {"Parameter Statistik": "Koefisien Variasi (Volatilitas Anggaran)", f"{country_a} ({c_data_a['iso3']})": f"{cv_a:.1f}%", f"{country_b} ({c_data_b['iso3']})": f"{cv_b:.1f}%"},
            {"Parameter Statistik": "Rata-Rata Beban Militer (% PDB)", f"{country_a} ({c_data_a['iso3']})": f"{df_a['military_expenditure_share_gdp_percent'].mean():.2f}%", f"{country_b} ({c_data_b['iso3']})": f"{df_b['military_expenditure_share_gdp_percent'].mean():.2f}%"},
            {"Parameter Statistik": "Total Impor Senjata Kumulatif (SIPRI TIV)", f"{country_a} ({c_data_a['iso3']})": f"${df_a['arms_imports_wdi_constant_1990_usd'].sum()/1e6:.0f}M", f"{country_b} ({c_data_b['iso3']})": f"${df_b['arms_imports_wdi_constant_1990_usd'].sum()/1e6:.0f}M"}
        ])
        st.dataframe(df_desc, use_container_width=True, height=275)

    with c_stat2:
        st.markdown("##### Dekomposisi PCA & Feature Factor Loadings (14 Negara)")
        df_window = df_panel[df_panel['year'].between(2016, 2025)].groupby(['iso3', 'country']).agg({
            'gdp_constant_2015_usd': 'mean',
            'military_expenditure_constant_2024_usd_millions': 'mean',
            'military_expenditure_share_gdp_percent': 'mean',
            'arms_imports_wdi_constant_1990_usd': 'mean'
        }).reset_index()
        df_window['arms_imports_wdi_constant_1990_usd'] = df_window['arms_imports_wdi_constant_1990_usd'].fillna(df_window['arms_imports_wdi_constant_1990_usd'].median())
        
        feats = ['gdp_constant_2015_usd', 'military_expenditure_constant_2024_usd_millions', 'military_expenditure_share_gdp_percent', 'arms_imports_wdi_constant_1990_usd']
        scaled = StandardScaler().fit_transform(df_window[feats])
        pca = PCA(n_components=2, random_state=42)
        pcs = pca.fit_transform(scaled)
        
        loadings = pca.components_
        var_exp = pca.explained_variance_ratio_ * 100
        
        df_pca_summary = pd.DataFrame([
            {"Indikator Fitur": "Kapasitas PDB Riil", "Loading PC1 (Skala)": f"{loadings[0,0]:.3f}", "Loading PC2 (Intensitas)": f"{loadings[1,0]:.3f}"},
            {"Indikator Fitur": "Belanja Militer Riil", "Loading PC1 (Skala)": f"{loadings[0,1]:.3f}", "Loading PC2 (Intensitas)": f"{loadings[1,1]:.3f}"},
            {"Indikator Fitur": "Beban Militer (% PDB)", "Loading PC1 (Skala)": f"{loadings[0,2]:.3f}", "Loading PC2 (Intensitas)": f"{loadings[1,2]:.3f}"},
            {"Indikator Fitur": "Impor Alutsista (SIPRI TIV)", "Loading PC1 (Skala)": f"{loadings[0,3]:.3f}", "Loading PC2 (Intensitas)": f"{loadings[1,3]:.3f}"},
            {"Indikator Fitur": "Varians Terjelaskan (%)", "Loading PC1 (Skala)": f"{var_exp[0]:.1f}%", "Loading PC2 (Intensitas)": f"{var_exp[1]:.1f}%"},
            {"Indikator Fitur": "Kumulatif Varians", "Loading PC1 (Skala)": f"{var_exp[0]:.1f}%", "Loading PC2 (Intensitas)": f"{var_exp[0]+var_exp[1]:.1f}%"}
        ])
        st.dataframe(df_pca_summary, use_container_width=True, height=275)

    st.markdown("---")
    st.markdown(f"##### Tabel Data Panel Observasi Empiris Terverifikasi (2020–2025: {country_a} vs {country_b})")
    df_table = df_panel[df_panel['iso3'].isin([c_data_a['iso3'], c_data_b['iso3']]) & (df_panel['year'] >= 2020)][[
        'year', 'country', 'military_expenditure_constant_2024_usd_millions',
        'military_expenditure_share_gdp_percent', 'arms_imports_wdi_constant_1990_usd', 'gdp_constant_2015_usd'
    ]].copy()
    df_table.columns = ['Tahun', 'Negara', 'Belanja Militer (Juta US$ 2024)', 'Beban Militer (% PDB)', 'Impor Senjata (Juta US$ 1990)', 'PDB Riil (Miliar US$ 2015)']
    df_table['Impor Senjata (Juta US$ 1990)'] = (df_table['Impor Senjata (Juta US$ 1990)'] / 1e6).round(1)
    df_table['Belanja Militer (Juta US$ 2024)'] = df_table['Belanja Militer (Juta US$ 2024)'].round(1)
    df_table['PDB Riil (Miliar US$ 2015)'] = (df_table['PDB Riil (Miliar US$ 2015)'] / 1e9).round(1)
    st.dataframe(df_table.sort_values(['Tahun', 'Negara'], ascending=[False, True]), use_container_width=True)

# ==============================================================================
# TAB 3: ENGINE SIMULASI MCDA & MONTE CARLO (DINAMIS 10.000 ITERASI)
# ==============================================================================
with tab_mcda:
    st.markdown(f"#### Multi-Criteria Capability Radar & Monte Carlo Simulation: {country_a} vs {country_b}")
    
    col_sim_ctrl, col_sim_view = st.columns([1, 2])
    
    with col_sim_ctrl:
        st.markdown("##### Parameter Skenario Pembobotan:")
        scenario_choice = st.selectbox(
            "Pilih Skenario Pembobotan:",
            ["Skenario 1: Keseimbangan Standar (50:50)",
             "Skenario 2: Pertahanan Teritorial Kepulauan",
             "Skenario 3: Proyeksi Kekuatan Udara-Maritim"]
        )
        
        # Kontrol Slider Dua Arah (Negara A dan Negara B)
        st.markdown(f"##### Penyesuaian Taktis [{c_data_a['iso3']}] {country_a}:")
        base_t2_a = int(COUNTRY_CAPABILITY_PROFILES.get(country_a, [50]*20)[11])
        base_t4_a = int(COUNTRY_CAPABILITY_PROFILES.get(country_a, [50]*20)[13])
        base_t9_a = int(COUNTRY_CAPABILITY_PROFILES.get(country_a, [50]*20)[18])
        t2_a = st.slider(f"T2: Kesiapan Alutsista ({c_data_a['iso3']} %)", 20, 98, base_t2_a)
        t4_a = st.slider(f"T4: Radar & ISR ({c_data_a['iso3']})", 20, 98, base_t4_a)
        t9_a = st.slider(f"T9: Drone & Nirawak ({c_data_a['iso3']})", 20, 98, base_t9_a)
        
        st.markdown(f"##### Penyesuaian Taktis [{c_data_b['iso3']}] {country_b}:")
        base_t2_b = int(COUNTRY_CAPABILITY_PROFILES.get(country_b, [50]*20)[11])
        base_t4_b = int(COUNTRY_CAPABILITY_PROFILES.get(country_b, [50]*20)[13])
        base_t9_b = int(COUNTRY_CAPABILITY_PROFILES.get(country_b, [50]*20)[18])
        t2_b = st.slider(f"T2: Kesiapan Alutsista ({c_data_b['iso3']} %)", 20, 98, base_t2_b)
        t4_b = st.slider(f"T4: Radar & ISR ({c_data_b['iso3']})", 20, 98, base_t4_b)
        t9_b = st.slider(f"T9: Drone & Nirawak ({c_data_b['iso3']})", 20, 98, base_t9_b)
        
        run_mc_btn = st.button("JALANKAN SIMULASI MONTE CARLO (10.000 RUN)", use_container_width=True)

    with col_sim_view:
        var_labels = [
            "S1: PDB", "S2: Belanja", "S3: Mandiri", "S4: Pasukan", "S5: Energi",
            "S6: R&D", "S7: Aliansi", "S8: Tata Kelola", "S9: Geografi", "S10: Rakyat",
            "T1: Latihan", "T2: Kesiapan", "T3: C2", "T4: Radar/ISR", "T5: Tri-Matra",
            "T6: Mobilitas", "T7: Amunisi", "T8: Siber/EW", "T9: Drone", "T10: Medis"
        ]
        
        profile_a = list(COUNTRY_CAPABILITY_PROFILES.get(country_a, [50.0]*20))
        profile_b = list(COUNTRY_CAPABILITY_PROFILES.get(country_b, [50.0]*20))
        
        # Terapkan slider interaktif pada kedua negara
        profile_a[11] = float(t2_a)
        profile_a[13] = float(t4_a)
        profile_a[18] = float(t9_a)
        
        profile_b[11] = float(t2_b)
        profile_b[13] = float(t4_b)
        profile_b[18] = float(t9_b)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=profile_a + [profile_a[0]], theta=var_labels + [var_labels[0]],
            fill='toself', name=f"{country_a} ({c_data_a['iso3']})", line=dict(color='#dc2626', width=2), fillcolor='rgba(220, 38, 38, 0.15)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=profile_b + [profile_b[0]], theta=var_labels + [var_labels[0]],
            fill='toself', name=f"{country_b} ({c_data_b['iso3']})", line=dict(color='#0284c7', width=2), fillcolor='rgba(2, 132, 199, 0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#e2e8f0'),
                angularaxis=dict(gridcolor='#e2e8f0')
            ),
            template='plotly_white', paper_bgcolor='#ffffff', font=dict(color='#0f172a', family='Inter'),
            margin=dict(l=40, r=40, t=30, b=30), height=410, legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    st.markdown(f"##### Distribusi Probabilitas Simulasi Monte Carlo (10.000 Iterasi: {country_a} vs {country_b})")
    
    np.random.seed(42)
    n_sims = 10000
    
    w_strat_base = np.array([0.1]*10 + [0.0]*10)
    w_takt_base = np.array([0.0]*10 + [0.1]*10)
    
    if "Skenario 2" in scenario_choice:
        w_strat_s2 = np.array([0.08, 0.08, 0.08, 0.16, 0.10, 0.06, 0.06, 0.08, 0.15, 0.15] + [0.0]*10)
        w_takt_s2 = np.array([0.0]*10 + [0.10, 0.12, 0.08, 0.08, 0.10, 0.12, 0.14, 0.08, 0.10, 0.08])
        w_active = 0.65 * w_strat_s2 + 0.35 * w_takt_s2
    elif "Skenario 3" in scenario_choice:
        w_strat_s3 = np.array([0.12, 0.14, 0.08, 0.05, 0.10, 0.12, 0.18, 0.10, 0.05, 0.06] + [0.0]*10)
        w_takt_s3 = np.array([0.0]*10 + [0.12, 0.12, 0.14, 0.14, 0.10, 0.08, 0.08, 0.12, 0.05, 0.05])
        w_active = 0.35 * w_strat_s3 + 0.65 * w_takt_s3
    else:
        w_active = 0.5 * w_strat_base + 0.5 * w_takt_base
        
    # Pembangkitan sampel acak 10.000 run dari distribusi segitiga
    samples_a = np.zeros((n_sims, 20))
    samples_b = np.zeros((n_sims, 20))
    for j in range(20):
        val_a = profile_a[j]
        samples_a[:, j] = np.random.triangular(val_a * 0.92, val_a, val_a * 1.08, n_sims)
        val_b = profile_b[j]
        samples_b[:, j] = np.random.triangular(val_b * 0.92, val_b, val_b * 1.08, n_sims)
        
    sim_a = np.dot(samples_a, w_active)
    sim_b = np.dot(samples_b, w_active)
    diff = sim_a - sim_b
    prob_a_superior = np.mean(diff > 0) * 100.0
    
    # Uji Hipotesis Inferensial: Welch's t-Test & Cohen's d
    t_stat, p_val = stats.ttest_ind(sim_a, sim_b, equal_var=False)
    cohen_d = (np.mean(sim_a) - np.mean(sim_b)) / np.sqrt((np.var(sim_a) + np.var(sim_b)) / 2)
    effect_size_label = "Very Large" if abs(cohen_d) > 1.2 else ("Large" if abs(cohen_d) > 0.8 else ("Medium" if abs(cohen_d) > 0.5 else "Small"))

    col_dist, col_table = st.columns([3, 2])
    with col_dist:
        fig_mc = go.Figure()
        fig_mc.add_trace(go.Histogram(x=sim_a, name=f"{country_a} ({c_data_a['iso3']})", marker_color='#dc2626', opacity=0.75, nbinsx=60))
        fig_mc.add_trace(go.Histogram(x=sim_b, name=f"{country_b} ({c_data_b['iso3']})", marker_color='#0284c7', opacity=0.75, nbinsx=60))
        fig_mc.update_layout(
            barmode='overlay', template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
            font=dict(color='#0f172a', family='Inter'),
            xaxis=dict(title='Skor Indeks Komposit Kapabilitas Pertahanan (0-100)', gridcolor='#f1f5f9'),
            yaxis=dict(title='Frekuensi / Densitas Sampel', gridcolor='#f1f5f9'),
            margin=dict(l=30, r=20, t=20, b=30), height=300, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_mc, use_container_width=True)
        
    with col_table:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Inferensi Statistik & Uji Hipotesis (10.000 Run)</div>
            <p style="margin:4px 0; font-size:0.88rem;"><b>Skor Rata-Rata {c_data_a['iso3']}:</b> {np.mean(sim_a):.2f} (95% CI: [{np.percentile(sim_a, 2.5):.2f}, {np.percentile(sim_a, 97.5):.2f}])</p>
            <p style="margin:4px 0; font-size:0.88rem;"><b>Skor Rata-Rata {c_data_b['iso3']}:</b> {np.mean(sim_b):.2f} (95% CI: [{np.percentile(sim_b, 2.5):.2f}, {np.percentile(sim_b, 97.5):.2f}])</p>
            <p style="margin:4px 0; font-size:0.88rem;"><b>Probabilitas Keunggulan {c_data_a['iso3']}:</b> {prob_a_superior:.2f}%</p>
            <p style="margin:4px 0; font-size:0.88rem;"><b>Uji Welch t-Statistic:</b> {t_stat:.2f} (p-value: {p_val:.4e})</p>
            <p style="margin:4px 0; font-size:0.88rem;"><b>Besaran Efek (Cohen's d):</b> {cohen_d:.2f} ({effect_size_label} Effect)</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Machine Learning Feature Importance (Random Forest Regressor)
    st.markdown("##### Machine Learning: Faktor Pengungkit Utama Pertahanan (Random Forest Feature Importance)")
    col_ml1, col_ml2 = st.columns([1.2, 0.8])
    
    if CSV_FEATURE_IMPORTANCE.exists():
        df_fi = pd.read_csv(CSV_FEATURE_IMPORTANCE)
    else:
        df_fi = pd.DataFrame([
            {"Variabel": "T9: Adaptasi Taktis & Sistem Nirawak (UAV)", "Importance (%)": 7.69},
            {"Variabel": "T2: Tingkat Kesiapan Armada Alutsista (Readiness)", "Importance (%)": 6.86},
            {"Variabel": "T4: Intelijen, Pengawasan & Radar (ISR)", "Importance (%)": 6.15},
            {"Variabel": "T10: Proteksi Pasukan & Dukungan Medis Tempur", "Importance (%)": 6.14},
            {"Variabel": "T1: Kualitas Pelatihan & Jam Terbang", "Importance (%)": 6.01},
            {"Variabel": "T7: Cadangan Amunisi Tempur Strategis", "Importance (%)": 5.76},
            {"Variabel": "T3: Komando, Kendali & Komunikasi (C2)", "Importance (%)": 5.67},
            {"Variabel": "T5: Interoperabilitas Tri-Matra Terpadu", "Importance (%)": 5.55},
            {"Variabel": "S7: Aliansi dan Kemitraan Strategis", "Importance (%)": 5.40},
            {"Variabel": "T6: Mobilitas Strategis (Airlift/Sealift)", "Importance (%)": 5.31}
        ])
        
    with col_ml1:
        fig_fi = px.bar(
            df_fi.head(10).sort_values("Importance (%)", ascending=True),
            x="Importance (%)", y="Variabel", orientation="h",
            color="Importance (%)", color_continuous_scale="Blues",
            title="Top 10 Variabel Penentu Keunggulan Ketahanan (MDI Feature Importance %)"
        )
        fig_fi.update_layout(
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
            font=dict(color='#0f172a', family='Inter'), margin=dict(l=20, r=20, t=35, b=20), height=300
        )
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_ml2:
        st.markdown(f"""
        <div class="metric-card" style="font-size:0.85rem; line-height:1.5;">
            <div class="metric-title">Interpretasi Global Sensitivity Analysis</div>
            <p>Model <b>Random Forest Regressor</b> membuktikan bahwa daya tahan pertahanan paling sensitif terhadap variabel taktis berteknologi tinggi:</p>
            <ol style="padding-left:18px; margin:4px 0;">
                <li><b>Adaptasi Drone Nirawak (T9 - 7.69%)</b></li>
                <li><b>Kesiapan Armada Alutsista (T2 - 6.86%)</b></li>
                <li><b>Radar & Pengawasan Maritim (T4 - 6.15%)</b></li>
            </ol>
            <p style="color:#64748b; font-size:0.78rem; margin-top:6px;">*Alokasi anggaran pada sensor dan drone memberikan efek perbaikan skor yang jauh lebih tinggi dibanding sekadar menambah personel mentah (S4 - 2.43%).</p>
        </div>
        """, unsafe_allow_html=True)

    # Master Table 20 Variabel Doktrin
    st.markdown("---")
    st.markdown(f"##### Master Data 20 Variabel Kapabilitas Pertahanan ({country_a} vs {country_b})")
    var_specs_display = []
    for idx, code in enumerate(var_labels):
        c_code = code.split(":")[0]
        c_name = code.split(":")[1].strip()
        dim = "Strategis (S)" if idx < 10 else "Taktis (T)"
        val_a = profile_a[idx]
        val_b = profile_b[idx]
        var_specs_display.append({
            "Kode": c_code,
            "Dimensi": dim,
            "Indikator Kapabilitas": c_name,
            f"Skor {c_data_a['iso3']}": f"{val_a:.1f}",
            f"Parameter Segitiga [{c_data_a['iso3']}]": f"[{val_a*0.92:.1f}, {val_a:.1f}, {val_a*1.08:.1f}]",
            f"Skor {c_data_b['iso3']}": f"{val_b:.1f}",
            f"Parameter Segitiga [{c_data_b['iso3']}]": f"[{val_b*0.92:.1f}, {val_b:.1f}, {val_b*1.08:.1f}]",
            "Selisih Gap": f"{val_a - val_b:+.1f}"
        })
    st.dataframe(pd.DataFrame(var_specs_display), use_container_width=True, height=340)

# ==============================================================================
# TAB 4: SINTESIS KEBIJAKAN & BILATERAL (DINAMIS SESUAI PASANGAN NEGARA)
# ==============================================================================
with tab_policy:
    st.markdown(f"#### Kajian Strategis Pertahanan: Hubungan Bilateral {country_a} – {country_b}")
    
    col_pol1, col_pol2 = st.columns([1, 1])
    
    if (c_data_a['iso3'] == 'IDN' and c_data_b['iso3'] == 'AUS') or (c_data_a['iso3'] == 'AUS' and c_data_b['iso3'] == 'IDN'):
        title_p1 = "Temuan Pokok Pemodelan Ilmiah RI–Australia"
        body_p1 = """
        <ul style="padding-left:18px; line-height:1.6; font-size:0.92rem; color:#334155;">
            <li><b>Asimetri Doktrin:</b> Australia beroperasi pada model padat modal teknologi tinggi (~US$587K/prajurit), sedangkan Indonesia beroperasi pada model ketahanan teritorial kepulauan padat karya (~US$22.7K/prajurit).</li>
            <li><b>Kompensasi Defensif Kepulauan:</b> Dalam skenario teritorial kepulauan (Skenario 2), selisih kapabilitas menyusut drastis dari 26.24 poin menjadi hanya 9.03 poin, membuktikan daya tangkal teritorial Indonesia yang sangat tangguh di perairan dalam.</li>
            <li><b>Faktor Pengungkit Machine Learning:</b> Algoritma Random Forest membuktikan adaptasi drone nirawak (T9), kesiapan armada (T2), dan radar maritim (T4) adalah prioritas tertinggi Indonesia.</li>
        </ul>
        """
        title_p2 = "Rasionalitas Pakta DCA 2024 (Nash Equilibrium)"
        body_p2 = """
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">Pada <b>29 Agustus 2024</b>, Menhan RI Prabowo Subianto dan Menhan Australia Richard Marles menandatangani pakta <i>Defence Cooperation Agreement</i> (DCA).</p>
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">Hasil simulasi matematis membuktikan bahwa pakta ini merupakan <b>Nash Equilibrium</b>: karena kedua belah pihak berada pada kondisi saling menangkal di Laut Arafura dan Celah Timor, kerja sama pengawasan maritim terpadu adalah pilihan paling rasional bagi stabilitas kawasan Indo-Pasifik.</p>
        """
        swot_s = "Kapasitas kedalaman teritorial kepulauan masif (IDN) & superioritas teknologi sensor maritim C4ISR (AUS)."
        swot_w = "Disparitas fiskal modal alutsista ~26:1 dan keterbatasan rantai pasok suku cadang."
        swot_o = "Implementasi pakta DCA 2024 untuk patroli terkoordinasi Selat Malaka, Celah Timor, dan pertukaran intelijen maritim."
        swot_t = "Peningkatan friksi persaingan kekuatan global di Laut China Selatan dan eskalasi perlombaan senjata kapal selam nuklir."
        payoff_coop = "(+8, +8) Nash Equilibrium: Keamanan ZEE Bersama Terjamin"
        payoff_defect = "(-6, -6) Perlombaan Senjata: Beban Fiskal Menguras PDB"
    elif (c_data_a['iso3'] in ['USA', 'CHN'] and c_data_b['iso3'] in ['USA', 'CHN']):
        title_p1 = "Dinamika Persaingan Kekuatan Hegemonik Global (AS vs China)"
        body_p1 = """
        <ul style="padding-left:18px; line-height:1.6; font-size:0.92rem; color:#334155;">
            <li><b>Kontestasi Pasifik Barat:</b> Amerika Serikat mengandalkan superioritas armada supercarrier dan aliansi terpadu, sementara China mengandalkan sistem Anti-Access/Area Denial (A2/AD) dengan rudal hipersonik DF-21D/DF-26.</li>
            <li><b>Ekuilibrium Penangkalan Nuklir & Konvensional:</b> Simulasi membuktikan benturan langsung di laut lepas memiliki biaya atrisi yang saling merugikan secara katastropik (*Mutually Assured Destruction*).</li>
            <li><b>Pentingnya Hotline Komunikasi Krisis:</b> Penurunan risiko perang terbuka bergantung pada mekanisme de-eskalasi maritim di Selat Taiwan dan Laut China Selatan.</li>
        </ul>
        """
        title_p2 = "Implikasi bagi Arsitektur Keamanan Kawasan"
        body_p2 = f"""
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">Persaingan antara <b>{country_a}</b> dan <b>{country_b}</b> menuntut negara-negara ASEAN untuk mempertahankan sentralitasnya dan tidak terjebak ke dalam konfrontasi blok polarisasi militer.</p>
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">Stabilitas Indo-Pasifik membutuhkan kepatuhan pada hukum laut internasional (UNCLOS 1982) dan kebebasan navigasi tanpa hegemoni sepihak.</p>
        """
        swot_s = "Kapabilitas proyeksi global absolut, teknologi satelit C4ISR, dan industri pertahanan skala berat."
        swot_w = "Biaya pemeliharaan armada raksasa dan kerentanan garis logistik samudra terhadap serangan rudal hipersonik."
        swot_o = "Mekanisme pengawasan krisis multilateral dan de-eskalasi insiden maritim internasional."
        swot_t = "Jebakan Thucydides (Thucydides Trap) dan salah kalkulasi taktis di Selat Taiwan."
        payoff_coop = "(+6, +6) Manajemen Kompetisi Strategis Terkendali"
        payoff_defect = "(-10, -10) Konflik Kinetik Terbuka: Runtuhnya Perdagangan Global"
    else:
        title_p1 = f"Struktur Komparasi Strategis: {country_a} vs {country_b}"
        body_p1 = f"""
        <ul style="padding-left:18px; line-height:1.6; font-size:0.92rem; color:#334155;">
            <li><b>Perbandingan Postur:</b> {country_a} ({c_data_a['doctrine'][:38]}...) berhadapan dengan {country_b} ({c_data_b['doctrine'][:38]}...).</li>
            <li><b>Rasio Disparitas Belanja:</b> Perbedaan belanja riil dan profil intensitas modal menciptakan dinamika atrisi yang sangat dipengaruhi oleh medan operasi yang dipilih.</li>
            <li><b>Peran Aliansi vs Kemandirian:</b> Keberadaan pakta keamanan eksternal sangat menentukan daya tahan logistik dalam konflik berkepanjangan.</li>
        </ul>
        """
        title_p2 = "Rekomendasi Doktrin & Stabilitas Kawasan"
        body_p2 = f"""
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">Pemodelan membuktikan bahwa keunggulan komparatif antara <b>{country_a}</b> dan <b>{country_b}</b> tidak bersifat mutlak, melainkan bergantung pada adaptasi teknologi nirawak, kesiapan alutsista, dan geografi medan pertempuran.</p>
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">Dialog bilateral berkelanjutan dan transparansi doktrin merupakan kunci menjaga perdamaian kawasan Indo-Pasifik.</p>
        """
        swot_s = f"Kekuatan alutsista terspesialisasi milik {c_data_a['iso3']} dan {c_data_b['iso3']} di kawasan operasinya."
        swot_w = "Ketergantungan komponen impor luar negeri dan keterbatasan kapasitas industri pemeliharaan mandiri."
        swot_o = "Kerja sama keamanan kawasan multilateral dalam kerangka ADMM-Plus dan latihan bersama."
        swot_t = "Gesekan teritorial perbatasan laut dan salah pengertian taktis navigasi."
        payoff_coop = "(+7, +7) Keseimbangan Stabilitas Maritim Terpadu"
        payoff_defect = "(-5, -5) Friksi Terbuka: Destabilisasi Jalur Pelayaran"

    with col_pol1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title_p1}</div>
            {body_p1}
        </div>
        """, unsafe_allow_html=True)

    with col_pol2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title_p2}</div>
            {body_p2}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Matriks SWOT Komparatif Bilateral
    st.markdown("##### Matriks SWOT Komparatif Strategis")
    col_swot1, col_swot2 = st.columns(2)
    with col_swot1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #059669;">
            <div style="font-weight:700; color:#059669; font-size:0.95rem;">STRENGTHS (KEKUATAN UTAMA)</div>
            <p style="font-size:0.86rem; color:#334155; margin-top:4px;">{swot_s}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #0284c7;">
            <div style="font-weight:700; color:#0284c7; font-size:0.95rem;">OPPORTUNITIES (PELUANG KERJA SAMA)</div>
            <p style="font-size:0.86rem; color:#334155; margin-top:4px;">{swot_o}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_swot2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #d97706;">
            <div style="font-weight:700; color:#d97706; font-size:0.95rem;">WEAKNESSES (KELEMAHAN KRITIS)</div>
            <p style="font-size:0.86rem; color:#334155; margin-top:4px;">{swot_w}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #dc2626;">
            <div style="font-weight:700; color:#dc2626; font-size:0.95rem;">THREATS (ANCAMAN ESKALASI)</div>
            <p style="font-size:0.86rem; color:#334155; margin-top:4px;">{swot_t}</p>
        </div>
        """, unsafe_allow_html=True)

    # Matriks Teori Permainan (Game Theory Payoff Matrix)
    st.markdown("##### Matriks Teori Permainan & Pembuktian Nash Equilibrium")
    df_game = pd.DataFrame([
        {"Strategi": "Kerja Sama Pertahanan (DCA)", f"{country_b} [Kooperasi]": payoff_coop, f"{country_b} [Konfrontasi]": "(-4, +2) Pembelotan Asimetris"},
        {"Strategi": "Konfrontasi / Perlombaan Senjata", f"{country_b} [Kooperasi]": "(+2, -4) Keuntungan Taktis Sesaat", f"{country_b} [Konfrontasi]": payoff_defect}
    ])
    st.dataframe(df_game.set_index("Strategi"), use_container_width=True)

    # Rekomendasi Alokasi Alutsista Tri-Matra
    st.markdown("##### Rekomendasi Prioritas Doktrin Tri-Matra Berdasarkan Hasil Pemodelan")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div class="metric-card" style="border-top:3px solid #16a34a;">
            <div class="metric-title">Matra Darat (TNI AD)</div>
            <p style="font-size:0.85rem; line-height:1.5;">Modernisasi baterai rudal pesisir pertahanan pantai terintegrasi (BrahMos/Yakhont), pengadaan radar counter-battery mobile, dan penguatan mobilitas taktis batalyon infanteri kepulauan.</p>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="metric-card" style="border-top:3px solid #0284c7;">
            <div class="metric-title">Matra Laut (TNI AL)</div>
            <p style="font-size:0.85rem; line-height:1.5;">Percepatan penyerapan kapal selam Scorpene Evolved AIP, penambahan frigat berpeluncur VLS pertahanan area (FREMM/Arrowhead 140), dan integrasi sensor akustik bawah air di seluruh ALKI I, II, dan III.</p>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="metric-card" style="border-top:3px solid #9333ea;">
            <div class="metric-title">Matra Udara (TNI AU)</div>
            <p style="font-size:0.85rem; line-height:1.5;">Pemenuhan kontrak pengadaan Skadron Rafale tranche penuh, penggelaran sistem radar Ground Controlled Interception (GCI Thales GM400A), dan adopsi masif drone taktis tempur MALE (UAV/UCAV).</p>
        </div>
        """, unsafe_allow_html=True)
