import base64
import os
import shutil
import textwrap
import streamlit as st

from web_ingestion import WebIngestion
from prompt import PromptBuilder
from llm import LLM
from vector_store import VectorStore
from router import Router



# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Prasuna |  AI Assistant",
    page_icon="✨",
    layout="centered"
)


# ============================================================
# IMAGE HELPER
# ============================================================

def get_image_base64(file_path):

    if os.path.exists(file_path):

        ext = os.path.splitext(file_path)[1].lower()

        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }

        mime_type = mime_map.get(ext, "image/png")

        with open(file_path, "rb") as image_file:

            encoded_string = base64.b64encode(
                image_file.read()
            ).decode()

        return f"data:{mime_type};base64,{encoded_string}"

    return ""


img_data = get_image_base64("picture1.png")

# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    f"""
    <div class="hero-container">
        <img src="{img_data}" class="header-icon" alt="Prasuna logo">
        <div class="hero-title">Prasuna</div>
        <div class="hero-subtitle">Your AI Assistant</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR PROFILE CARD
# ============================================================

sidebar_img = get_image_base64("profile.png")

with st.sidebar:

    sidebar_html = f"""
    <div class="sidebar-card">
        <div class="sidebar-photo-wrapper">
            <img src="{sidebar_img}" class="sidebar-photo" alt="Profile photo">
        </div>
        <div class="sidebar-name">Pransu Farswan</div>
        <div class="sidebar-role">AI Engineer &amp; Developer</div>
        <hr class="sidebar-divider">
        <div class="sidebar-section-title">🤖 About Prasuna AI</div>
        <div class="sidebar-text">
            Prasuna AI is a web-augmented AI assistant built using RAG,
            combining live web search with retrieval-augmented generation
            to answer questions with up-to-date context.
        </div>
        <a href="https://github.com/pransufarswan111-hash" target="_blank" class="sidebar-github-btn">
            🐙 View my GitHub
        </a>
        <div class="sidebar-section-title" style="margin-top:22px;">⚙️ Technology</div>
        <ul class="sidebar-tech-list">
            <li>🔍 Web Search</li>
            <li>🌐 Web Scraping</li>
            <li>🧬 RAG Pipeline</li>
            <li>📊 FAISS</li>
            <li>🦙 LLM</li>
            <li>🐍 Python</li>
            <li>🎈 Streamlit</li>
        </ul>
        <div class="sidebar-footer">Prasuna AI • v1.0</div>
    </div>
    """

    st.markdown(
        textwrap.dedent(sidebar_html),
        unsafe_allow_html=True
    )

