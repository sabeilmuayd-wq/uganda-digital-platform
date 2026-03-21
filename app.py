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

# ==================== اللغة ====================
if "language" not in st.session_state:
    st.session_state.language = "en"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "🇺🇬 Uganda Digital Platform",
        "subtitle": "Empowering Citizens | Connecting Farmers | Serving Government",
        "features": "🤖 Powered by AI Agents | 📱 Works Offline | 🌍 3 Languages",
        "who_are_you": "👤 Who are you?",
        "farmer": "👨‍🌾 Farmer",
        "government": "🏛️ Government Official",
        "citizen": "👥 Citizen",
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
        "admin_panel": "🔧 Admin Panel",
        "dashboard": "📊 Dashboard",
        "total_users": "Total Users",
        "complaints_resolved": "Complaints Resolved",
        "farmers_connected": "Farmers Connected",
        "total_products": "Total Products",
        "ai_agents": "AI Agents",
        "languages": "Languages",
        "sectors": "Sectors",
        "offline": "Offline",
        "support": "Support",
        "back_home": "← Back to Home"
    },
    "ar": {
        "title": "🇺🇬 منصة أوغندا الرقمية",
        "subtitle": "تمكين المواطنين | ربط المزارعين | خدمة الحكومة",
        "features": "🤖 مدعوم بوكلاء الذكاء الاصطناعي | 📱 يعمل بدون إنترنت | 🌍 3 لغات",
        "who_are_you": "👤 من أنت؟",
        "farmer": "👨‍🌾 مزارع",
        "government": "🏛️ موظف حكومي",
        "citizen": "👥 مواطن",
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
        "admin_panel": "🔧 لوحة المسؤول",
        "dashboard": "📊 لوحة التحكم",
        "total_users": "إجمالي المستخدمين",
        "complaints_resolved": "الشكاوى المحلولة",
        "farmers_connected": "المزارعون المتصلون",
        "total_products": "إجمالي المنتجات",
        "ai_agents": "وكلاء ذكاء اصطناعي",
        "languages": "لغات",
        "sectors": "قطاعات",
        "offline": "بدون إنترنت",
        "support": "الدعم",
        "back_home": "← العودة للرئيسية"
    },
    "sw": {
        "title": "🇺🇬 Jukwaa la Kidijitali Uganda",
        "subtitle": "Kuwawezesha Wananchi | Kuunganisha Wakulima | Kuhudumia Serikali",
        "features": "🤖 Inaendeshwa na AI Agents | 📱 Inafanya kazi Offline | 🌍 Lugha 3",
        "who_are_you": "👤 Wewe ni nani?",
        "farmer": "👨‍🌾 Mkulima",
        "government": "🏛️ Afisa Serikali",
        "citizen": "👥 Raia",
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
        "admin_panel": "🔧 Jopo la Msimamizi",
        "dashboard": "📊 Dashibodi",
        "total_users": "Jumla ya Watumiaji",
        "complaints_resolved": "Malalamiko Yaliyotatuliwa",
        "farmers_connected": "Wakulima Waliounganishwa",
        "total_products": "Jumla ya Bidhaa",
        "ai_agents": "AI Agents",
        "languages": "Lugha",
        "sectors": "Sekta",
        "offline": "Offline",
        "support": "Msaada",
        "back_home": "← Rudi Nyumbani"
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
    return str(uuid.uuid4())[:8].upper()

# تهيئة البيانات التجريبية
if not os.path.exists(USERS_FILE):
    save_data(USERS_FILE, [
        {"id": "USR-001", "name": "John Farmer", "type": "farmer", "date": "2026-03-01"},
        {"id": "USR-002", "name": "Jane Official", "type": "government", "date": "2026-03-02"},
        {"id": "USR-003", "name": "Peter Citizen", "type": "citizen", "date": "2026-03-03"},
    ])

if not os.path.exists(COMPLAINTS_FILE):
    save_data(COMPLAINTS_FILE, [
        {"id": "CMP-001", "category": "roads", "status": "resolved", "date": "2026-03-10"},
        {"id": "CMP-002", "category": "water", "status": "processing", "date": "2026-03-15"},
        {"id": "CMP-003", "category": "health", "status": "pending", "date": "2026-03-18"},
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
        cursor: pointer;
    }
    .service-card:hover {
        transform: translateY(-5px);
    }
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border-top: 4px solid #2ecc71;
    }
    .stats-row {
        background: #f0f2f6;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .admin-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #e67e22;
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
    
    col1, col2, col3 = st.columns(3)
    
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
    
    # زر لوحة المسؤول
    if st.button("🔧 Admin Panel", use_container_width=True):
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
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🌽</div>
            <h3>SOKO LINK</h3>
            <p>Sell your produce directly to buyers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open SOKO LINK →", key="soko", use_container_width=True):
            st.info("🔗 SOKO LINK is available at: [your-soko-link.streamlit.app]")
    
    with col2:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>📊</div>
            <h3>Market Prices</h3>
            <p>Check current market prices for your crops</p>
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
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>📊</div>
            <h3>DataCollect UG</h3>
            <p>Collect field data from farmers and health workers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open DataCollect UG →", key="datacollect", use_container_width=True):
            st.info("🔗 DataCollect UG is available at: [your-datacollect.streamlit.app]")
    
    with col2:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>📈</div>
            <h3>Analytics Dashboard</h3>
            <p>View reports and statistics</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Total Complaints", len(load_data(COMPLAINTS_FILE)))
        st.metric("Total Farmers", len([u for u in load_data(USERS_FILE) if u.get("type") == "farmer"]))

# ==================== صفحة المواطن ====================
elif st.session_state.page == "citizen":
    st.markdown(f"## {t('citizen_services')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🤖</div>
            <h3>Report a Problem</h3>
            <p>Submit complaints to the government</p>
        </div>
        """, unsafe_allow_html=True)
        
        category = st.selectbox("Category", ["Roads", "Water", "Health", "Education", "Electricity"])
        location = st.text_input("Location")
        description = st.text_area("Description")
        
        if st.button("Submit Complaint", use_container_width=True):
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
                st.success(f"✅ Complaint submitted! ID: {complaint['id']}")
                st.balloons()
            else:
                st.error("Please fill all fields")
    
    with col2:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🔍</div>
            <h3>Track Complaint</h3>
            <p>Check the status of your complaint</p>
        </div>
        """, unsafe_allow_html=True)
        
        complaint_id = st.text_input(t('complaint_id'), placeholder="CMP-XXXXXXXX")
        if complaint_id:
            complaints = load_data(COMPLAINTS_FILE)
            found = None
            for c in complaints:
                if c["id"] == complaint_id.upper():
                    found = c
                    break
            
            if found:
                status_text = found["status"]
                st.info(f"""
                **ID:** {found['id']}
                **Category:** {found['category']}
                **Location:** {found['location']}
                **Description:** {found['description']}
                **Status:** {status_text}
                **Date:** {found['date']}
                """)
            else:
                st.error("Complaint not found")

# ==================== لوحة المسؤول ====================
elif st.session_state.page == "admin":
    st.markdown(f"## {t('admin_panel')}")
    
    if st.button(t('back_home'), use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    password = st.text_input("Admin Password", type="password")
    
    if password == "admin123":
        st.session_state.admin_logged_in = True
    elif password:
        st.error("Wrong password")
    
    if st.session_state.admin_logged_in:
        st.success("✅ Logged in as Admin")
        
        # Dashboard
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
        
        # Users
        st.markdown("---")
        st.subheader("👥 Users")
        users = load_data(USERS_FILE)
        if users:
            df = pd.DataFrame(users)
            st.dataframe(df, use_container_width=True)
        
        # Complaints
        st.subheader("📋 Complaints")
        complaints = load_data(COMPLAINTS_FILE)
        if complaints:
            df = pd.DataFrame(complaints)
            st.dataframe(df, use_container_width=True)
            
            # Update status
            st.subheader("Update Complaint Status")
            complaint_id = st.text_input("Complaint ID to update")
            new_status = st.selectbox("New Status", ["pending", "processing", "resolved", "rejected"])
            
            if st.button("Update Status"):
                for c in complaints:
                    if c["id"] == complaint_id.upper():
                        c["status"] = new_status
                        save_data(COMPLAINTS_FILE, complaints)
                        st.success(f"✅ Complaint {complaint_id} updated to {new_status}")
                        st.rerun()
                st.error("Complaint not found")
        
        # Products
        st.subheader("🌽 Products")
        products = load_data(PRODUCTS_FILE)
        if products:
            df = pd.DataFrame(products)
            st.dataframe(df, use_container_width=True)

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### {t('title')}")
    st.markdown(f"**Version:** 1.0")
    st.markdown(f"**{t('ai_agents')}:** 4 Active")
    st.markdown(f"**{t('languages')}:** English, Swahili, Arabic")
    st.markdown("---")
    st.markdown(f"### 📊 {t('dashboard')}")
    
    stats = get_stats()
    st.metric(t('total_users'), stats['total_users'])
    st.metric(t('complaints_resolved'), stats['complaints_resolved'])
    st.metric(t('farmers_connected'), stats['farmers_connected'])
    
    st.markdown("---")
    st.markdown(f"### 📞 {t('support')}")
    st.markdown("📞 0800-200-900")
    st.markdown("📧 support@ugandadigital.go.ug")

# ==================== تذييل ====================
st.markdown(f"""
<div class='footer'>
    <p>{t('title')} | {t('subtitle')}</p>
    <p>{t('features')}</p>
</div>
""", unsafe_allow_html=True)
