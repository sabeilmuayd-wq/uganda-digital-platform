import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random
import plotly.express as px

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="Uganda Digital Platform",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== روابط التطبيقات الحقيقية ====================
APP_LINKS = {
    "soko_link": "https://soko-link-kfayyoqvr3shxvszm3y9rw.streamlit.app",
    "datacollect": "https://datacollect-ug-grpssnnub8pdr4anlafo2q.streamlit.app",
    "govfeedback": "https://mkdir-govfeedback-az6rjzjegwgktvf2mq6ypr.streamlit.app",
    "portfolio": "https://portfoliopy-bmxlappposgwybcasvcduu.streamlit.app"
}

# ==================== معلومات التواصل ====================
CONTACT_PHONE = "0767063120"
CONTACT_EMAIL = "support@ugandadigital.go.ug"

# ==================== اللغة ====================
if "language" not in st.session_state:
    st.session_state.language = "en"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==================== الترجمة الكاملة ====================
lang = {
    "en": {
        "title": "🇺🇬 Uganda Digital Platform",
        "subtitle": "Empowering Citizens | Connecting Farmers | Serving Government",
        "features": "🤖 Powered by AI Agents | 📱 Works Offline | 🌍 3 Languages",
        "who_are_you": "👤 Who are you?",
        "farmer": "👨‍🌾 Farmer",
        "government": "🏛️ Government Official",
        "citizen": "👥 Citizen",
        "admin_panel": "🔧 Admin Panel",
        "portfolio": "📁 My Portfolio",
        "back_home": "← Back to Home",
        "support": "Support",
        "dashboard": "📊 Dashboard",
        "stats": "Statistics",
        
        "farmer_services": "🌾 Farmer Services",
        "government_services": "🏛️ Government Services",
        "citizen_services": "👥 Citizen Services",
        "sell_produce": "Sell Your Produce",
        "buy_produce": "Buy Produce",
        "market_prices": "Market Prices",
        "collect_data": "Collect Field Data",
        "view_reports": "View Reports",
        "manage_complaints": "Manage Complaints",
        "report_problem": "Report a Problem",
        "track_complaint": "Track Complaint",
        
        "complaint_id": "Complaint ID",
        "status": "Status",
        "category": "Category",
        "location": "Location",
        "description": "Description",
        "submit": "Submit",
        "update": "Update",
        "search": "Search",
        
        "roads": "🚧 Roads",
        "water": "💧 Water",
        "health": "🏥 Health",
        "education": "📚 Education",
        "electricity": "⚡ Electricity",
        "waste": "🗑️ Waste",
        "security": "👮 Security",
        "other": "📌 Other",
        
        "pending": "⏳ Pending",
        "processing": "🛠️ Processing",
        "resolved": "✅ Resolved",
        "rejected": "❌ Rejected",
        
        "complaint_submitted": "Complaint submitted successfully!",
        "complaint_not_found": "Complaint not found",
        "fill_all_fields": "Please fill all fields",
        "wrong_password": "Wrong password",
        "login_success": "Logged in as Admin",
        "status_updated": "Status updated successfully",
        "open_app": "Open App",
        "launch": "Launch",
        
        "total_users": "Total Users",
        "complaints_resolved": "Complaints Resolved",
        "farmers_connected": "Farmers Connected",
        "total_products": "Total Products",
        "ai_agents": "AI Agents",
        "languages": "Languages",
        "sectors": "Sectors",
        "offline": "Offline",
        
        "submit_complaint": "✅ Submit Complaint",
        "track": "🔍 Track",
        "update_status": "Update Status",
        "admin_password": "Admin Password",
        "login": "Login"
    },
    "ar": {
        "title": "🇺🇬 منصة أوغندا الرقمية",
        "subtitle": "تمكين المواطنين | ربط المزارعين | خدمة الحكومة",
        "features": "🤖 مدعوم بوكلاء الذكاء الاصطناعي | 📱 يعمل بدون إنترنت | 🌍 3 لغات",
        "who_are_you": "👤 من أنت؟",
        "farmer": "👨‍🌾 مزارع",
        "government": "🏛️ موظف حكومي",
        "citizen": "👥 مواطن",
        "admin_panel": "🔧 لوحة المسؤول",
        "portfolio": "📁 أعمالي",
        "back_home": "← العودة للرئيسية",
        "support": "الدعم",
        "dashboard": "📊 لوحة التحكم",
        "stats": "إحصائيات",
        
        "farmer_services": "🌾 خدمات المزارعين",
        "government_services": "🏛️ خدمات الحكومة",
        "citizen_services": "👥 خدمات المواطنين",
        "sell_produce": "بيع المنتجات",
        "buy_produce": "شراء المنتجات",
        "market_prices": "أسعار السوق",
        "collect_data": "جمع البيانات الميدانية",
        "view_reports": "عرض التقارير",
        "manage_complaints": "إدارة الشكاوى",
        "report_problem": "تسجيل شكوى",
        "track_complaint": "تتبع شكوى",
        
        "complaint_id": "رقم الشكوى",
        "status": "الحالة",
        "category": "الفئة",
        "location": "الموقع",
        "description": "الوصف",
        "submit": "إرسال",
        "update": "تحديث",
        "search": "بحث",
        
        "roads": "🚧 الطرق",
        "water": "💧 المياه",
        "health": "🏥 الصحة",
        "education": "📚 التعليم",
        "electricity": "⚡ الكهرباء",
        "waste": "🗑️ النفايات",
        "security": "👮 الأمن",
        "other": "📌 أخرى",
        
        "pending": "⏳ قيد المراجعة",
        "processing": "🛠️ قيد المعالجة",
        "resolved": "✅ تم الحل",
        "rejected": "❌ مرفوضة",
        
        "complaint_submitted": "تم إرسال الشكوى بنجاح!",
        "complaint_not_found": "لم نجد الشكوى",
        "fill_all_fields": "يرجى ملء جميع الحقول",
        "wrong_password": "كلمة المرور غير صحيحة",
        "login_success": "تم الدخول كمسؤول",
        "status_updated": "تم تحديث الحالة بنجاح",
        "open_app": "فتح التطبيق",
        "launch": "تشغيل",
        
        "total_users": "إجمالي المستخدمين",
        "complaints_resolved": "الشكاوى المحلولة",
        "farmers_connected": "المزارعون المتصلون",
        "total_products": "إجمالي المنتجات",
        "ai_agents": "وكلاء ذكاء اصطناعي",
        "languages": "لغات",
        "sectors": "قطاعات",
        "offline": "بدون إنترنت",
        
        "submit_complaint": "✅ إرسال الشكوى",
        "track": "🔍 تتبع",
        "update_status": "تحديث الحالة",
        "admin_password": "كلمة المرور",
        "login": "دخول"
    },
    "sw": {
        "title": "🇺🇬 Jukwaa la Kidijitali Uganda",
        "subtitle": "Kuwawezesha Wananchi | Kuunganisha Wakulima | Kuhudumia Serikali",
        "features": "🤖 Inaendeshwa na AI Agents | 📱 Inafanya kazi Offline | 🌍 Lugha 3",
        "who_are_you": "👤 Wewe ni nani?",
        "farmer": "👨‍🌾 Mkulima",
        "government": "🏛️ Afisa Serikali",
        "citizen": "👥 Raia",
        "admin_panel": "🔧 Jopo la Msimamizi",
        "portfolio": "📁 Kazi Zangu",
        "back_home": "← Rudi Nyumbani",
        "support": "Msaada",
        "dashboard": "📊 Dashibodi",
        "stats": "Takwimu",
        
        "farmer_services": "🌾 Huduma za Wakulima",
        "government_services": "🏛️ Huduma za Serikali",
        "citizen_services": "👥 Huduma za Wananchi",
        "sell_produce": "Uza Mazao",
        "buy_produce": "Nunua Mazao",
        "market_prices": "Bei za Soko",
        "collect_data": "Kusanya Data Shambani",
        "view_reports": "Angalia Ripoti",
        "manage_complaints": "Simamia Malalamiko",
        "report_problem": "Ripoti Tatizo",
        "track_complaint": "Fuatilia Malalamiko",
        
        "complaint_id": "Namba ya Malalamiko",
        "status": "Hali",
        "category": "Aina",
        "location": "Mahali",
        "description": "Maelezo",
        "submit": "Tuma",
        "update": "Badilisha",
        "search": "Tafuta",
        
        "roads": "🚧 Barabara",
        "water": "💧 Maji",
        "health": "🏥 Afya",
        "education": "📚 Elimu",
        "electricity": "⚡ Umeme",
        "waste": "🗑️ Taka",
        "security": "👮 Usalama",
        "other": "📌 Nyingine",
        
        "pending": "⏳ Inasubiri",
        "processing": "🛠️ Inachakatwa",
        "resolved": "✅ Imetatuliwa",
        "rejected": "❌ Imekataliwa",
        
        "complaint_submitted": "Malalamiko yametumwa!",
        "complaint_not_found": "Malalamiko hayapatikani",
        "fill_all_fields": "Tafadhali jaza sehemu zote",
        "wrong_password": "Nenosiri si sahihi",
        "login_success": "Umeingia kama Msimamizi",
        "status_updated": "Hali imebadilishwa",
        "open_app": "Fungua App",
        "launch": "Zindua",
        
        "total_users": "Jumla ya Watumiaji",
        "complaints_resolved": "Malalamiko Yaliyotatuliwa",
        "farmers_connected": "Wakulima Waliounganishwa",
        "total_products": "Jumla ya Bidhaa",
        "ai_agents": "AI Agents",
        "languages": "Lugha",
        "sectors": "Sekta",
        "offline": "Offline",
        
        "submit_complaint": "✅ Tuma Malalamiko",
        "track": "🔍 Fuatilia",
        "update_status": "Badilisha Hali",
        "admin_password": "Nenosiri",
        "login": "Ingia"
    }
}

