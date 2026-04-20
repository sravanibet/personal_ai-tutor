import os
import tempfile
import streamlit as st
from answer_evaluator import evaluate_answer


from src.model.ollama_client import OllamaClient
from src.model.prompt_builder import build_messages
from src.utils.config import CONFIG

from src.rag.loader import load_text_from_file
from src.rag.chunker import chunk_text
from src.rag.retriever import SimpleRetriever


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title=CONFIG.app_title,
    page_icon=CONFIG.app_icon,
    layout="wide",
)

st.title(f"{CONFIG.app_icon} {CONFIG.app_title}")
st.caption("Local LLM + Tutor Prompting + Simple RAG")


# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📂 Upload", "⚙️ Settings"])


# =========================
# SIDEBAR
# =========================
st.sidebar.header("Tutor Settings")

model_name = st.sidebar.selectbox(
    "Choose model",
    ["mistral"],
    index=0
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"],
    index=0
)

mode = st.sidebar.selectbox(
    "Mode",
    ["Explain", "Quiz", "Hint"],
    index=0
)

temperature = st.sidebar.slider(
    "Temperature",
    0.0,
    1.0,
    0.3,
    0.1
)


# =========================
# SESSION STATE
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages_for_display" not in st.session_state:
    st.session_state.messages_for_display = []

if "retriever" not in st.session_state:
    st.session_state.retriever = SimpleRetriever()

if "notes_loaded" not in st.session_state:
    st.session_state.notes_loaded = False

if "loaded_filename" not in st.session_state:
    st.session_state.loaded_filename = None


# =========================
# UPLOAD TAB
# =========================
with tab2:
    st.header("📂 Upload Notes")

    uploaded_file = st.file_uploader(
        "Upload PDF, DOCX, or TXT",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:
        st.success("File uploaded successfully!")
        st.write("File Name:", uploaded_file.name)
        st.write("File Type:", uploaded_file.type)
        st.write("File Size:", uploaded_file.size, "bytes")

        if uploaded_file.name != st.session_state.loaded_filename:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{uploaded_file.name.split('.')[-1]}"
            ) as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name

            try:
                text = load_text_from_file(temp_path)
                chunks = chunk_text(text)
                st.session_state.retriever.add_chunks(chunks)
                st.session_state.notes_loaded = True
                st.session_state.loaded_filename = uploaded_file.name
                st.success(f"Loaded notes: {uploaded_file.name}")
                st.info(f"Created {len(chunks)} chunks")
            except Exception as exc:
                st.error(f"Failed to load file: {exc}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    if st.session_state.notes_loaded:
        st.write(f"Current loaded notes: **{st.session_state.loaded_filename}**")

        if st.button("Reset Notes"):
            st.session_state.retriever = SimpleRetriever()
            st.session_state.notes_loaded = False
            st.session_state.loaded_filename = None
            st.rerun()


# =========================
# CHAT TAB
# =========================
with tab1:
    for msg in st.session_state.messages_for_display:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a Machine Learning question...")

    if user_input:
        st.session_state.messages_for_display.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            client = OllamaClient(CONFIG.ollama_base_url)

            retrieved_context = None
            source_snippets = []

            if st.session_state.notes_loaded:
                source_snippets = st.session_state.retriever.retrieve(user_input, top_k=1)

                if source_snippets:
                    shortened_snippets = [snippet[:800] for snippet in source_snippets]
                    retrieved_context = "\n\n---\n\n".join(shortened_snippets)

            messages = build_messages(
                user_question=user_input,
                difficulty=difficulty,
                mode=mode,
                chat_history=st.session_state.chat_history,
                retrieved_context=retrieved_context,
            )

            response = client.chat(
                model=model_name,
                messages=messages,
                temperature=temperature,
            )

            st.session_state.messages_for_display.append(
                {"role": "assistant", "content": response}
            )

            with st.chat_message("assistant"):
                st.markdown(response)

                if source_snippets:
                    with st.expander("Retrieved source snippets"):
                        for i, snippet in enumerate(source_snippets, start=1):
                            st.markdown(f"**Snippet {i}:**")
                            st.write(snippet)
                           
           

                st.markdown("---")
                st.markdown("### ✍️ Try answering yourself")
                st.markdown("<br>", unsafe_allow_html=True)

                user_answer = st.text_input("Your answer:", key="eval_input")

                if user_answer and len(user_answer) > 10:
                    feedback = evaluate_answer(user_input, user_answer)

                    st.markdown("### 📊 Feedback")
                    st.write(feedback)
            

            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}
            )
            st.session_state.chat_history.append(
                {"role": "assistant", "content": response}
            )

        except Exception as exc:
            st.error(f"Error: {exc}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.messages_for_display = []
            st.rerun()

    with col2:
        if st.button("Sample Question"):
            sample = "Explain overfitting in simple terms with an example."
            st.session_state.messages_for_display.append(
                {"role": "user", "content": sample}
            )
            st.rerun()


# =========================
# SETTINGS TAB
# =========================
with tab3:
    st.header("⚙️ Settings")
    st.write("Model:", model_name)
    st.write("Difficulty:", difficulty)
    st.write("Mode:", mode)
    st.write("Temperature:", temperature)
    st.write("Notes loaded:", st.session_state.notes_loaded)

    if st.session_state.loaded_filename:
        st.write("Current file:", st.session_state.loaded_filename)