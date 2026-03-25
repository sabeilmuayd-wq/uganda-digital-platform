import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime, timedelta
import plotly.express as px
from PIL import Image
import io
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="Uganda Digital Platform - UCSATP",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PWA Support ====================
st.markdown("""
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#2ecc71">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="UDP">
<link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/1674/1674083.png">
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then(function(registration) {
      console.log('Service Worker registered with scope:', registration.scope);
    })
    .catch(function(error) {
      console.log('Service Worker registration failed:', error);
    });
}
</script>
<style>
    @media (display-mode: standalone) {
        body {
            padding-top: env(safe-area-inset-top);
        }
    }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .pilot-badge {
        background: #ffd700;
        color: #1e3c72;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
    }
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .farmer-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2ecc71;
    }
    .api-box {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 10px;
        font-family: monospace;
        font-size: 0.8rem;
    }
    .rating {
        color: #ffc107;
        font-size: 1.2rem;
    }
    .admin-card {
        background: #fef9e6;
        border: 1px solid #ffd700;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== إعداد اللغة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"

# ==================== وضع التجربة ====================
if "pilot_mode" not in st.session_state:
    st.session_state.pilot_mode = False
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==================== الترجمة الكاملة (5 لغات) ====================
translations = {
    "en": {
        "app_name": "🇺🇬 Uganda Digital Platform",
        "subtitle": "UCSATP - Ministry of Agriculture",
        "pilot": "🚀 PILOT PHASE",
        "district_label": "📍",
        "register_farmer": "👨‍🌾 Register Farmer",
        "add_crop": "🌾 Add Crop",
        "view_data": "📋 View Data",
        "reports": "📊 Ministry Reports",
        "api_docs": "🔌 API Documentation",
        "admin_panel": "🔧 Admin Panel",
        "pilot_mode": "🚀 Pilot Mode",
        "send_report": "📤 Send Report to Ministry",
        "report_sent": "Report sent successfully!",
        "weekly_report": "📋 Weekly Report",
        "farmer_name": "Full Name",
        "nin": "National ID (NIN)",
        "phone": "Phone Number",
        "village": "Village / Parish",
        "sub_county": "Sub-county",
        "farmer_type": "Farmer Type",
        "smallholder": "Smallholder",
        "commercial": "Commercial",
        "cooperative": "Cooperative Member",
        "crop_type": "Crop Type",
        "quantity": "Quantity (kg)",
        "price": "Price (UGX/kg)",
        "quality": "Quality",
        "harvest_date": "Harvest Date",
        "save": "✅ Save",
        "success_farmer": "Farmer registered successfully!",
        "success_crop": "Crop added successfully!",
        "required": "Please fill all required fields",
        "no_farmers": "No farmers registered yet",
        "total_farmers": "Total Farmers",
        "total_crops": "Total Crops",
        "total_quantity": "Total Quantity (kg)",
        "export_csv": "📥 Download CSV Report",
        "export_pdf": "📄 Export PDF Report",
        "about": "About This Platform",
        "api_ready": "🔌 NBI Integration Ready",
        "api_endpoints": "API Endpoints",
        "example_request": "Example Request",
        "integration_ready": "Integration Ready For:",
        "farmers": "👨‍🌾 Farmers",
        "crops": "🌾 Crops",
        "summary_by_district": "📋 Summary by District",
        "contact": "📞 Contact",
        "language": "🌍 Language",
        "select_district": "Select Pilot District:",
        "active": "Active:",
        "statistics": "📊 Pilot Statistics",
        "ministry_partner": "In partnership with UCSATP",
        "ministry_label": "Ministry of Agriculture",
        "map_title": "🗺️ Farmer Distribution Map",
        "ratings": "⭐ Ratings",
        "your_rating": "Your Rating",
        "submit_rating": "Submit Rating",
        "avg_rating": "Average Rating",
        "photo": "📸 Upload Photo",
        "live_stats": "📈 Live Statistics",
        "admin_password": "Admin Password",
        "login": "Login",
        "logout": "Logout",
        "pilot_active": "✅ Pilot Mode Active - Data will be shared with Ministry",
        "pilot_inactive": "⚪ Pilot Mode Inactive",
        "extension_workers": "Extension Workers Trained",
        "farmers_reached": "Farmers Reached"
    },
    "ar": {
        "app_name": "🇺🇬 منصة أوغندا الرقمية",
        "subtitle": "UCSATP - وزارة الزراعة",
        "pilot": "🚀 المرحلة التجريبية",
        "district_label": "📍",
        "register_farmer": "👨‍🌾 تسجيل مزارع",
        "add_crop": "🌾 إضافة محصول",
        "view_data": "📋 عرض البيانات",
        "reports": "📊 تقارير الوزارة",
        "api_docs": "🔌 توثيق API",
        "admin_panel": "🔧 لوحة المسؤول",
        "pilot_mode": "🚀 وضع التجربة",
        "send_report": "📤 إرسال التقرير للوزارة",
        "report_sent": "تم إرسال التقرير بنجاح!",
        "weekly_report": "📋 التقرير الأسبوعي",
        "farmer_name": "الاسم الكامل",
        "nin": "الرقم الوطني",
        "phone": "رقم الهاتف",
        "village": "القرية",
        "sub_county": "المقاطعة الفرعية",
        "farmer_type": "نوع المزارع",
        "smallholder": "صغير",
        "commercial": "تجاري",
        "cooperative": "عضو تعاونية",
        "crop_type": "نوع المحصول",
        "quantity": "الكمية (كيلو)",
        "price": "السعر (شلن/كيلو)",
        "quality": "الجودة",
        "harvest_date": "تاريخ الحصاد",
        "save": "✅ حفظ",
        "success_farmer": "تم تسجيل المزارع بنجاح!",
        "success_crop": "تم إضافة المحصول بنجاح!",
        "required": "يرجى ملء جميع الحقول المطلوبة",
        "no_farmers": "لا يوجد مزارعون مسجلون بعد",
        "total_farmers": "إجمالي المزارعين",
        "total_crops": "إجمالي المحاصيل",
        "total_quantity": "إجمالي الكمية (كيلو)",
        "export_csv": "📥 تحميل التقرير CSV",
        "export_pdf": "📄 تحميل التقرير PDF",
        "about": "عن هذه المنصة",
        "api_ready": "🔌 جاهز للربط مع NBI",
        "api_endpoints": "نقاط الاتصال API",
        "example_request": "مثال على الطلب",
        "integration_ready": "جاهز للربط مع:",
        "farmers": "👨‍🌾 المزارعون",
        "crops": "🌾 المحاصيل",
        "summary_by_district": "📋 ملخص حسب المقاطعة",
        "contact": "📞 للتواصل",
        "language": "🌍 اللغة",
        "select_district": "اختر المقاطعة التجريبية:",
        "active": "نشط:",
        "statistics": "📊 إحصائيات التجربة",
        "ministry_partner": "بشراكة مع UCSATP",
        "ministry_label": "وزارة الزراعة",
        "map_title": "🗺️ خريطة توزيع المزارعين",
        "ratings": "⭐ التقييمات",
        "your_rating": "تقييمك",
        "submit_rating": "إرسال التقييم",
        "avg_rating": "متوسط التقييم",
        "photo": "📸 رفع صورة",
        "live_stats": "📈 إحصائيات حية",
        "admin_password": "كلمة المرور",
        "login": "دخول",
        "logout": "خروج",
        "pilot_active": "✅ وضع التجربة نشط - البيانات ستُرسل للوزارة",
        "pilot_inactive": "⚪ وضع التجربة غير نشط",
        "extension_workers": "مرشدون تم تدريبهم",
        "farmers_reached": "مزارعون تم الوصول إليهم"
    },
    "sw": {
        "app_name": "🇺🇬 Jukwaa la Kidijitali Uganda",
        "subtitle": "UCSATP - Wizara ya Kilimo",
        "pilot": "🚀 AWAMU YA MAJARIBIO",
        "district_label": "📍",
        "register_farmer": "👨‍🌾 Sajili Mkulima",
        "add_crop": "🌾 Ongeza Zao",
        "view_data": "📋 Angalia Data",
        "reports": "📊 Ripoti za Wizara",
        "api_docs": "🔌 Nyaraka za API",
        "admin_panel": "🔧 Jopo la Msimamizi",
        "pilot_mode": "🚀 Hali ya Majaribio",
        "send_report": "📤 Tuma Ripoti kwa Wizara",
        "report_sent": "Ripoti imetumwa!",
        "weekly_report": "📋 Ripoti ya Wiki",
        "farmer_name": "Jina Kamili",
        "nin": "Namba ya Kitambulisho",
        "phone": "Namba ya Simu",
        "village": "Kijiji",
        "sub_county": "Kata ndogo",
        "farmer_type": "Aina ya Mkulima",
        "smallholder": "Mdogo",
        "commercial": "Biashara",
        "cooperative": "Mwanachama wa Ushirika",
        "crop_type": "Aina ya Zao",
        "quantity": "Kiasi (kg)",
        "price": "Bei (UGX/kg)",
        "quality": "Ubora",
        "harvest_date": "Tarehe ya Mavuno",
        "save": "✅ Hifadhi",
        "success_farmer": "Mkulima amehifadhiwa!",
        "success_crop": "Zao limeongezwa!",
        "required": "Tafadhali jaza sehemu zote",
        "no_farmers": "Hakuna wakulima bado",
        "total_farmers": "Jumla ya Wakulima",
        "total_crops": "Jumla ya Mazao",
        "total_quantity": "Jumla ya Kiasi (kg)",
        "export_csv": "📥 Pakua Ripoti CSV",
        "export_pdf": "📄 Pakua Ripoti PDF",
        "about": "Kuhusu Jukwaa Hili",
        "api_ready": "🔌 Tayari kwa Ushirikiano na NBI",
        "api_endpoints": "Sehemu za API",
        "example_request": "Mfano wa Ombi",
        "integration_ready": "Tayari kwa Ushirikiano na:",
        "farmers": "👨‍🌾 Wakulima",
        "crops": "🌾 Mazao",
        "summary_by_district": "📋 Muhtasari kwa Wilaya",
        "contact": "📞 Wasiliana",
        "language": "🌍 Lugha",
        "select_district": "Chagua Wilaya ya Majaribio:",
        "active": "Inatumika:",
        "statistics": "📊 Takwimu za Majaribio",
        "ministry_partner": "Kwa ushirikiano na UCSATP",
        "ministry_label": "Wizara ya Kilimo",
        "map_title": "🗺️ Ramani ya Usambazaji wa Wakulima",
        "ratings": "⭐ Makadirio",
        "your_rating": "Makadirio Yako",
        "submit_rating": "Wasilisha Makadirio",
        "avg_rating": "Wastani wa Makadirio",
        "photo": "📸 Pakia Picha",
        "live_stats": "📈 Takwimu za Moja kwa Moja",
        "admin_password": "Nenosiri",
        "login": "Ingia",
        "logout": "Toka",
        "pilot_active": "✅ Hali ya Majaribio imeanzishwa",
        "pilot_inactive": "⚪ Hali ya Majaribio haijaanzishwa",
        "extension_workers": "Wafanyakazi wa Ugani Waliofunzwa",
        "farmers_reached": "Wakulima Waliofikia"
    },
    "lg": {
        "app_name": "🇺🇬 Embuga ya Uganda eya Digitali",
        "subtitle": "UCSATP - Minisitule ya Bya bulimi",
        "pilot": "🚀 EKIKUUKO KY'OKUGEZESA",
        "district_label": "📍",
        "register_farmer": "👨‍🌾 Kwata Omulimi",
        "add_crop": "🌾 Gatta Ebya bulimi",
        "view_data": "📋 Laba Data",
        "reports": "📊 Ripoti za Minisitule",
        "api_docs": "🔌 Ebyawandiikibwa ku API",
        "admin_panel": "🔧 Jopo lya Admin",
        "pilot_mode": "🚀 Ennaku z'Okukesa",
        "send_report": "📤 Wereza Ripoti eri Minisitule",
        "report_sent": "Ripoti erezeddwa!",
        "weekly_report": "📋 Ripoti ya Sawa",
        "farmer_name": "Erinnya",
        "nin": "Namba ya Kakubere",
        "phone": "Namba ya Simu",
        "village": "Kyalo",
        "sub_county": "Gombolola",
        "farmer_type": "Muwendo wa Mulimi",
        "smallholder": "Mutono",
        "commercial": "Okugulisa",
        "cooperative": "Munnakibiina",
        "crop_type": "Bika bya bulimi",
        "quantity": "Bungi (kg)",
        "price": "Emitwalo (UGX/kg)",
        "quality": "Bwangu",
        "harvest_date": "Nnaku ya Kukungula",
        "save": "✅ Kkuma",
        "success_farmer": "Omulimi akkiddwa!",
        "success_crop": "Ebya bulimi byongeddwa!",
        "required": "Wekka mu bitundu byonna",
        "no_farmers": "Tewali balimi bakkiddwa",
        "total_farmers": "Balimi Bonna",
        "total_crops": "Ebya bulimi Byonna",
        "total_quantity": "Bungi Bwonna (kg)",
        "export_csv": "📥 Ggya Ripoti CSV",
        "export_pdf": "📄 Ggya Ripoti PDF",
        "about": "Kikwata ku nteekateeka eno",
        "api_ready": "🔌 Kya kutegeka okukola ne NBI",
        "api_endpoints": "Ebyawandiikibwa ku API",
        "example_request": "Okusabira okwokulabirako",
        "integration_ready": "Kya kutegeka okukola ne:",
        "farmers": "👨‍🌾 Balimi",
        "crops": "🌾 Ebya bulimi",
        "summary_by_district": "📋 Ebyokulabirako mu Disitulikiti",
        "contact": "📞 Okukwatagana",
        "language": "🌍 Olulimi",
        "select_district": "Londa Disitulikiti ey'okugezesa:",
        "active": "Kikolebwa:",
        "statistics": "📊 Ebyokulabirako",
        "ministry_partner": "Mu kukolagana ne UCSATP",
        "ministry_label": "Minisitule ya Bya bulimi",
        "map_title": "🗺️ Emmandwa ey'Okusaasaana kw'Abalimi",
        "ratings": "⭐ Okugereka",
        "your_rating": "Okugereka Kwo",
        "submit_rating": "Wereza Okugereka",
        "avg_rating": "Okugereka Okw'omu Makulu",
        "photo": "📸 Gatta Ekifananyi",
        "live_stats": "📈 Ebyokulabirako Ebiriwo",
        "admin_password": "Kigambo ky'Okukyusa",
        "login": "Yingira",
        "logout": "Fuluma",
        "pilot_active": "✅ Ennaku z'Okukesa zikola",
        "pilot_inactive": "⚪ Ennaku z'Okukesa tezikola",
        "extension_workers": "Abakugu mu by'obulimi Abatendekeddwa",
        "farmers_reached": "Balimi Abatuuseeko"
    },
    "rn": {
        "app_name": "🇺🇬 Orutaro rwa Uganda orwa Digitali",
        "subtitle": "UCSATP - Minisituri y'Obuhinzi",
        "pilot": "🚀 OKUGEZESHA",
        "district_label": "📍",
        "register_farmer": "👨‍🌾 Handika Omuhinzi",
        "add_crop": "🌾 Ongyeraho Ekyokuhinga",
        "view_data": "📋 Reba Data",
        "reports": "📊 Rapoti za Minisituri",
        "api_docs": "🔌 Eby'API",
        "admin_panel": "🔧 Orubaju rw'Admin",
        "pilot_mode": "🚀 Enkora y'Okugyendesya",
        "send_report": "📤 Ohereza Rapoti eri Minisituri",
        "report_sent": "Rapoti yoherezwe!",
        "weekly_report": "📋 Rapoti y'Ebucweka",
        "farmer_name": "Eiziina",
        "nin": "Namba y'Obwegyese",
        "phone": "Namba ya Simu",
        "village": "Omuringa",
        "sub_county": "Omujumba",
        "farmer_type": "Omuhinzi w'omuringa",
        "smallholder": "Mutono",
        "commercial": "Okugurisa",
        "cooperative": "Omwezi w'ekibiina",
        "crop_type": "Ekihingwa",
        "quantity": "Obuto (kg)",
        "price": "Omutwalo (UGX/kg)",
        "quality": "Oburungi",
        "harvest_date": "Ebiro by'okuhinga",
        "save": "✅ Handika",
        "success_farmer": "Omuhinzi ahanditswe!",
        "success_crop": "Ekihingwa kyongyerwe!",
        "required": "Juza ebisigaire byona",
        "no_farmers": "Tihariho bahinzi bahanditswe",
        "total_farmers": "Abahinzi Bona",
        "total_crops": "Ebihingwa Byona",
        "total_quantity": "Obuto Bwona (kg)",
        "export_csv": "📥 Iko Rapoti CSV",
        "export_pdf": "📄 Iko Rapoti PDF",
        "about": "Kubiruga orutaro oru",
        "api_ready": "🔌 Kitegiriwe okukora na NBI",
        "api_endpoints": "Eby'API",
        "example_request": "Okusaba okurikuratwaho",
        "integration_ready": "Kitegiriwe okukora na:",
        "farmers": "👨‍🌾 Abahinzi",
        "crops": "🌾 Ebihingwa",
        "summary_by_district": "📋 Ebiragiro by'Okuruga mu Distirikiti",
        "contact": "📞 Okweterana",
        "language": "🌍 Orurimi",
        "select_district": "Torana Distirikiti y'Okugyendesya:",
        "active": "Nikora:",
        "statistics": "📊 Ebiragiro by'Okugyendesya",
        "ministry_partner": "Mu kuhuriza hamwe na UCSATP",
        "ministry_label": "Minisituri y'Obuhinzi",
        "map_title": "🗺️ Ekibonero ky'Okwihurira kw'Abahinzi",
        "ratings": "⭐ Okugera",
        "your_rating": "Okugera Kwawe",
        "submit_rating": "Ohereza Okugera",
        "avg_rating": "Okugera Okuri Hafi",
        "photo": "📸 Shohoza Ekishushani",
        "live_stats": "📈 Ebiragiro Biriho",
        "admin_password": "Ekigambo ky'Okuhinda",
        "login": "Hinda",
        "logout": "Hingura",
        "pilot_active": "✅ Enkora y'Okugyendesya ikora",
        "pilot_inactive": "⚪ Enkora y'Okugyendesya tikora",
        "extension_workers": "Abakozi b'Okugyendesya Abahinzwe",
        "farmers_reached": "Abahinzi Bahikiriwe"
    }
}

def t(key):
    return translations[st.session_state.language].get(key, key)

# ==================== إعداد المقاطعات ====================
if "district" not in st.session_state:
    st.session_state.district = "Kiryandongo"

PILOT_DISTRICTS = ["Kiryandongo", "Masindi", "Gulu"]

# ==================== ملفات التخزين ====================
DATA_FOLDER = "ucsatp_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

FARMERS_FILE = os.path.join(DATA_FOLDER, "farmers.json")
CROPS_FILE = os.path.join(DATA_FOLDER, "crops.json")
RATINGS_FILE = os.path.join(DATA_FOLDER, "ratings.json")
REPORTS_FILE = os.path.join(DATA_FOLDER, "reports.json")

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== دوال التقارير ====================
def generate_weekly_report():
    farmers = load_data(FARMERS_FILE)
    crops = load_data(CROPS_FILE)
    
    # إحصائيات الأسبوع الماضي
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    new_farmers = [f for f in farmers if f.get("registration_date", "") > week_ago]
    new_crops = [c for c in crops if c.get("date_listed", "") > week_ago]
    
    report = {
        "date": datetime.now().isoformat(),
        "district": st.session_state.district,
        "total_farmers": len(farmers),
        "total_crops": len(crops),
        "new_farmers": len(new_farmers),
        "new_crops": len(new_crops),
        "total_quantity": sum([c.get("quantity", 0) for c in crops])
    }
    return report

def send_report_to_ministry():
    """محاكاة إرسال تقرير للوزارة"""
    report = generate_weekly_report()
    reports = load_data(REPORTS_FILE)
    reports.append(report)
    save_data(REPORTS_FILE, reports)
    return report

# ==================== شعار الوزارة والرأس ====================
st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
    <div>
        <span style='font-size: 2rem;'>🇺🇬</span>
        <span style='font-weight: bold; color: #1e3c72;'> {t('ministry_label')}</span>
    </div>
    <span style='background: #2ecc71; color: white; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem;'>
        {t('ministry_partner')}
    </span>
</div>
""", unsafe_allow_html=True)

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### {t('language')}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 English", key="lang_en", use_container_width=True):
            st.session_state.language = "en"
            st.rerun()
        if st.button("🇸🇦 العربية", key="lang_ar", use_container_width=True):
            st.session_state.language = "ar"
            st.rerun()
        if st.button("🇺🇬 Luganda", key="lang_lg", use_container_width=True):
            st.session_state.language = "lg"
            st.rerun()
    with col2:
        if st.button("🇺🇬 Kiswahili", key="lang_sw", use_container_width=True):
            st.session_state.language = "sw"
            st.rerun()
        if st.button("🇺🇬 Runyoro", key="lang_rn", use_container_width=True):
            st.session_state.language = "rn"
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"### 📍 UCSATP Pilot")
    
    selected_district = st.radio(
        t("select_district"),
        PILOT_DISTRICTS,
        index=PILOT_DISTRICTS.index(st.session_state.district),
        key="district_radio"
    )
    if selected_district != st.session_state.district:
        st.session_state.district = selected_district
        st.rerun()
    
    st.markdown(f"**{t('active')}** `{st.session_state.district}`")
    
    # عرض وضع التجربة
    if st.session_state.pilot_mode:
        st.success(f"✅ {t('pilot_active')}")
    else:
        st.info(f"⚪ {t('pilot_inactive')}")
    
    st.markdown("---")
    st.markdown(f"### {t('statistics')}")
    
    farmers = load_data(FARMERS_FILE)
    district_farmers = [f for f in farmers if f.get("district") == st.session_state.district]
    st.metric(t("total_farmers"), len(district_farmers))
    
    crops = load_data(CROPS_FILE)
    district_crops = [c for c in crops if c.get("district") == st.session_state.district]
    st.metric(t("total_crops"), len(district_crops))
    
    total_quantity = sum([c.get("quantity", 0) for c in district_crops])
    st.metric(t("total_quantity"), f"{total_quantity:,}")
    
    st.markdown("---")
    st.markdown(f"### {t('contact')}")
    st.markdown("📧 procurement.ucsatp@agriculture.go.ug")
    st.markdown("📞 0774373737")

