import streamlit as st
from src.config import validate_config
from src.styles import inject_css, render_toc_item

st.set_page_config(
    page_title="PageWise",
    page_icon="assets/logo.png",
    layout="centered",
)

inject_css()

try:
    validate_config()
except EnvironmentError as e:
    st.error(str(e))
    st.stop()

st.markdown(
    """
    <div class="pw-hero">
        <img src="app/static/logo2.png" width="200" style="margin-bottom: 0.5rem;">
        <h1>PageWise</h1>
        <div class="pw-tagline">A RAG-based chat with your documents</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="pw-toc">', unsafe_allow_html=True)
render_toc_item("Semantic search over your PDF", "I")
render_toc_item("Answers grounded strictly in context", "II")
render_toc_item("Page-level source attribution", "III")
render_toc_item("Nothing persists after you leave", "IV")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Begin Reading →", use_container_width=True):
        st.switch_page("pages/1_Chat.py")