def t(key):
    return lang[st.session_state.language].get(key, key)

# ==================== ملفات البيانات ====================
DATA_FOLDER = "platform_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
COMPLAINTS_FILE = os.path.join(DATA_FOLDER, "complaints.json")
PRODUCTS_FILE = os.path.join(DATA_FOLDER, "products.json")

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except:
            return []
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def generate_id():
    return "CMP-" + str(uuid.uuid4())[:8].upper()

# تهيئة البيانات التجريبية
if not os.path.exists(USERS_FILE):
    save_data(USERS_FILE, [
        {"id": "USR-001", "name": "John Farmer", "type": "farmer", "date": "2026-03-01"},
        {"id": "USR-002", "name": "Jane Official", "type": "government", "date": "2026-03-02"},
        {"id": "USR-003", "name": "Peter Citizen", "type": "citizen", "date": "2026-03-03"},
    ])

if not os.path.exists(COMPLAINTS_FILE):
    save_data(COMPLAINTS_FILE, [
        {"id": "CMP-001", "category": "roads", "status": "resolved", "date": "2026-03-10", "location": "Kiryandongo", "description": "Bad road"},
        {"id": "CMP-002", "category": "water", "status": "processing", "date": "2026-03-15", "location": "Masindi", "description": "No clean water"},
        {"id": "CMP-003", "category": "health", "status": "pending", "date": "2026-03-18", "location": "Gulu", "description": "Clinic needs supplies"},
    ])