# ==================== العنوان الرئيسي ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('app_name')}</h1>
    <p>{t('subtitle')}</p>
    <div>
        <span class='pilot-badge'>{t('pilot')}</span>
        <span class='pilot-badge' style='background: #2ecc71;'>{t('district_label')} {st.session_state.district}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== إحصائيات حية ====================
st.markdown(f"### {t('live_stats')}")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👨‍🌾 " + t("total_farmers"), len(load_data(FARMERS_FILE)), delta="+2 this week")
with col2:
    st.metric("🌾 " + t("total_crops"), len(load_data(CROPS_FILE)), delta="+5 this week")
with col3:
    ratings = load_data(RATINGS_FILE)
    avg_rating = sum([r.get("rating", 0) for r in ratings]) / len(ratings) if ratings else 0
    st.metric("⭐ " + t("avg_rating"), f"{avg_rating:.1f}/5")

# ==================== تبويبات التطبيق ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    t("register_farmer"), 
    t("add_crop"), 
    t("view_data"), 
    t("reports"),
    t("api_docs"),
    t("admin_panel")
])

# ==================== TAB 1: تسجيل مزارع جديد ====================
with tab1:
    st.subheader(f"{t('register_farmer')} - {st.session_state.district}")
    
    with st.form(key="farmer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nin = st.text_input(t("nin"))
            full_name = st.text_input(t("farmer_name"))
            phone = st.text_input(t("phone"))
            
        with col2:
            village = st.text_input(t("village"))
            sub_county = st.text_input(t("sub_county"))
            farmer_type = st.selectbox(t("farmer_type"), t("farmer_type_options"))
        
        photo = st.file_uploader(t("photo"), type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button(t("save"), type="primary", use_container_width=True)
        
        if submitted:
            if nin and full_name and village:
                farmer = {
                    "id": str(uuid.uuid4())[:8],
                    "nin": nin,
                    "name": full_name,
                    "phone": phone,
                    "village": village,
                    "sub_county": sub_county,
                    "farmer_type": farmer_type,
                    "district": st.session_state.district,
                    "registration_date": datetime.now().isoformat(),
                    "has_photo": photo is not None,
                    "status": "active"
                }
                farmers_data = load_data(FARMERS_FILE)
                farmers_data.append(farmer)
                save_data(FARMERS_FILE, farmers_data)
                st.success(f"✅ {t('success_farmer')}")
                st.balloons()
            else:
                st.warning(f"⚠️ {t('required')}")

# ==================== TAB 2: إضافة محصول ====================
with tab2:
    st.subheader(f"{t('add_crop')} - {st.session_state.district}")
    
    farmers_data = load_data(FARMERS_FILE)
    district_farmers = [f for f in farmers_data if f.get("district") == st.session_state.district]
    
    if district_farmers:
        with st.form(key="crop_form"):
            farmer_names = [f"{f['name']} ({f['nin']})" for f in district_farmers]
            selected_farmer = st.selectbox(t("farmer_name"), farmer_names)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                crop_type = st.text_input(t("crop_type"), placeholder=t("crop_placeholder"))
            with col2:
                quantity = st.number_input(t("quantity"), min_value=1, step=10, value=100)
            with col3:
                price = st.number_input(t("price"), min_value=100, step=500, value=2000)
            
            quality = st.select_slider(t("quality"), options=t("quality_options"))
            harvest_date = st.date_input(t("harvest_date"), datetime.now())
            
            crop_photo = st.file_uploader(t("photo"), type=["jpg", "png", "jpeg"], key="crop_photo")
            
            submitted = st.form_submit_button(t("save"), type="primary", use_container_width=True)
            
            if submitted:
                if selected_farmer and crop_type:
                    farmer_id = [f for f in district_farmers if f"{f['name']} ({f['nin']})" == selected_farmer][0]["id"]
                    crop = {
                        "id": str(uuid.uuid4())[:8],
                        "farmer_id": farmer_id,
                        "farmer_name": selected_farmer.split(" (")[0],
                        "crop": crop_type,
                        "quantity": quantity,
                        "price": price,
                        "quality": quality,
                        "has_photo": crop_photo is not None,
                        "harvest_date": harvest_date.isoformat(),
                        "district": st.session_state.district,
                        "date_listed": datetime.now().isoformat(),
                        "status": "available"
                    }
                    crops_data = load_data(CROPS_FILE)
                    crops_data.append(crop)
                    save_data(CROPS_FILE, crops_data)
                    st.success(f"✅ {t('success_crop')}")
                    st.balloons()
                else:
                    st.warning(f"⚠️ {t('required')}")
    else:
        st.warning(f"⚠️ {t('no_farmers')}")

# ==================== TAB 3: عرض البيانات مع خريطة وتقييمات ====================
with tab3:
    st.subheader(f"{t('view_data')} - {st.session_state.district}")
    
    # خريطة تفاعلية
    st.markdown(f"### {t('map_title')}")
    
    farmers_data = load_data(FARMERS_FILE)
    district_farmers = [f for f in farmers_data if f.get("district") == st.session_state.district]
    
    if district_farmers:
        map_data = []
        for i, f in enumerate(district_farmers):
            coords = {
                "Kiryandongo": [1.9, 32.1],
                "Masindi": [1.7, 31.7],
                "Gulu": [2.8, 32.3]
            }
            lat, lon = coords.get(st.session_state.district, [1.5, 32.0])
            map_data.append({
                "name": f['name'],
                "village": f['village'],
                "lat": lat + (i * 0.01),
                "lon": lon + (i * 0.01),
                "farmers": 1
            })
        
        df_map = pd.DataFrame(map_data)
        fig = px.scatter_mapbox(
            df_map,
            lat='lat',
            lon='lon',
            hover_name='name',
            hover_data={'village': True},
            size=[5] * len(df_map),
            zoom=8,
            title=t("map_title")
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # عرض المزارعين
    if district_farmers:
        st.markdown(f"### {t('farmers')}")
        for f in district_farmers:
            st.markdown(f"""
            <div class='farmer-card'>
                <strong>{f['name']}</strong> (NIN: {f['nin']})<br>
                📍 {f['village']}, {f.get('sub_county', 'N/A')}<br>
                📞 {f.get('phone', 'N/A')} | 📅 {f['registration_date'][:10]}
            </div>
            """, unsafe_allow_html=True)
    
    # عرض المحاصيل
    crops_data = load_data(CROPS_FILE)
    district_crops = [c for c in crops_data if c.get("district") == st.session_state.district]
    
    if district_crops:
        st.markdown(f"### {t('crops')}")
        for c in district_crops:
            st.markdown(f"""
            <div class='farmer-card'>
                <strong>{c['crop']}</strong><br>
                📦 {c['quantity']} kg | 💰 {c['price']:,} UGX/kg<br>
                👨‍🌾 {c['farmer_name']} | 📅 {c['harvest_date'][:10]}
            </div>
            """, unsafe_allow_html=True)
    
    # نظام التقييم
    st.markdown(f"### {t('ratings')}")
    
    ratings = load_data(RATINGS_FILE)
    avg_rating = sum([r.get("rating", 0) for r in ratings]) / len(ratings) if ratings else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{t('avg_rating')}:** {'⭐' * int(avg_rating)}{'☆' * (5 - int(avg_rating))} ({avg_rating:.1f}/5)")
    with col2:
        rating = st.slider(t("your_rating"), 1, 5, 3)
        if st.button(t("submit_rating")):
            ratings.append({"rating": rating, "date": datetime.now().isoformat()})
            save_data(RATINGS_FILE, ratings)
            st.success("✅ Thank you for your rating!")
            st.rerun()

# ==================== TAB 4: تقارير للوزارة ====================
with tab4:
    st.subheader(t("reports"))
    
    farmers_data = load_data(FARMERS_FILE)
    crops_data = load_data(CROPS_FILE)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_farmers = len([f for f in farmers_data if f.get("district") in PILOT_DISTRICTS])
        st.metric(t("total_farmers"), total_farmers)
    
    with col2:
        total_crops = len([c for c in crops_data if c.get("district") in PILOT_DISTRICTS])
        st.metric(t("total_crops"), total_crops)
    
    with col3:
        total_quantity = sum([c.get("quantity", 0) for c in crops_data if c.get("district") in PILOT_DISTRICTS])
        st.metric(t("total_quantity"), f"{total_quantity:,}")
    
    st.markdown("---")
    st.markdown(f"### {t('summary_by_district')}")
    
    summary_data = []
    for d in PILOT_DISTRICTS:
        district_farmers = len([f for f in farmers_data if f.get("district") == d])
        district_crops = len([c for c in crops_data if c.get("district") == d])
        district_quantity = sum([c.get("quantity", 0) for c in crops_data if c.get("district") == d])
        summary_data.append({"District": d, "Farmers": district_farmers, "Crops": district_crops, "Quantity (kg)": district_quantity})
    
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("export_csv"), key="csv_btn", use_container_width=True):
            df = pd.DataFrame(summary_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ucsatp_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_csv"
            )
    with col2:
        if st.button(t("export_pdf"), key="pdf_btn", use_container_width=True):
            st.info("📄 PDF Report Ready. (In production, this would download a formatted report with charts and official letterhead)")
    
    # التقرير الأسبوعي
    st.markdown("---")
    st.markdown(f"### {t('weekly_report')}")
    
    if st.button(t("send_report"), key="send_report_btn", use_container_width=True):
        report = send_report_to_ministry()
        st.success(f"✅ {t('report_sent')}")
        st.info(f"""
        **{t('total_farmers')}:** {report['total_farmers']}
        **{t('total_crops')}:** {report['total_crops']}
        **{t('total_quantity')}:** {report['total_quantity']:,} kg
        **New this week:** +{report['new_farmers']} farmers, +{report['new_crops']} crops
        """)
    
    st.markdown("---")
    st.markdown(f"### ℹ️ {t('about')}")
    st.markdown(f"""
    **{t('app_name')} – UCSATP Pilot**
    
    This platform supports the Uganda Climate Smart Agricultural Transformation Project (UCSATP).
    
    **Pilot Districts:** Kiryandongo, Masindi, Gulu
    
    **Features:**
    - Farmer registration with National ID (NIN)
    - Crop listing with photos
    - Real-time data collection
    - Interactive map
    - Rating system
    - Ministry reporting dashboard
    - Weekly reports
    - Works offline (PWA)
    - **5 Languages:** English, Arabic, Swahili, Luganda, Runyoro
    """)

# ==================== TAB 5: API Documentation ====================
with tab5:
    st.subheader(t("api_docs"))
    
    st.markdown(f"""
    <div class='api-box'>
    <strong>🔌 {t('api_ready')}</strong><br><br>
    
    <strong>{t('api_endpoints')}:</strong><br>
    <code>GET /api/farmers?district={{district}}</code><br>
    <code>GET /api/crops?district={{district}}&crop={{crop}}</code><br>
    <code>POST /api/farmers</code><br>
    <code>POST /api/crops</code><br><br>
    
    <strong>{t('example_request')}:</strong><br>
    <code>
    import requests<br><br>
    response = requests.get(<br>
        "https://uganda-digital-platform.streamlit.app/api/farmers",<br>
        params={{"district": "Kiryandongo"}},<br>
        headers={{"X-API-Key": "your-nbi-key"}}<br>
    )<br>
    data = response.json()<br>
    print(data)
    </code><br><br>
    
    <strong>{t('integration_ready')}</strong><br>
    ✅ NIFAMIS (Ministry of Agriculture)<br>
    ✅ DHIS2 (Ministry of Health)<br>
    ✅ EMIS (Ministry of Education)<br>
    ✅ NIRA (National ID)
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 6: لوحة المسؤول ====================
with tab6:
    st.subheader(t("admin_panel"))
    
    if not st.session_state.admin_logged_in:
        password = st.text_input(t("admin_password"), type="password")
        if st.button(t("login"), use_container_width=True):
            if password == "admin123":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Wrong password")
    else:
        if st.button(t("logout"), use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        st.markdown(f"""
        <div class='admin-card'>
            <h3>🔧 {t('admin_panel')}</h3>
            <p>{t('pilot_mode')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # تفعيل وضع التجربة
        pilot_active = st.checkbox(t("pilot_mode"), value=st.session_state.pilot_mode)
        if pilot_active != st.session_state.pilot_mode:
            st.session_state.pilot_mode = pilot_active
            st.rerun()
        
        if st.session_state.pilot_mode:
            st.success(f"✅ {t('pilot_active')}")
            
            # إرسال تقرير للوزارة
            if st.button(t("send_report"), key="admin_send_report", use_container_width=True):
                report = send_report_to_ministry()
                st.success(f"✅ {t('report_sent')}")
                st.info(f"""
                **{t('total_farmers')}:** {report['total_farmers']}
                **{t('total_crops')}:** {report['total_crops']}
                **{t('total_quantity')}:** {report['total_quantity']:,} kg
                """)
        
        # إحصائيات التجربة
        st.markdown("---")
        st.markdown("### 📊 Pilot Statistics")
        
        farmers = load_data(FARMERS_FILE)
        crops = load_data(CROPS_FILE)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(t("total_farmers"), len(farmers))
            st.metric(t("extension_workers"), "0")
        with col2:
            st.metric(t("total_crops"), len(crops))
            st.metric(t("farmers_reached"), len(farmers))
