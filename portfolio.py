import streamlit as st

st.set_page_config(
    page_title="My Portfolio | Software Developer",
    page_icon="🚀",
    layout="wide"
)

# ==================== العنوان ====================
st.markdown("""
<h1 style='text-align: center; color: #2c3e50;'>🚀 My Portfolio</h1>
<h3 style='text-align: center; color: #7f8c8d;'>Python Developer | Streamlit Expert | AI Agent Builder</h3>
<p style='text-align: center;'>📍 Uganda | 🌍 3 Languages | 📱 Mobile-first</p>
<hr>
""", unsafe_allow_html=True)

# ==================== معلومات عني ====================
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style='background: #f0f2f6; padding: 1rem; border-radius: 10px;'>
        <h3>📞 Contact</h3>
        <p>📍 Kiryandongo, Uganda</p>
        <p>📧 your-email@example.com</p>
        <p>📱 +256 77XXXXXXX</p>
        <p>🔗 <a href="https://github.com/yourusername">GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### 👋 About Me
    
    I am a self-taught software developer based in Uganda. I build mobile and web applications using **Python** and **Streamlit**.
    
    **What makes me different:**
    - ✅ I build apps that work **offline** (no internet needed)
    - ✅ I support **3 languages** (English, Swahili, Arabic)
    - ✅ I work **from my phone** (no laptop required)
    - ✅ I build **AI agents** that automate work
    
    **Skills:** Python, Streamlit, Pandas, Plotly, AI Agents, Mobile Development
    """)

st.markdown("---")

# ==================== المشاريع ====================
st.subheader("📁 My Projects")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌽 SOKO LINK
    *Farmers Market Platform*
    
    - Connects farmers directly to buyers
    - Works offline, 3 languages
    - Live price comparison
    - Used by farmers in Kiryandongo
    
    **Tech:** Python, Streamlit, Pandas
    """)
    
    if st.button("🔗 View Project", key="soko"):
        st.info("🔗 Link: https://soko-link-yourname.streamlit.app")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🤖 GovFeedback AI Agent
    *AI-Powered Complaints System*
    
    - 4 AI agents working together
    - Auto-classification and routing
    - WhatsApp notifications
    - Used by local government
    
    **Tech:** Python, Streamlit, AI Agents
    """)
    
    if st.button("🔗 View Project", key="gov"):
        st.info("🔗 Link: https://govfeedback-ai-agent-yourname.streamlit.app")

with col2:
    st.markdown("""
    ### 📊 DataCollect UG
    *Government Data Collection*
    
    - Field data for agriculture and health
    - Data Protection Act 2019 compliant
    - Offline-first design
    - Ready for NIFAMIS integration
    
    **Tech:** Python, Streamlit, Pandas, Plotly
    """)
    
    if st.button("🔗 View Project", key="data"):
        st.info("🔗 Link: https://datacollect-ug-yourname.streamlit.app")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🇺🇬 Uganda Digital Platform
    *Unified Digital Platform*
    
    - Combines all services in one place
    - 3 user types: Farmer, Government, Citizen
    - Admin dashboard
    - Real-time statistics
    
    **Tech:** Python, Streamlit, Multi-page app
    """)
    
    if st.button("🔗 View Project", key="platform"):
        st.info("🔗 Link: https://uganda-digital-platform-yourname.streamlit.app")

st.markdown("---")

# ==================== المهارات ====================
st.subheader("💡 Skills & Technologies")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Languages**\n- Python\n- SQL\n- HTML/CSS")
with col2:
    st.markdown("**Frameworks**\n- Streamlit\n- Pandas\n- Plotly")
with col3:
    st.markdown("**Tools**\n- Git/GitHub\n- Replit\n- VS Code")
with col4:
    st.markdown("**Special**\n- AI Agents\n- Offline Apps\n- 3 Languages")

st.markdown("---")

# ==================== الشهادات والإنجازات ====================
st.subheader("🏆 Achievements")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("✅ **4 Live Applications**\nBuilt and deployed")

with col2:
    st.markdown("✅ **AI Agent Developer**\n4 agents working together")

with col3:
    st.markdown("✅ **Government Ready**\nApps compliant with Uganda Data Protection Act")

st.markdown("---")

# ==================== تواصل معي ====================
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f0f2f6; border-radius: 10px;'>
    <h3>📫 Let's Work Together</h3>
    <p>I am available for remote work, government projects, and AI agent development.</p>
    <p><strong>Email:</strong> your-email@example.com | <strong>Phone:</strong> +256 77XXXXXXX</p>
</div>
""", unsafe_allow_html=True)

# ==================== تذييل ====================
st.markdown("""
<hr>
<p style='text-align: center; color: #7f8c8d;'>
    © 2026 | Built with ❤️ using Streamlit | Uganda
</p>
""", unsafe_allow_html=True)