if not os.path.exists(PRODUCTS_FILE):
    save_data(PRODUCTS_FILE, [
        {"id": "PRD-001", "name": "Bananas", "price": 5000, "quantity": 100, "date": "2026-03-20"},
        {"id": "PRD-002", "name": "Maize", "price": 3000, "quantity": 200, "date": "2026-03-19"},
        {"id": "PRD-003", "name": "Beans", "price": 4000, "quantity": 150, "date": "2026-03-18"},
    ])

# ==================== دوال الإحصائيات ====================
def get_stats():
    users = load_data(USERS_FILE)
    complaints = load_data(COMPLAINTS_FILE)
    products = load_data(PRODUCTS_FILE)
    
    return {
        "total_users": len(users),
        "complaints_resolved": len([c for c in complaints if c.get("status") == "resolved"]),
        "farmers_connected": len([u for u in users if u.get("type") == "farmer"]),
        "total_products": len(products)
    }

# ==================== دالة عرض الرابط ====================
def open_app_link(app_name, app_url):
    st.markdown(f"""
    <div style='background: #f0f2f6; padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;'>
        <p style='font-size: 1.2rem;'>{t('open_app')}</p>
        <a href='{app_url}' target='_blank'>
            <button style='background-color: #2ecc71; color: white; padding: 0.8rem 2rem; border: none; border-radius: 10px; font-size: 1rem; cursor: pointer;'>
                🚀 {t('launch')} {app_name}
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ==================== تصميم الصفحة ====================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    .service-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .service-card:hover {
        transform: translateY(-5px);
    }
    .stats-row {
        background: #f0f2f6;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        color: #7f8c8d;
    }
</style>
""", unsafe_allow_html=True)

