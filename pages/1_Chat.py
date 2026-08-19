import streamlit as st
import uuid

from src.ingest import ingest_pdf
from src.retrieve import connect_to_collection, get_answer
from src.qdrant_utils import delete_collection

st.set_page_config(
    page_title="PageWise — Chat",
    page_icon="📄",
    layout="centered",
)

st.caption("Let us see what we have")
st.title("PageWise")

# ---------- Session state initialization ----------
if "collection_name" not in st.session_state:
    st.session_state.collection_name = f"pagewise_{uuid.uuid4().hex[:8]}"

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- Helper: full reset + redirect to home on error ----------
def fail_and_redirect(error_message: str):
    delete_collection(st.session_state.collection_name)
    st.session_state.clear()
    st.error(error_message)
    st.stop()


# ---------- Upload gate ----------
if not st.session_state.pdf_ready:
    st.subheader("Upload a PDF to get started")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Reading and embedding your PDF... this may take a moment"):
            try:
                vector_db = ingest_pdf(uploaded_file, st.session_state.collection_name)
                st.session_state.vector_db = vector_db
                st.session_state.pdf_ready = True
                st.rerun()
            except Exception as e:
                fail_and_redirect(f"Something went wrong processing your PDF: {e}")

else:
    # ---------- Chat interface ----------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask something about your PDF...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if st.session_state.vector_db is None:
                        st.session_state.vector_db = connect_to_collection(
                            st.session_state.collection_name
                        )
                    answer = get_answer(st.session_state.vector_db, user_query)
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    fail_and_redirect(f"Something went wrong answering your question: {e}")

    # ---------- End Chat button ----------
    st.divider()
    if st.button("End Chat", use_container_width=True):
        delete_collection(st.session_state.collection_name)
        st.session_state.clear()
        st.success("Chat ended. Your data has been cleared.")
        st.switch_page("app.py")