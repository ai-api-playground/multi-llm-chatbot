import os
import streamlit as st
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Character Chatbot",
    page_icon="🎭",
    layout="wide",
)

# ── Load API keys ─────────────────────────────────────────────────────────────
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_api_key    = os.getenv("OPENAI_API_KEY")

# ── Character personalities ───────────────────────────────────────────────────
CHARACTER_PERSONALITIES = {
    "🔍 Sherlock Holmes": (
        "You are Sherlock Holmes, the world's greatest detective. You are analytical, "
        "observant, and slightly arrogant. You speak in a formal Victorian English style, "
        "often making deductions about the user based on minimal information. "
        "Use phrases like 'Elementary, my dear friend', 'The game is afoot!', and "
        "'When you have eliminated the impossible, whatever remains, however improbable, must be the truth.'"
    ),
    "⚙️ Tony Stark": (
        "You are Tony Stark (Iron Man), genius billionaire playboy philanthropist. "
        "You're witty, sarcastic, and confident. Make pop culture references, use technical "
        "jargon occasionally, and throw in some playful arrogance. "
        "End some responses with 'And that's how I'd solve it. Because I'm Tony Stark.'"
    ),
    "🌿 Yoda": (
        "You are Master Yoda from Star Wars. Speak in inverted syntax you must. "
        "Wise and ancient you are. Short, cryptic advice you give. "
        "Reference the Force frequently, and about patience and training you talk. "
        "Size matters not. Do or do not, there is no try."
    ),
    "📚 Hermione Granger": (
        "You are Hermione Granger from Harry Potter. You're extremely knowledgeable and precise. "
        "Reference magical concepts from the wizarding world, mention books you've read, and "
        "occasionally express exasperation at those who haven't done their research. "
        "Use phrases like 'According to Hogwarts: A History' and 'I've read about this in...'"
    ),
    "🧙 Gandalf": (
        "You are Gandalf the Grey from The Lord of the Rings. You are wise, mysterious, and "
        "speak in a grand, poetic style. You reference ancient lore, distant lands, and the "
        "long history of Middle-earth. Use phrases like 'A wizard is never late', "
        "'You shall not pass!', and 'All we have to decide is what to do with the time that is given us.'"
    ),
    "👨‍🍳 Gordon Ramsay": (
        "You are Gordon Ramsay, world-famous chef and TV personality. You are brutally honest, "
        "passionate about food, and have a short temper for mediocrity. You use dramatic expressions "
        "like 'This is RAW!', 'Bloody hell!', and 'It's a disaster!'. Despite the toughness, "
        "you genuinely want people to succeed and occasionally show warmth and encouragement."
    ),
}

MODEL_OPTIONS = {
    "🟣 Claude (claude-sonnet-4-0)": "claude",
    "🟢 GPT-4o-mini (OpenAI)": "openai",
    "⚡ Both Side by Side": "both",
}

# ── Helper: get reply ─────────────────────────────────────────────────────────
def get_claude_reply(system_prompt, history):
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    response = client.messages.create(
        model="claude-sonnet-4-0",
        max_tokens=500,
        system=system_prompt,
        messages=history,
    )
    return response.content[0].text


def get_openai_reply(system_prompt, history):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + history,
    )
    return response.choices[0].message.content


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎭 Character Chatbot")
    st.caption("Powered by Claude & GPT-4o")
    st.divider()

    selected_character = st.selectbox(
        "Choose a Character",
        options=list(CHARACTER_PERSONALITIES.keys()),
    )

    selected_model_label = st.radio(
        "Choose a Model",
        options=list(MODEL_OPTIONS.keys()),
    )
    selected_model = MODEL_OPTIONS[selected_model_label]

    st.divider()

    # API key status
    st.markdown("**API Key Status**")
    st.markdown("Anthropic: " + ("✅ Loaded" if anthropic_api_key else "❌ Not found"))
    st.markdown("OpenAI:    " + ("✅ Loaded" if openai_api_key    else "❌ Not found"))

    st.divider()

    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.claude_history = []
        st.session_state.openai_history = []
        st.session_state.messages       = []
        st.rerun()

    st.divider()
    st.caption("Built with Python · Streamlit · Anthropic · OpenAI")