# ==================== أزرار اللغة ====================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🇸🇦 العربية", use_container_width=True):
        st.session_state.language = "ar"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.language = "en"
        st.rerun()
with col3:
    if st.button("🇺🇬 Kiswahili", use_container_width=True):
        st.session_state.language = "sw"
        st.rerun()

# ==================== العنوان ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('title')}</h1>
    <p>{t('subtitle')}</p>
    <p style='font-size: 0.9rem;'>{t('features')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== إحصائيات سريعة ====================
stats = get_stats()

st.markdown(f"""
<div class='stats-row'>
    <div style='display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap;'>
        <div><h2>{stats['total_users']}</h2><p>{t('total_users')}</p></div>
        <div><h2>{stats['complaints_resolved']}</h2><p>{t('complaints_resolved')}</p></div>
        <div><h2>{stats['farmers_connected']}</h2><p>{t('farmers_connected')}</p></div>
        <div><h2>{stats['total_products']}</h2><p>{t('total_products')}</p></div>
        <div><h2>4</h2><p>{t('ai_agents')}</p></div>
        <div><h2>3</h2><p>{t('languages')}</p></div>
        <div><h2>6</h2><p>{t('sectors')}</p></div>
        <div><h2>∞</h2><p>{t('offline')}</p></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== الصفحة الرئيسية ====================
if st.session_state.page == "home":
    st.markdown(f"### {t('who_are_you')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(t('farmer'), use_container_width=True):
            st.session_state.page = "farmer"
            st.rerun()
    with col2:
        if st.button(t('government'), use_container_width=True):
            st.session_state.page = "government"
            st.rerun()
    with col3:
        if st.button(t('citizen'), use_container_width=True):
            st.session_state.page = "citizen"
            st.rerun()
    with col4:
        if st.button(t('portfolio'), use_container_width=True):
            st.session_state.page = "portfolio"
            st.rerun()
    
    if st.button(t('admin_panel'), use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

# ==================== صفحة المزارع ====================
elif st.session_state.page == "farmer":
    st.markdown(f"## {t('farmer_services')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='service-card'>
            <div class='service-icon'>🌽</div>
            <h3>SOKO LINK</h3>
            <p>{t('sell_produce')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        open_app_link("SOKO LINK", APP_LINKS["soko_link"])
    
    with col2:
        st.markdown(f"""
        <div class='service-card'>
            <div class='service-icon'>📊</div>
            <h3>{t('market_prices')}</h3>
            <p>{t('buy_produce')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        products = load_data(PRODUCTS_FILE)
        if products:
            for p in products[-3:]:
                st.write(f"🍌 {p['name']}: {p['price']:,} UGX / kg")

# ==================== صفحة الحكومة ====================
elif st.session_state.page == "government":
    st.markdown(f"## {t('government_services')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='service-card'>
            <div class='service-icon'>📊</div>
            <h3>DataCollect UG</h3>
            <p>{t('collect_data')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        open_app_link("DataCollect UG", APP_LINKS["datacollect"])
    
    with col2:
        st.markdown(f"""
        <div class='service-card'>
            <div class='service-icon'>🤖</div>
            <h3>GovFeedback AI Agent</h3>
            <p>{t('manage_complaints')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        open_app_link("GovFeedback AI Agent", APP_LINKS["govfeedback"])

# ==================== صفحة المواطن ====================
elif st.session_state.page == "citizen":
    st.markdown(f"## {t('citizen_services')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    tab1, tab2 = st.tabs([t('report_problem'), t('track_complaint')])
    
    with tab1:
        category_options = [t('roads'), t('water'), t('health'), t('education'), t('electricity'), t('waste'), t('security'), t('other')]
        category = st.selectbox(t('category'), category_options)
        location = st.text_input(t('location'))
        description = st.text_area(t('description'))
        
        if st.button(t('submit_complaint'), use_container_width=True):
            if location and description:
                complaint = {
                    "id": generate_id(),
                    "category": category,
                    "location": location,
                    "description": description,
                    "status": "pending",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                complaints = load_data(COMPLAINTS_FILE)
                complaints.append(complaint)
                save_data(COMPLAINTS_FILE, complaints)
                st.success(f"✅ {t('complaint_submitted')} ID: {complaint['id']}")
                st.balloons()
            else:
                st.error(f"❌ {t('fill_all_fields')}")
    
    with tab2:
        complaint_id = st.text_input(t('complaint_id'), placeholder="CMP-XXXXXXXX")
        
        if st.button(t('track'), use_container_width=True):
            if complaint_id:
                complaints = load_data(COMPLAINTS_FILE)
                found = None
                for c in complaints:
                    if c["id"] == complaint_id.upper():
                        found = c
                        break
                
                if found:
                    st.markdown(f"""
                    <div style='background: #f0f2f6; padding: 1rem; border-radius: 10px;'>
                        <h3>{t('complaint_id')}: {found['id']}</h3>
                        <p><strong>{t('category')}:</strong> {found['category']}</p>
                        <p><strong>{t('location')}:</strong> {found['location']}</p>
                        <p><strong>{t('description')}:</strong> {found['description']}</p>
                        <p><strong>{t('status')}:</strong> {t(found['status'])}</p>
                        <p><strong>{t('date')}:</strong> {found['date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ {t('complaint_not_found')}")

# ==================== صفحة البورتفوليو ====================
elif st.session_state.page == "portfolio":
    st.markdown(f"## 📁 {t('portfolio')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    open_app_link("My Portfolio", APP_LINKS["portfolio"])

# ==================== لوحة المسؤول ====================
elif st.session_state.page == "admin":
    st.markdown(f"## {t('admin_panel')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    password = st.text_input(t('admin_password'), type="password")
    
    if password == "admin123":
        st.session_state.admin_logged_in = True
    elif password:
        st.error(f"❌ {t('wrong_password')}")
    
    if st.session_state.admin_logged_in:
        st.success(f"✅ {t('login_success')}")
        
        st.markdown(f"### {t('dashboard')}")
        stats = get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t('total_users'), stats['total_users'])
        with col2:
            st.metric(t('complaints_resolved'), stats['complaints_resolved'])
        with col3:
            st.metric(t('farmers_connected'), stats['farmers_connected'])
        with col4:
            st.metric(t('total_products'), stats['total_products'])
        
        st.markdown("---")
        st.subheader("👥 Users")
        users = load_data(USERS_FILE)
        if users:
            df = pd.DataFrame(users)
            st.dataframe(df, use_container_width=True)
        
        st.subheader("📋 Complaints")
        complaints = load_data(COMPLAINTS_FILE)
        if complaints:
            df = pd.DataFrame(complaints)
            st.dataframe(df, use_container_width=True)
            
            st.subheader(t('update_status'))
            complaint_id = st.text_input(t('complaint_id'))
            status_options = ["pending", "processing", "resolved", "rejected"]
            new_status = st.selectbox(t('status'), status_options, format_func=lambda x: t(x))
            
            if st.button(t('update_status'), use_container_width=True):
                for c in complaints:
                    if c["id"] == complaint_id.upper():
                        c["status"] = new_status
                        save_data(COMPLAINTS_FILE, complaints)
                        st.success(f"✅ {t('status_updated')}")
                        st.rerun()
                st.error(f"❌ {t('complaint_not_found')}")

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### {t('title')}")
    st.markdown(f"**Version:** 2.0")
    st.markdown(f"**{t('ai_agents')}:** 4 Active")
    st.markdown(f"**{t('languages')}:** English, Swahili, Arabic")
    st.markdown("---")
    st.markdown(f"### 📊 {t('dashboard')}")
    
    stats = get_stats()
    st.metric(t('total_users'), stats['total_users'])
    st.metric(t('complaints_resolved'), stats['complaints_resolved'])
    st.metric(t('farmers_connected'), stats['farmers_connected'])
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown(f"[🌽 SOKO LINK]({APP_LINKS['soko_link']})")
    st.markdown(f"[📊 DataCollect UG]({APP_LINKS['datacollect']})")
    st.markdown(f"[🤖 GovFeedback AI]({APP_LINKS['govfeedback']})")
    st.markdown(f"[📁 My Portfolio]({APP_LINKS['portfolio']})")
    
    st.markdown("---")
    st.markdown(f"### 📞 {t('support')}")
    st.markdown(f"📞 {CONTACT_PHONE}")
    st.markdown(f"📧 {CONTACT_EMAIL}")

# ==================== تذييل ====================
st.markdown(f"""
<div class='footer'>
    <p>{t('title')} | {t('subtitle')}</p>
    <p>{t('features')}</p>
    <p>📞 {CONTACT_PHONE} | 📧 {CONTACT_EMAIL}</p>
</div>
""", unsafe_allow_html=True)
