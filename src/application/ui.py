from __future__ import annotations

from textwrap import dedent
from typing import Any, Mapping

import streamlit as st


APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #14161f;
        --panel: #1b1e29;
        --panel-soft: #202432;
        --panel-muted: #242938;
        --border: rgba(255, 255, 255, 0.08);
        --text: #f5f7fb;
        --muted: #a8afc3;
        --accent: #ea5555;
        --accent-soft: rgba(234, 85, 85, 0.14);
        --purple: #7b4ae2;
        --green: #68c490;
        --shadow: 0 22px 60px rgba(0, 0, 0, 0.34);
    }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(123, 74, 226, 0.16), transparent 26%),
            radial-gradient(circle at top right, rgba(234, 85, 85, 0.13), transparent 18%),
            linear-gradient(180deg, #12141c 0%, #0d1017 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1380px;
        padding-top: 0.55rem;
        padding-bottom: 1rem;
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }

    header[data-testid="stHeader"] {
        background: linear-gradient(180deg, rgba(13, 16, 23, 0.96), rgba(13, 16, 23, 0.72));
    }

    div[data-testid="stToolbar"] {
        right: 0.85rem;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
        align-items: flex-start;
    }

    .panel-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015));
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(14px);
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin-bottom: 1rem;
    }

    .settings-intro {
        margin-bottom: 1rem;
    }

    .single-page-section {
        margin-top: 1.25rem;
    }

    .section-headline {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.3rem;
    }

    .section-copy {
        color: var(--muted);
        margin-bottom: 0.9rem;
    }

    .brand-badge {
        width: 42px;
        height: 42px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(123, 74, 226, 0.35), rgba(234, 85, 85, 0.28));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.12);
        font-size: 1.25rem;
    }

    .brand-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
    }

    .brand-copy, .eyebrow, .helper-copy, .meta-copy, .topic-list li {
        color: var(--muted);
    }

    .hero h1 {
        margin: 0;
        font-size: 2.35rem;
        line-height: 1.02;
        letter-spacing: -0.045em;
    }

    .hero p {
        margin-top: 0.35rem;
        color: var(--muted);
    }

    .section-label {
        color: var(--text);
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.65rem;
    }

    .feature-list {
        display: grid;
        gap: 0.65rem;
    }

    .feature-pill {
        padding: 0.95rem 1rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid transparent;
        color: var(--text);
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }

    .feature-pill.active {
        background: rgba(234, 85, 85, 0.16);
        border-color: rgba(234, 85, 85, 0.22);
        color: #ff8f8f;
    }

    .feature-icon {
        width: 1.9rem;
        height: 1.9rem;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.04);
        font-size: 0.95rem;
    }

    .feature-copy {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
    }

    .feature-copy small {
        color: var(--muted);
        font-weight: 500;
    }

    .message-card {
        border-radius: 18px;
        border: 1px solid var(--border);
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem 1.05rem;
        margin-bottom: 1rem;
    }

    .message-card.user-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
    }

    .message-card.assistant-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.025));
        border-color: rgba(255,255,255,0.1);
    }

    .message-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.7rem;
    }

    .message-author {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 700;
    }

    .avatar {
        width: 38px;
        height: 38px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(123, 74, 226, 0.18);
        color: #cdb8ff;
        font-size: 1.15rem;
    }

    .avatar.user {
        background: rgba(86, 112, 255, 0.2);
        color: #b9c8ff;
    }

    .message-role.user {
        color: #ff8f8f;
    }

    .message-role.assistant {
        color: #bd9cff;
    }

    .timestamp {
        color: #8f97aa;
        font-size: 0.82rem;
    }

    .notes-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.45rem 0.75rem;
        border-radius: 999px;
        background: rgba(104, 196, 144, 0.14);
        border: 1px solid rgba(104, 196, 144, 0.24);
        color: #9fe6b8;
        font-size: 0.85rem;
        margin-bottom: 0.9rem;
    }

    .feedback-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.6rem;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-left: 0.55rem;
        border: 1px solid rgba(255,255,255,0.12);
        color: var(--muted);
    }

    .feedback-chip.helpful {
        color: #9fe6b8;
        border-color: rgba(104, 196, 144, 0.28);
        background: rgba(104, 196, 144, 0.12);
    }

    .feedback-chip.needs-work {
        color: #ffb3b3;
        border-color: rgba(234, 85, 85, 0.26);
        background: rgba(234, 85, 85, 0.1);
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 3rem;
        border-radius: 14px;
        border: 1px solid var(--border);
        background: rgba(255, 255, 255, 0.04);
        color: var(--text);
        font-weight: 600;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: rgba(234, 85, 85, 0.38);
        color: #ffffff;
    }

    .message-action-row div[data-testid="stButton"] > button {
        min-height: 2.3rem;
        border-radius: 12px;
        font-size: 0.85rem;
        background: rgba(255,255,255,0.025);
    }

    .cta-card div[data-testid="stButton"] > button,
    .send-row div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(180deg, #f05b5b 0%, #dd4949 100%);
        border-color: transparent;
        color: white;
        box-shadow: 0 14px 34px rgba(234, 85, 85, 0.24);
    }

    .stTextInput > div > div,
    .stTextArea textarea,
    .stSelectbox > div > div,
    .stFileUploader,
    .stSlider {
        background: transparent;
    }

    /* File uploader dark theme fix */
    [data-testid="stFileUploader"] section {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px dashed var(--border) !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] section:hover {
        background: rgba(255, 255, 255, 0.07) !important;
        border-color: var(--accent) !important;
    }

    [data-testid="stFileUploader"] section > div {
        color: var(--text-muted) !important;
    }

    [data-testid="stFileUploader"] button {
        background: rgba(255, 255, 255, 0.08) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.04);
        color: var(--text);
        border-radius: 14px;
        border: 1px solid var(--border);
        min-height: 3rem;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border);
        border-radius: 14px;
        color: var(--text);
    }

    div[data-testid="stRadio"] > label {
        display: none;
    }

    div[data-testid="stRadio"] [role="radiogroup"] {
        display: grid;
        gap: 0.85rem;
        margin-bottom: 1rem;
        border-bottom: none;
    }

    div[data-testid="stRadio"] [role="radio"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid transparent;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        min-height: auto;
        color: var(--text);
        box-shadow: none;
    }

    div[data-testid="stRadio"] [role="radio"]:hover {
        border-color: rgba(255,255,255,0.1);
    }

    div[data-testid="stRadio"] [role="radio"][aria-checked="true"] {
        color: #ff9a9a;
        background: rgba(234, 85, 85, 0.16);
        border-color: rgba(234, 85, 85, 0.22);
    }

    .topic-list {
        margin: 0;
        padding-left: 1.15rem;
        display: grid;
        gap: 0.65rem;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.8rem;
    }

    .stat-card {
        border-radius: 16px;
        padding: 0.95rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
    }

    .stat-value {
        color: var(--text);
        font-size: 1.3rem;
        font-weight: 700;
    }

    .hero-meta {
        display: inline-flex;
        align-items: center;
        gap: 0.65rem;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        color: var(--muted);
        font-size: 0.83rem;
        margin-top: 0.45rem;
    }

    .welcome-card {
        padding: 1.15rem 1.15rem 1rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(123, 74, 226, 0.12), rgba(234, 85, 85, 0.08));
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }

    .welcome-card h3 {
        margin: 0 0 0.3rem 0;
        font-size: 1.05rem;
    }

    .welcome-card p {
        margin: 0;
        color: var(--muted);
    }

    .quick-actions-label {
        color: var(--muted);
        font-size: 0.82rem;
        margin: 0.35rem 0 0.7rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .composer-card {
        margin-top: 1rem;
        padding: 0.9rem;
        border-radius: 18px;
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
    }

    .composer-hint {
        color: var(--muted);
        font-size: 0.84rem;
        margin-bottom: 0.55rem;
    }

    .copied-card {
        margin-top: 0.85rem;
        padding: 0.9rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.025);
    }

    .side-card-title {
        margin: 0 0 0.35rem 0;
        font-size: 1.35rem;
    }

    .side-separator {
        border-top: 1px dashed rgba(255,255,255,0.12);
        margin: 0.95rem 0;
    }

    .topic-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.09);
        background: rgba(255,255,255,0.03);
        color: var(--muted);
        font-size: 0.82rem;
        margin-bottom: 0.85rem;
    }

    .upload-dropzone {
        padding: 1.1rem;
        border-radius: 18px;
        border: 1px dashed rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.02);
        margin-bottom: 1rem;
    }

    @media (max-width: 1100px) {
        .left-panel, .main-panel, .right-panel {
            min-height: auto;
        }
    }
