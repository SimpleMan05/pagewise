import streamlit as st

MOONLIT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, .pw-serif {
    font-family: 'Source Serif 4', serif !important;
}

/* Subtle starfield glow behind the whole app */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(143, 165, 201, 0.12), transparent),
        #0D1220;
}

/* Hide default Streamlit chrome for a cleaner look */
#MainMenu, footer, header {visibility: hidden;}

/* ---- Landing page hero ---- */
.pw-hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
}
.pw-hero h1 {
    font-size: 3rem;
    font-weight: 700;
    color: #E4E7EE;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.pw-hero .pw-tagline {
    color: #8FA5C9;
    font-size: 1.05rem;
    font-style: italic;
    font-family: 'Source Serif 4', serif;
}

/* ---- Table-of-contents style feature list ---- */
.pw-toc {
    max-width: 520px;
    margin: 2rem auto;
    padding: 1.5rem 0;
    border-top: 1px solid rgba(143, 165, 201, 0.25);
    border-bottom: 1px solid rgba(143, 165, 201, 0.25);
}
.pw-toc-item {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding: 0.55rem 0.2rem;
    color: #E4E7EE;
    font-size: 0.98rem;
}
.pw-toc-item .pw-toc-label {
    white-space: nowrap;
    padding-right: 0.5rem;
}
.pw-toc-item .pw-toc-dots {
    flex: 1;
    border-bottom: 1px dotted rgba(107, 114, 128, 0.6);
    margin: 0 0.4rem;
    transform: translateY(-4px);
}
.pw-toc-item .pw-toc-page {
    color: #C9A876;
    font-family: 'Source Serif 4', serif;
    font-style: italic;
    white-space: nowrap;
}

/* ---- Chat bubbles ---- */
.pw-chat-row {
    display: flex;
    margin: 0.6rem 0;
    width: 100%;
}
.pw-chat-row.user {
    justify-content: flex-end;
}
.pw-chat-row.assistant {
    justify-content: flex-start;
}
.pw-bubble {
    max-width: 72%;
    padding: 0.7rem 1rem;
    border-radius: 14px;
    line-height: 1.5;
    font-size: 0.96rem;
}
.pw-bubble.user {
    background: #8FA5C9;
    color: #0D1220;
    border-bottom-right-radius: 4px;
}
.pw-bubble.assistant {
    background: #151B2E;
    color: #E4E7EE;
    border: 1px solid rgba(143, 165, 201, 0.25);
    border-bottom-left-radius: 4px;
}
</style>
"""


def inject_css():
    st.markdown(MOONLIT_CSS, unsafe_allow_html=True)


def render_toc_item(label: str, page: str):
    st.markdown(
        f"""
        <div class="pw-toc-item">
            <span class="pw-toc-label">{label}</span>
            <span class="pw-toc-dots"></span>
            <span class="pw-toc-page">{page}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_bubble(role: str, content: str):
    css_role = "user" if role == "user" else "assistant"
    st.markdown(
        f"""
        <div class="pw-chat-row {css_role}">
            <div class="pw-bubble {css_role}">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )