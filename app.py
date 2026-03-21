import streamlit as st

st.set_page_config(
    page_title="Uganda Digital Platform",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== التصميم ====================
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
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .service-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .stats-row {
        background: #f0f2f6;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان ====================
st.markdown("""
<div class='main-header'>
    <h1>🇺🇬 Uganda Digital Platform</h1>
    <p>Empowering Citizens | Connecting Farmers | Serving Government</p>
    <p style='font-size: 0.9rem;'>🤖 Powered by AI Agents | 📱 Works Offline | 🌍 3 Languages</p>
</div>
""", unsafe_allow_html=True)

# ==================== إحصائيات سريعة ====================
st.markdown("""
<div class='stats-row'>
    <div style='display: flex; justify-content: space-around; text-align: center;'>
        <div>
            <h2>4</h2>
            <p>AI Agents</p>
        </div>
        <div>
            <h2>3</h2>
            <p>Languages</p>
        </div>
        <div>
            <h2>6</h2>
            <p>Sectors</p>
        </div>
        <div>
            <h2>∞</h2>
            <p>Offline</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== اختيار المستخدم ====================
st.subheader("👤 Who are you?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👨‍🌾 Farmer", use_container_width=True):
        st.session_state.selected_service = "farmer"
        st.rerun()
with col2:
    if st.button("🏛️ Government Official", use_container_width=True):
        st.session_state.selected_service = "government"
        st.rerun()
with col3:
    if st.button("👥 Citizen", use_container_width=True):
        st.session_state.selected_service = "citizen"
        st.rerun()

# ==================== خدمات المزارع ====================
if st.session_state.get("selected_service") == "farmer":
    st.markdown("---")
    st.subheader("🌾 Farmer Services")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🌽</div>
            <h3>SOKO LINK</h3>
            <p>Sell your produce directly to buyers</p>
            <p>✅ Post products with photos</p>
            <p>✅ Get fair prices</p>
            <p>✅ No middlemen</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to SOKO LINK →", key="soko", use_container_width=True):
            st.markdown("[Open SOKO LINK](https://your-soko-link.streamlit.app)")
    
    with col2:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>📊</div>
            <h3>DataCollect UG</h3>
            <p>Register your farm data for government support</p>
            <p>✅ Get extension services</p>
            <p>✅ Access subsidies</p>
            <p>✅ Connect with buyers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to DataCollect UG →", key="datacollect", use_container_width=True):
            st.markdown("[Open DataCollect UG](https://your-datacollect.streamlit.app)")

# ==================== خدمات الحكومة ====================
elif st.session_state.get("selected_service") == "government":
    st.markdown("---")
    st.subheader("🏛️ Government Services")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>📊</div>
            <h3>DataCollect UG</h3>
            <p>Collect field data from farmers and health workers</p>
            <p>✅ Offline collection</p>
            <p>✅ Real-time sync</p>
            <p>✅ Export reports</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to DataCollect UG →", key="gov_data", use_container_width=True):
            st.markdown("[Open DataCollect UG](https://your-datacollect.streamlit.app)")
    
    with col2:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🤖</div>
            <h3>GovFeedback AI Agent</h3>
            <p>AI-powered citizen complaints management</p>
            <p>✅ Auto-classification</p>
            <p>✅ Smart routing</p>
            <p>✅ WhatsApp notifications</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to GovFeedback →", key="gov_feedback", use_container_width=True):
            st.markdown("[Open GovFeedback AI Agent](https://your-govfeedback.streamlit.app)")

# ==================== خدمات المواطن ====================
elif st.session_state.get("selected_service") == "citizen":
    st.markdown("---")
    st.subheader("👥 Citizen Services")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🤖</div>
            <h3>Report a Problem</h3>
            <p>Submit complaints to the government</p>
            <p>✅ Add photo and location</p>
            <p>✅ Track your complaint</p>
            <p>✅ Get WhatsApp updates</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Report Now →", key="report", use_container_width=True):
            st.markdown("[Open GovFeedback AI Agent](https://your-govfeedback.streamlit.app)")
    
    with col2:
        st.markdown("""
        <div class='service-card'>
            <div class='service-icon'>🔍</div>
            <h3>Track Complaint</h3>
            <p>Check the status of your complaint</p>
            <p>✅ Enter your complaint ID</p>
            <p>✅ See current status</p>
            <p>✅ Get updates</p>
        </div>
        """, unsafe_allow_html=True)
        
        complaint_id = st.text_input("Enter Complaint ID", placeholder="CMP-XXXXXXXX")
        if complaint_id:
            st.info(f"Tracking complaint: {complaint_id}")

# ==================== شريط جانبي ====================
with st.sidebar:
    st.markdown("### 🇺🇬 Uganda Digital Platform")
    st.markdown("**Version:** 1.0")
    st.markdown("**AI Agents:** 4 Active")
    st.markdown("**Languages:** English, Swahili, Arabic")
    st.markdown("---")
    st.markdown("### 📊 Platform Stats")
    st.metric("Total Users", "1,234+")
    st.metric("Complaints Resolved", "456")
    st.metric("Farmers Connected", "789")
    st.markdown("---")
    st.markdown("### 📞 Support")
    st.markdown("📞 0800-200-900")
    st.markdown("📧 support@ugandadigital.go.ug")

# ==================== تذييل ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #7f8c8d;'>
    <p>🇺🇬 Uganda Digital Platform | Empowering Citizens | Connecting Farmers | Serving Government 🇺🇬</p>
    <p>Built with ❤️ for Uganda | Powered by AI Agents</p>
</div>
""", unsafe_allow_html=True)