</style>
"""


def inject_styles() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)


def render_html(markup: str) -> None:
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)


def render_shell_start() -> None:
    return None


def render_shell_end() -> None:
    return None


def render_left_panel(
    app_icon: str,
    active_tab: str,
    model_name: str,
    difficulty: str,
    mode: str,
    temperature: float,
) -> tuple[str, str, str, float, str]:
    render_html(
        f'''
        <div class="panel-card settings-intro">
            <div class="brand-row">
                <div class="brand-badge">{app_icon}</div>
                <div>
                    <div class="brand-title">Tutor Settings</div>
                    <div class="brand-copy">Tune the assistant before each question.</div>
                </div>
            </div>
        </div>
        '''
    )

    model_options = ["mistral", "llama3.2:3b", "llama3.2:1b", "llama3.1:8b", "gemma3:12b"]
    default_model_index = model_options.index(model_name) if model_name in model_options else 0
    model_name = st.selectbox("Choose model", model_options, index=default_model_index)
    difficulty = st.selectbox(
        "Difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner", "Intermediate", "Advanced"].index(difficulty),
    )
    mode = st.selectbox(
        "Mode",
        ["Explain", "Quiz", "Hint"],
        index=["Explain", "Quiz", "Hint"].index(mode),
    )
    temperature = st.slider("Temperature", 0.0, 1.0, float(temperature), 0.1)

    render_html(
        '''
        <div class="panel-card">
            <div class="section-label">Features</div>
        </div>
        '''
    )

    feature_options = ["Chat", "Upload", "Settings"]
    feature_captions = [
        "Ask and learn interactively",
        "Ground answers with notes",
        "Adjust tutor behavior",
    ]
    selected_feature_index = feature_options.index(active_tab) if active_tab in feature_options else 0
    active_tab = st.radio(
        "Features",
        feature_options,
        index=selected_feature_index,
        captions=feature_captions,
        key="feature_panel_selector",
        label_visibility="collapsed",
    )

    render_html(
        '''
        <div class="panel-card">
            <div class="section-label">About</div>
            <div class="helper-copy">Your personal ML tutor. Ask questions, get explanations, take quizzes and learn better.</div>
        </div>
        '''
    )

    st.markdown("---")
    clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)
    if clear_clicked:
        return model_name, difficulty, mode, temperature, active_tab, True

    return model_name, difficulty, mode, temperature, active_tab, False


def render_message_card(message: Mapping[str, Any]) -> str | None:
    render_message_header(message)

    if message["role"] == "assistant" and message.get("source_snippets"):
        render_html('<div class="notes-chip">📚 Answer grounded in uploaded notes</div>')

    st.markdown(message["content"])
    action = None
    if message["role"] == "assistant":
        copy_col, up_col, down_col, spacer = st.columns([1.05, 1, 1.15, 5])
        with copy_col:
            if st.button("Copy", key=f"copy_{message['id']}", use_container_width=True):
                action = "copy"
        with up_col:
            if st.button("Helpful", key=f"helpful_{message['id']}", use_container_width=True):
                action = "helpful"
        with down_col:
            if st.button("Needs work", key=f"needs_work_{message['id']}", use_container_width=True):
                action = "needs-work"
        snippets = message.get("source_snippets") or []
        if snippets:
            with st.expander("Retrieved source snippets"):
                for index, snippet in enumerate(snippets, start=1):
                    st.markdown(f"**Snippet {index}:**")
                    st.write(snippet)

    return action


def render_message_header(message: Mapping[str, Any]) -> None:
    role = message["role"]
    role_label = "You" if role == "user" else "Tutor"
    avatar = "👤" if role == "user" else "🤖"
    rating = message.get("rating")
    left_col, right_col = st.columns([5, 1])
    with left_col:
        label = f"{avatar} {role_label}"
        if rating == "helpful":
            label += "  |  Helpful"
        elif rating == "needs-work":
            label += "  |  Needs work"
        st.markdown(f"**{label}**")
    with right_col:
        st.caption(message.get("timestamp", ""))


def render_streaming_assistant(message: Mapping[str, Any]) -> Any:
    render_message_header(message)

    if message.get("source_snippets"):
        render_html('<div class="notes-chip">📚 Answer grounded in uploaded notes</div>')

    return st.empty()


def render_empty_chat_state() -> None:
    st.markdown(
        '''
        <div class="welcome-card">
            <h3>Start a conversation</h3>
            <p>Ask about overfitting, bias vs variance, gradient descent, regression, or upload your own notes for grounded answers.</p>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_quick_actions() -> tuple[str, str] | None:
    st.markdown('<div class="quick-actions-label">Quick actions</div>', unsafe_allow_html=True)
    action_cols = st.columns(4)
    actions = [
        ("✨ Explain more", "Explain this topic in more depth, but keep it easy to follow."),
        ("🔎 Give example", "Give a concrete example for this topic."),
        ("🧠 Make it simpler", "Explain the same topic in simpler words for a beginner."),
        ("🔁 Related topics", "List a few closely related machine learning topics to study next."),
    ]
    for column, (label, prompt) in zip(action_cols, actions):
        with column:
            if st.button(label, use_container_width=True):
                return label, prompt
    return None


def render_chat_input() -> str | None:
    prompt = None
    st.markdown('<div class="composer-card">', unsafe_allow_html=True)
    st.markdown('<div class="composer-hint">Type your message and send it to the tutor.</div>', unsafe_allow_html=True)
    if st.session_state.get("clear_chat_input"):
        st.session_state.chat_input = ""
        st.session_state.clear_chat_input = False
    input_col, send_col = st.columns([6.2, 1])
    with input_col:
        question = st.text_input(
            "Type your message",
            placeholder="Type your question here...",
            key="chat_input",
            label_visibility="collapsed",
        )
    with send_col:
        send_clicked = st.button("➤", use_container_width=True, key="send_chat")

    if send_clicked and question.strip():
        prompt = question
    st.markdown("</div>", unsafe_allow_html=True)
    return prompt


def render_copied_message(text: str) -> None:
    st.markdown('<div class="section-label">Copied response</div>', unsafe_allow_html=True)
    st.code(text)


def render_answer_evaluator(feedback: str | None) -> str | None:
    submitted_answer = None
    st.markdown('<div class="section-label">Try answering yourself</div>', unsafe_allow_html=True)
    answer = st.text_area(
        "Your answer",
        key="eval_input",
        height=120,
        placeholder="Write your own explanation and get tutor feedback...",
        label_visibility="collapsed",
    )
    if st.button("Evaluate my answer", use_container_width=True):
        submitted_answer = answer

    if feedback:
        st.markdown("### Feedback")
        st.write(feedback)
    return submitted_answer


def render_upload_tab(notes_loaded: bool, loaded_filename: str | None) -> tuple[Any | None, bool]:
    st.markdown(
        '''
        <div class="upload-dropzone">
            <div class="section-label">Upload Notes</div>
            <div class="helper-copy">Drop a PDF, DOCX, or TXT file to ground answers in your own class material.</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload notes",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        key=f"upload_notes_{st.session_state.upload_widget_key}",
    )
    reset_clicked = False

    if notes_loaded:
        st.markdown(f"Loaded file: **{loaded_filename}**")
        if st.button("Reset Notes", use_container_width=True):
            reset_clicked = True

    return uploaded_file, reset_clicked


def render_settings_tab(
    model_name: str,
    difficulty: str,
    mode: str,
    temperature: float,
    message_count: int,
    notes_loaded: bool,
    loaded_filename: str | None,
) -> bool:
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    stats = [
        ("Model", model_name),
        ("Difficulty", difficulty),
        ("Mode", mode),
        ("Temp", f"{temperature:.1f}"),
    ]
    for label, value in stats:
        st.markdown(
            f'''
            <div class="stat-card">
                <div class="meta-copy">{label}</div>
                <div class="stat-value">{value}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    clear_chat_clicked = False
    st.markdown('<div class="section-label">Session Overview</div>', unsafe_allow_html=True)
    st.write("Messages in chat:", message_count)
    st.write("Notes loaded:", notes_loaded)
    if loaded_filename:
        st.write("Current file:", loaded_filename)
    if st.button("Clear Chat", use_container_width=True):
        clear_chat_clicked = True
    return clear_chat_clicked


def render_main_panel(app_icon: str, app_title: str) -> None:
    render_html(
        f'''
        <div class="panel-card hero">
            <div class="brand-row" style="margin-bottom: 0.4rem;">
                <div class="brand-badge">{app_icon}</div>
                <div>
                    <h1>{app_title}</h1>
                    <p>Local LLM + Tutor Prompting + Simple RAG</p>
                    <div class="hero-meta">● Live locally on Ollama · Tutor mode ready</div>
                </div>
            </div>
        </div>
        '''
    )


def close_main_panel() -> None:
    return None


def render_right_panel(mode: str, recent_topics: list[str]) -> tuple[str, str] | None:
    selected_action = None

    if mode == "Quiz":
        st.markdown('<div class="panel-card cta-card">', unsafe_allow_html=True)
        st.markdown('<div class="topic-badge">🧠 Learning mode</div>', unsafe_allow_html=True)
        st.markdown('<h3 class="side-card-title">Quiz</h3>', unsafe_allow_html=True)
        st.markdown('<div class="helper-copy">Generate a quiz question from the current topic.</div>', unsafe_allow_html=True)
        if st.button("Generate Quiz", use_container_width=True):
            selected_action = (
                "Create a short quiz on this topic with multiple choice questions and answers.",
                "Quiz",
            )
        st.markdown('<div class="side-separator"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if mode == "Hint":
        st.markdown('<div class="panel-card cta-card">', unsafe_allow_html=True)
        st.markdown('<div class="topic-badge">💡 Study assist</div>', unsafe_allow_html=True)
        st.markdown('<h3 class="side-card-title">Hint</h3>', unsafe_allow_html=True)
        st.markdown('<div class="helper-copy">Get a hint to understand the current concept better.</div>', unsafe_allow_html=True)
        if st.button("Give Hint", use_container_width=True):
            selected_action = (
                "Give me a short hint about this topic without fully answering it yet.",
                "Hint",
            )
        st.markdown('<div class="side-separator"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('### 📗 Recent Topics')
    if recent_topics:
        items = "".join(f"<li>{topic}</li>" for topic in recent_topics)
        st.markdown(f'<ul class="topic-list">{items}</ul>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="helper-copy">No recent topics yet. Start by asking your first ML question.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    return selected_action