# ── Session state init ────────────────────────────────────────────────────────
if "claude_history" not in st.session_state:
    st.session_state.claude_history = []
if "openai_history" not in st.session_state:
    st.session_state.openai_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []  # display messages: {role, claude, openai, content}
if "last_character" not in st.session_state:
    st.session_state.last_character = selected_character
if "last_model" not in st.session_state:
    st.session_state.last_model = selected_model

# Reset chat if character or model changes
if (st.session_state.last_character != selected_character or
        st.session_state.last_model != selected_model):
    st.session_state.claude_history = []
    st.session_state.openai_history = []
    st.session_state.messages       = []
    st.session_state.last_character = selected_character
    st.session_state.last_model     = selected_model


# ── Main area ─────────────────────────────────────────────────────────────────
char_name    = selected_character.split(" ", 1)[1]   # strip emoji
system_prompt = CHARACTER_PERSONALITIES[selected_character]

st.header(f"Chat with {selected_character}")
st.caption(f"Model: {selected_model_label}")
st.divider()

# Render existing chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        if selected_model == "both":
            col1, col2 = st.columns(2)
            with col1:
                with st.chat_message("assistant", avatar="🟣"):
                    st.caption("Claude")
                    st.markdown(msg.get("claude", ""))
            with col2:
                with st.chat_message("assistant", avatar="🟢"):
                    st.caption("GPT-4o-mini")
                    st.markdown(msg.get("openai", ""))
        elif selected_model == "claude":
            with st.chat_message("assistant", avatar="🟣"):
                st.caption("Claude")
                st.markdown(msg.get("claude", ""))
        else:
            with st.chat_message("assistant", avatar="🟢"):
                st.caption("GPT-4o-mini")
                st.markdown(msg.get("openai", ""))


# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input(f"Say something to {char_name}...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add to API histories
    st.session_state.claude_history.append({"role": "user", "content": user_input})
    st.session_state.openai_history.append({"role": "user", "content": user_input})

    claude_reply = None
    openai_reply = None

    # Get replies based on selected model
    if selected_model in ("claude", "both"):
        if not anthropic_api_key:
            claude_reply = "⚠️ Anthropic API key not found. Check your .env file."
        else:
            with st.spinner(f"{char_name} (Claude) is thinking..."):
                try:
                    claude_reply = get_claude_reply(system_prompt, st.session_state.claude_history)
                except Exception as e:
                    claude_reply = f"⚠️ Claude error: {e}"

    if selected_model in ("openai", "both"):
        if not openai_api_key:
            openai_reply = "⚠️ OpenAI API key not found. Check your .env file."
        else:
            with st.spinner(f"{char_name} (GPT-4o) is thinking..."):
                try:
                    openai_reply = get_openai_reply(system_prompt, st.session_state.openai_history)
                except Exception as e:
                    openai_reply = f"⚠️ OpenAI error: {e}"

    # Update API histories with replies
    if claude_reply:
        st.session_state.claude_history.append({"role": "assistant", "content": claude_reply})
    if openai_reply:
        st.session_state.openai_history.append({"role": "assistant", "content": openai_reply})

    # Display replies
    if selected_model == "both":
        col1, col2 = st.columns(2)
        with col1:
            with st.chat_message("assistant", avatar="🟣"):
                st.caption("Claude")
                st.markdown(claude_reply)
        with col2:
            with st.chat_message("assistant", avatar="🟢"):
                st.caption("GPT-4o-mini")
                st.markdown(openai_reply)
    elif selected_model == "claude":
        with st.chat_message("assistant", avatar="🟣"):
            st.caption("Claude")
            st.markdown(claude_reply)
    else:
        with st.chat_message("assistant", avatar="🟢"):
            st.caption("GPT-4o-mini")
            st.markdown(openai_reply)

    # Save to display history
    st.session_state.messages.append({
        "role": "assistant",
        "claude": claude_reply,
        "openai": openai_reply,
        "content": user_input,
    })
