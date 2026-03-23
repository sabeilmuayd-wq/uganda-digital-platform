import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="Uganda Digital Platform - UCSATP",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== إعداد المقاطعات التجريبية ====================
if "district" not in st.session_state:
    st.session_state.district = "Kiryandongo"

PILOT_DISTRICTS = ["Kiryandongo", "Masindi", "Gulu"]

# ==================== ملفات التخزين ====================
DATA_FOLDER = "ucsatp_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

FARMERS_FILE = os.path.join(DATA_FOLDER, "farmers.json")
CROPS_FILE = os.path.join(DATA_FOLDER, "crops.json")

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

# ==================== تصميم الصفحة ====================
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# ==================== الشريط الجانبي (اختيار المقاطعة والإحصائيات) ====================
with st.sidebar:
    st.markdown("### 📍 UCSATP Pilot")
    st.markdown("**Ministry of Agriculture**")
    
    selected_district = st.radio(
        "Select Pilot District:",
        PILOT_DISTRICTS,
        index=PILOT_DISTRICTS.index(st.session_state.district)
    )
    if selected_district != st.session_state.district:
        st.session_state.district = selected_district
        st.rerun()
    
    st.markdown(f"**Active:** `{st.session_state.district}`")
    
    st.markdown("---")
    st.markdown("### 📊 Pilot Statistics")
    
    farmers = load_data(FARMERS_FILE)
    district_farmers = [f for f in farmers if f.get("district") == st.session_state.district]
    st.metric("Farmers Registered", len(district_farmers))
    
    crops = load_data(CROPS_FILE)
    district_crops = [c for c in crops if c.get("district") == st.session_state.district]
    st.metric("Crops Listed", len(district_crops))
    
    total_quantity = sum([c.get("quantity", 0) for c in district_crops])
    st.metric("Total Quantity (kg)", f"{total_quantity:,}")
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("📧 procurement.ucsatp@agriculture.go.ug")
    st.markdown("📞 0774373737")

