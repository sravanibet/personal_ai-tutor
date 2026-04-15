import streamlit as st

from src.model.ollama_client import OllamaClient
from src.model.prompt_builder import build_messages
from src.utils.config import CONFIG


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title=CONFIG.app_title,
    page_icon=CONFIG.app_icon,
    layout="wide",
)

st.title(f"{CONFIG.app_icon} {CONFIG.app_title}")
st.caption("Base version: Pretrained local model + tutor prompting")

# =========================
# TABS (UI)
# =========================
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📂 Upload", "⚙️ Settings"])


# =========================
# SIDEBAR (UI)
# =========================
st.sidebar.header("Tutor Settings")

model_name = st.sidebar.selectbox(
    "Choose model",
    options=["mistral"],
    index=0,
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    options=["Beginner", "Intermediate", "Advanced"],
    index=0,
)

mode = st.sidebar.selectbox(
    "Mode",
    options=["Explain", "Quiz", "Hint"],
    index=0,
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1,
)


# =========================
# SESSION STATE
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages_for_display" not in st.session_state:
    st.session_state.messages_for_display = []


# =========================
# 💬 CHAT TAB
# =========================
with tab1:

    # Show messages
    for msg in st.session_state.messages_for_display:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.text_input("Ask a Machine Learning question...")

    if user_input:
        st.session_state.messages_for_display.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            client = OllamaClient(CONFIG.ollama_base_url)

            messages = build_messages(
                user_question=user_input,
                difficulty=difficulty,
                mode=mode,
                chat_history=st.session_state.chat_history,
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
            st.experimental_rerun()

    with col2:
        if st.button("Sample Question"):
            st.session_state.messages_for_display.append(
                {
                    "role": "user",
                    "content": "Explain overfitting in simple terms with an example."
                }
            )
            st.experimental_rerun()


# =========================
# 📂 UPLOAD TAB
# =========================
with tab2:
    st.header("📂 Upload File")

    uploaded_file = st.file_uploader("Upload a file")

    if uploaded_file:
        st.success("File uploaded successfully!")

        st.write("File Name:", uploaded_file.name)
        st.write("File Type:", uploaded_file.type)
        st.write("File Size:", uploaded_file.size, "bytes")


# =========================
# ⚙️ SETTINGS TAB
# =========================
with tab3:
    st.header("⚙️ Settings")

    st.write("Model:", model_name)
    st.write("Difficulty:", difficulty)
    st.write("Mode:", mode)
    st.write("Temperature:", temperature)