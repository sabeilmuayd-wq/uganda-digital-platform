import streamlit as st

st.set_page_config(
    page_title="Uganda Digital Platform",
    page_icon="🇺🇬",
    layout="wide"
)

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
    }
    .service-icon {
        font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-header'>
    <h1>🇺🇬 Uganda Digital Platform</h1>
    <p>Empowering Citizens | Connecting Farmers | Serving Government</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Choose a Service")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='service-card'>
        <div class='service-icon'>🌽</div>
        <h3>SOKO LINK</h3>
        <p>Farmers Market</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open SOKO LINK →", key="soko"):
        st.switch_page("pages/soko_link.py")

with col2:
    st.markdown("""
    <div class='service-card'>
        <div class='service-icon'>📊</div>
        <h3>DataCollect UG</h3>
        <p>Government Data</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open DataCollect UG →", key="datacollect"):
        st.switch_page("pages/datacollect.py")

with col3:
    st.markdown("""
    <div class='service-card'>
        <div class='service-icon'>🤖</div>
        <h3>GovFeedback AI</h3>
        <p>Citizen Complaints</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open GovFeedback →", key="govfeedback"):
        st.switch_page("pages/govfeedback.py")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Powered by AI Agents | 3 Languages | Offline Support</p>", unsafe_allow_html=True)