# ==================== العنوان الرئيسي ====================
st.markdown(f"""
<div class='main-header'>
    <h1>🇺🇬 Uganda Digital Platform</h1>
    <p>UCSATP - Ministry of Agriculture, Animal Industry and Fisheries</p>
    <div>
        <span class='pilot-badge'>🚀 PILOT PHASE</span>
        <span class='pilot-badge' style='background: #2ecc71;'>📍 {st.session_state.district}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== تبويبات التطبيق ====================
tab1, tab2, tab3, tab4 = st.tabs(["👨‍🌾 Register Farmer", "🌾 Add Crop", "📋 View Data", "📊 Ministry Reports"])

# ==================== TAB 1: تسجيل مزارع جديد ====================
with tab1:
    st.subheader(f"Register New Farmer - {st.session_state.district}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nin = st.text_input("National ID (NIN) *", help="Required for government records")
        full_name = st.text_input("Full Name *")
        phone = st.text_input("Phone Number")
        
    with col2:
        village = st.text_input("Village / Parish *")
        sub_county = st.text_input("Sub-county")
        farmer_type = st.selectbox("Farmer Type", ["Smallholder", "Commercial", "Cooperative Member"])
    
    if st.button("✅ Register Farmer", type="primary", use_container_width=True):
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
                "status": "active"
            }
            farmers = load_data(FARMERS_FILE)
            farmers.append(farmer)
            save_data(FARMERS_FILE, farmers)
            st.success(f"✅ Farmer {full_name} registered successfully in {st.session_state.district}!")
            st.balloons()
        else:
            st.warning("⚠️ Please fill all required fields (*)")

# ==================== TAB 2: إضافة محصول ====================
with tab2:
    st.subheader(f"Add Crop / Produce - {st.session_state.district}")
    
    farmers = load_data(FARMERS_FILE)
    district_farmers = [f for f in farmers if f.get("district") == st.session_state.district]
    
    if district_farmers:
        farmer_names = [f"{f['name']} ({f['nin']})" for f in district_farmers]
        selected_farmer = st.selectbox("Select Farmer", farmer_names)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop_type = st.selectbox("Crop Type", ["Bananas", "Maize", "Beans", "Cassava", "Coffee", "Sweet Potatoes", "Other"])
            if crop_type == "Other":
                crop_type = st.text_input("Specify crop")
        
        with col2:
            quantity = st.number_input("Quantity (kg)", min_value=1, step=10, value=100)
            unit = st.selectbox("Unit", ["kg", "tonnes", "bunches"])
        
        with col3:
            price = st.number_input("Expected Price (UGX/unit)", min_value=100, step=500, value=2000)
            harvest_date = st.date_input("Harvest Date", datetime.now())
        
        quality = st.select_slider("Quality Grade", options=["Low", "Medium", "High", "Premium"])
        notes = st.text_area("Additional Notes", placeholder="Any special information about the produce...")
        
        if st.button("🌾 Add Crop Listing", type="primary", use_container_width=True):
            if selected_farmer and crop_type and quantity:
                farmer_id = [f for f in district_farmers if f"{f['name']} ({f['nin']})" == selected_farmer][0]["id"]
                crop = {
                    "id": str(uuid.uuid4())[:8],
                    "farmer_id": farmer_id,
                    "farmer_name": selected_farmer.split(" (")[0],
                    "crop": crop_type,
                    "quantity": quantity,
                    "unit": unit,
                    "price": price,
                    "quality": quality,
                    "notes": notes,
                    "harvest_date": harvest_date.isoformat(),
                    "district": st.session_state.district,
                    "date_listed": datetime.now().isoformat(),
                    "status": "available"
                }
                crops = load_data(CROPS_FILE)
                crops.append(crop)
                save_data(CROPS_FILE, crops)
                st.success(f"✅ {crop_type} added for {selected_farmer.split(' (')[0]}!")
                st.balloons()
            else:
                st.warning("⚠️ Please fill all required fields")
    else:
        st.warning(f"⚠️ No farmers registered in {st.session_state.district} yet. Please register a farmer first.")

# ==================== TAB 3: عرض البيانات ====================
with tab3:
    st.subheader(f"Farmers & Crops - {st.session_state.district}")
    
    farmers = load_data(FARMERS_FILE)
    district_farmers = [f for f in farmers if f.get("district") == st.session_state.district]
    
    if district_farmers:
        st.markdown("### 👨‍🌾 Registered Farmers")
        for f in district_farmers:
            st.markdown(f"""
            <div class='farmer-card'>
                <strong>{f['name']}</strong> (NIN: {f['nin']})<br>
                📍 {f['village']}, {f.get('sub_county', 'N/A')}<br>
                📞 {f.get('phone', 'N/A')} | 📅 {f['registration_date'][:10]}
            </div>
            """, unsafe_allow_html=True)
    
    crops = load_data(CROPS_FILE)
    district_crops = [c for c in crops if c.get("district") == st.session_state.district]
    
    if district_crops:
        st.markdown("### 🌾 Available Crops")
        for c in district_crops:
            quality_color = {"Premium": "🟢", "High": "🟡", "Medium": "🟠", "Low": "🔴"}.get(c.get("quality"), "⚪")
            st.markdown(f"""
            <div class='farmer-card'>
                <strong>{c['crop']}</strong> {quality_color}<br>
                📦 {c['quantity']} {c['unit']} | 💰 {c['price']:,} UGX/{c['unit']}<br>
                👨‍🌾 {c['farmer_name']} | 📅 {c['harvest_date'][:10]}
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 4: تقارير للوزارة ====================
with tab4:
    st.subheader("📊 UCSATP Ministry Reports")
    
    farmers = load_data(FARMERS_FILE)
    crops = load_data(CROPS_FILE)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_farmers = len([f for f in farmers if f.get("district") in PILOT_DISTRICTS])
        st.metric("Total Farmers (All Pilots)", total_farmers)
    
    with col2:
        total_crops = len([c for c in crops if c.get("district") in PILOT_DISTRICTS])
        st.metric("Total Crop Listings", total_crops)
    
    with col3:
        total_quantity = sum([c.get("quantity", 0) for c in crops if c.get("district") in PILOT_DISTRICTS])
        st.metric("Total Quantity (kg)", f"{total_quantity:,}")
    
    st.markdown("---")
    st.markdown("### 📋 Summary by District")
    
    summary_data = []
    for d in PILOT_DISTRICTS:
        district_farmers = len([f for f in farmers if f.get("district") == d])
        district_crops = len([c for c in crops if c.get("district") == d])
        district_quantity = sum([c.get("quantity", 0) for c in crops if c.get("district") == d])
        summary_data.append({"District": d, "Farmers": district_farmers, "Crops": district_crops, "Quantity (kg)": district_quantity})
    
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📄 Export Report")
    
    if st.button("📥 Download CSV Report", use_container_width=True):
        df = pd.DataFrame(summary_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download",
            data=csv,
            file_name=f"ucsatp_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    st.markdown("### ℹ️ About This Platform")
    st.markdown("""
    **Uganda Digital Platform – UCSATP Pilot**
    
    This platform is developed to support the Uganda Climate Smart Agricultural Transformation Project (UCSATP).
    
    **Pilot Districts:** Kiryandongo, Masindi, Gulu
    
    **Features:**
    - Farmer registration with National ID (NIN)
    - Crop listing and market access
    - Real-time data collection
    - Ministry reporting dashboard
    - Works offline (data stored locally)
    
    **Contact:** procurement.ucsatp@agriculture.go.ug | 0774373737
    """)