# ============================================================
# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================================
       HEADER
       ========================================= */

    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 1.5rem 0 1rem 0;
    }

    .header-icon {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #888888;
        font-size: 0.95rem;
        margin-top: 4px;
    }


    /* =========================================
       SIDEBAR PROFILE CARD
       ========================================= */

    .sidebar-card {
        border: 1px dashed #d63384;
        border-radius: 10px;
        padding: 22px 18px;
        margin: 10px 4px;
        text-align: center;
        background-color: var(--secondary-background-color);
    }

    .sidebar-photo-wrapper {
        display: flex;
        justify-content: center;
        margin-bottom: 14px;
    }

    .sidebar-photo {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid var(--text-color);
        opacity: 0.9;
    }

    .sidebar-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-color);
    }

    .sidebar-role {
        font-size: 0.8rem;
        color: var(--text-color);
        opacity: 0.65;
        margin-top: 2px;
    }

    .sidebar-divider {
        border: none;
        border-top: 1px dashed var(--text-color);
        opacity: 0.2;
        margin: 16px 0;
    }

    .sidebar-section-title {
        text-align: left;
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-color);
        margin-bottom: 8px;
    }

    .sidebar-text {
        text-align: left;
        font-size: 0.8rem;
        color: var(--text-color);
        opacity: 0.75;
        line-height: 1.5;
        margin-bottom: 14px;
    }

    .sidebar-github-btn {
        display: inline-block;
        text-decoration: none;
        font-size: 0.8rem;
        color: var(--text-color);
        background-color: var(--background-color);
        border: 1px solid var(--text-color);
        border-opacity: 0.2;
        border-radius: 6px;
        padding: 6px 14px;
        margin-top: 4px;
    }

    .sidebar-github-btn:hover {
        background-color: #d63384;
        border-color: #d63384;
        color: #ffffff;
    }

    .sidebar-tech-list {
        list-style: none;
        padding: 0;
        margin: 0;
        text-align: left;
    }

    .sidebar-tech-list li {
        font-size: 0.82rem;
        color: var(--text-color);
        opacity: 0.85;
        padding: 5px 0;
        border-bottom: 1px dashed var(--text-color);
    }

    .sidebar-tech-list li {
        border-bottom-color: rgba(128, 128, 128, 0.25);
    }

    .sidebar-tech-list li:last-child {
        border-bottom: none;
    }

    .sidebar-footer {
        margin-top: 20px;
        font-size: 0.7rem;
        color: var(--text-color);
        opacity: 0.5;
    }


    /* =========================================
       USER MESSAGE
       ========================================= */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) {
        flex-direction: row-reverse !important;
        background-color: #2b5278 !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: auto !important;
        width: fit-content !important;
        max-width: 80% !important;
    }


    /* =========================================
       ASSISTANT MESSAGE
       ========================================= */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: auto !important;
        width: fit-content !important;
        max-width: 85% !important;
    }


    /* =========================================
       CHAT INPUT
       ========================================= */

    div[data-testid="stBottom"] {
        padding-bottom: 25px !important;
    }


    /* =========================================
       CLEAR BUTTON
       ========================================= */

    div[data-testid="stButton"] {
        position: fixed !important;
        bottom: 30px !important;
        left: 20px !important;
        width: auto !important;
        height: auto !important;
        z-index: 999999 !important;
    }

    div[data-testid="stButton"] > button {
        width: auto !important;
        min-width: 0px !important;
        padding: 4px 10px !important;
        font-size: 0.75rem !important;
        height: 30px !important;
        line-height: 1 !important;
        background-color: #2b2b2b !important;
        color: #dddddd !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-testid="stButton"] > button:hover {
        background-color: #ff4d4d !important;
        color: #ffffff !important;
        border-color: #ff4d4d !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# ============================================================
# LOAD PIPELINE
# ============================================================

@st.cache_resource
def load_pipeline():

    pipeline = WebIngestion()

    if os.path.exists("vector_db/index.faiss"):

        pipeline.vector_store.load()

    return pipeline


@st.cache_resource
def load_llm():

    return LLM()


pipeline = load_pipeline()

llm = load_llm()

prompt_builder = PromptBuilder()

router = Router()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# CLEAR BUTTON
# ============================================================

if st.button(
    "🗑️ Clear",
    type="secondary"
):

    st.session_state.messages = []

    if os.path.exists("vector_db"):

        shutil.rmtree(
            "vector_db",
            ignore_errors=True
        )

    pipeline.vector_store = VectorStore(
        dimension=768
    )

    st.rerun()


# ============================================================
# DISPLAY OLD MESSAGES
# ============================================================

for msg in st.session_state.messages:

    avatar = (
        "👤"
        if msg["role"] == "user"
        else "✨"
    )

    st.chat_message(
        msg["role"],
        avatar=avatar
    ).write(
        msg["content"]
    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Try me..."
)


# ============================================================
# MAIN CHAT LOGIC
# ============================================================

if question:

    # ========================================================
    # 1. SHOW USER QUESTION
    # ========================================================

    st.chat_message(
        "user",
        avatar="👤"
    ).write(question)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ========================================================
    # 1b. BUILD CONVERSATION HISTORY FOR THE LLM
    # ========================================================

    MAX_HISTORY_MESSAGES = 20  # last 10 user/assistant turns

    def build_contents(final_text):

        # exclude the question we just appended above -
        # it gets added back as the final turn below
        history = st.session_state.messages[:-1]

        history = history[-MAX_HISTORY_MESSAGES:]

        contents = []

        for msg in history:

            role = "model" if msg["role"] == "assistant" else "user"

            contents.append(
                {
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                }
            )

        contents.append(
            {
                "role": "user",
                "parts": [{"text": final_text}]
            }
        )

        return contents



    # ========================================================
    # 2. ASSISTANT RESPONSE AREA
    # ========================================================

    with st.chat_message(
        "assistant",
        avatar="✨"
    ):

        placeholder = st.empty()


        # ====================================================
        # 3. THINKING
        # ====================================================

        placeholder.markdown(
            "✨ Brain Storming..."
        )


        # ====================================================
        # 3b. DECIDE WHETHER RETRIEVAL IS NEEDED
        # ====================================================

        need_retrieval = router.should_search(question)


        if need_retrieval:

            # ====================================================
            # 4. CREATE QUERY EMBEDDING
            # ====================================================

            query_embedding = (
                pipeline.embedder.create_embeddings(
                    [question]
                )
            )


            # ====================================================
            # 5. SEARCH EXISTING VECTOR STORE
            # ====================================================

            chunks = pipeline.vector_store.search(
                query_embedding[0],
                k=3,
                threshold=0.60,
                debug=True
            )


            # ====================================================
            # 6. WEB SEARCH IF NOTHING RELEVANT
            # ====================================================

            if not chunks:

                placeholder.markdown(
                    "🌐 Mulling..."
                )

                pipeline.ingest(
                    question
                )


                placeholder.markdown(
                    "🧠 Understanding information..."
                )


                # Re-create query embedding
                query_embedding = (
                    pipeline.embedder.create_embeddings(
                        [question]
                    )
                )


                placeholder.markdown(
                    "🔍 Finding relevant answers..."
                )


                # Search newly created knowledge base
                chunks = pipeline.vector_store.search(
                    query_embedding[0],
                    k=3,
                    threshold=0.60,
                    debug=True
                )


            # ====================================================
            # 7. DEBUG SEARCH
            # ====================================================

            debug_results = (
                pipeline.vector_store.search_debug(
                    query_embedding[0],
                    k=5
                )
            )


            # ====================================================
            # 8. FALLBACK TO BEST RETRIEVED RESULT
            # ====================================================

            if not chunks and debug_results:

                best_result = debug_results[0]

                best_score = best_result["score"]


                # Use Rank 1 if it is relevant
                if best_score >= 0.60:

                    chunks = [
                        {
                            "rank": best_result["rank"],
                            "text": best_result["text"],
                            "score": best_score
                        }
                    ]


                    print(
                        f"[Fallback] "
                        f"Using Rank 1 "
                        f"score={best_score:.4f}"
                    )


            # ====================================================
            # 9. RETRIEVAL DEBUG PANEL
            # ====================================================

            with st.expander(
                "🔎 Retrieved Content",
                expanded=False
            ):

                if debug_results:

                    st.caption(
                        f"Showing top "
                        f"{len(debug_results)} "
                        f"retrieved chunks"
                    )


                    for item in debug_results:

                        score = item["score"]


                        if score >= 0.60:

                            status = (
                                "✅ Relevant"
                            )

                        else:

                            status = (
                                "⚠️ Below threshold"
                            )


                        st.markdown(
                            f"### {status} — "
                            f"Rank {item['rank']}"
                        )


                        st.caption(
                            f"Similarity score: "
                            f"`{score:.4f}`"
                        )


                        st.write(
                            item["text"]
                        )


                        st.divider()


                else:

                    st.warning(
                        "No content was retrieved "
                        "from the vector store."
                    )


            # ====================================================
            # 10. BUILD CONTEXT
            # ====================================================

            if chunks:

                context = "\n\n".join(
                    item["text"]
                    for item in chunks
                )


                # Optional terminal debugging
                print(
                    "\n========== FINAL CONTEXT =========="
                )

                print(
                    context[:2000]
                )

                print(
                    "===================================\n"
                )


                prompt = (
                    prompt_builder.build_prompt(
                        question,
                        context
                    )
                )

            else:

                prompt = None


            # ====================================================
            # 11. GENERATE ANSWER
            # ====================================================

            if prompt:

                full_answer = ""


                for chunk in llm.stream(
                    build_contents(prompt)
                ):

                    token = (
                        chunk
                        .get("message", {})
                        .get("content", "")
                    )


                    full_answer += token


                    placeholder.markdown(
                        full_answer + "▌"
                    )


                placeholder.markdown(
                    full_answer
                )


            # ====================================================
            # 12. FALLBACK TO GENERAL KNOWLEDGE
            # ====================================================

            else:

                placeholder.markdown(
                    "No matching web content found — answering from general knowledge..."
                )

                full_answer = ""

                for chunk in llm.stream(
                    build_contents(question)
                ):

                    token = (
                        chunk
                        .get("message", {})
                        .get("content", "")
                    )

                    full_answer += token

                    placeholder.markdown(
                        full_answer + "▌"
                    )

                placeholder.markdown(
                    full_answer
                )

        else:

            placeholder.markdown(
                " Tracking..."
            )

            full_answer = ""

            for chunk in llm.stream(
                build_contents(question)
            ):

                token = (
                    chunk
                    .get("message", {})
                    .get("content", "")
                )

                full_answer += token

                placeholder.markdown(
                    full_answer + "▌"
                )

            placeholder.markdown(
                full_answer
            )





    # ========================================================
    # 13. SAVE ASSISTANT RESPONSE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_answer
        }
    )


    # ========================================================
    # 14. RESET TEMPORARY VECTOR STORE
    # ========================================================

    if os.path.exists(
        "vector_db"
    ):

        shutil.rmtree(
            "vector_db",
            ignore_errors=True
        )


    pipeline.vector_store = VectorStore(
        dimension=768
    )