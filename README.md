# 🎭 LLM Character Chatbot

Chat with iconic fictional characters powered by **Anthropic Claude** and **OpenAI GPT-4o** — built with Python, Streamlit, and prompt engineering.

---

## 🚀 Live Demo

👉 **[Try it here] https://multi-llm-chatbot-ramzai.streamlit.app 

---

## 📌 What Is This?

This project demonstrates how **system prompt engineering** can transform any large language model into a distinct fictional persona. Send the same question to Sherlock Holmes, Tony Stark, Yoda, Hermione Granger, Gandalf, or Gordon Ramsay — each powered by Claude or GPT-4o — and watch how their personalities, speech patterns, and reasoning styles differ dramatically.

It ships as both a **Streamlit web app** (interactive, deployable) and a set of **Jupyter notebooks** (explorable, educational), including a side-by-side model comparison notebook.

---

## ✨ Features

- 🎭 **6 character personas** — each with a carefully engineered system prompt
- 🤖 **Dual LLM support** — Anthropic Claude (claude-sonnet-4-0) and OpenAI (gpt-4o-mini)
- ⚡ **Side-by-side comparison mode** — same question, both models, one screen
- 🧠 **Conversation memory** — full multi-turn history maintained per model
- 🌐 **Streamlit web app** — runs in browser, deployable to Streamlit Cloud
- 📓 **Jupyter notebooks** — step-by-step exploration of both APIs
- 🔐 **Secure key management** — `.env` locally, `st.secrets` on the cloud
- 🎨 **Custom dark theme** — clean UI with colour-coded model panels

---

## 🎭 Characters

| Character | Universe | Personality |
|-----------|----------|-------------|
| 🔍 Sherlock Holmes | Arthur Conan Doyle | Analytical, deductive, Victorian English |
| ⚙️ Tony Stark | Marvel | Sarcastic, genius, pop culture references |
| 🌿 Yoda | Star Wars | Inverted syntax, Force wisdom, cryptic |
| 📚 Hermione Granger | Harry Potter | Precise, book-referencing, exasperated |
| 🧙 Gandalf | Lord of the Rings | Poetic, mysterious, ancient lore |
| 👨‍🍳 Gordon Ramsay | Reality TV | Brutally honest, passionate, dramatic |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Web Framework | Streamlit |
| LLM — Anthropic | `anthropic` SDK · claude-sonnet-4-0 |
| LLM — OpenAI | `openai` SDK · gpt-4o-mini |
| Secret Management | `python-dotenv` · `st.secrets` |
| Notebook UI | Jupyter · `ipywidgets` |
| Architecture | C1–C4 diagrams (Mermaid) |

---

## 🧠 How It Works

```
User Input
    │
    ▼
Character Selected  →  System Prompt Injected
    │                        │
    ▼                        ▼
┌─────────────────────────────────────────────┐
│              API Router                     │
│                                             │
│  🟣 Claude                  🟢 GPT-4o-mini  │
│  system= top-level param    role: system    │
│  claude_history[ ]          openai_history[]│
│  response.content[0].text   choices[0]...  │
└─────────────────────────────────────────────┘
    │                        │
    ▼                        ▼
Claude Reply            OpenAI Reply
    └──────────┬─────────────┘
               ▼
     Side-by-Side Display
```

The key insight: both APIs achieve the same result — persona injection — but with different structures. Claude uses a dedicated `system=` parameter separate from the messages list, while OpenAI uses a `{"role": "system"}` entry inside the messages array. This project demonstrates both patterns cleanly.

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com)
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation

```bash
# Clone the repo
git clone https://github.com/ai-api-playground/multi-llm-chatbot.git
cd multi-llm-chatbot

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env and add your keys
```

### Environment Setup

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Run the Streamlit App

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

### Run the Notebooks

```bash
jupyter notebook
```

---

## 📁 Project Structure

```
multi-llm--chatbot/
│
├── app.py                              # Streamlit web app
├── requirements.txt                    # Dependencies
├── .env                                # API keys (never committed)
├── .gitignore
│
├── .streamlit/
│   ├── config.toml                     # Custom dark theme
│   └── secrets.toml                    # Cloud secrets (never committed)
│
├── CharacterChatbot-Claude.ipynb       # Anthropic API walkthrough
├── CharacterChatbot-OpenAI.ipynb       # OpenAI API walkthrough
├── CharacterChatbot-Comparison.ipynb   # Side-by-side comparison
│
└── docs/
    ├── C1-SystemContext.mermaid        # System context diagram
    ├── C2-Container.mermaid            # Container diagram
    ├── C3-Component.mermaid            # Component diagram
    └── C4-Code.mermaid                 # Code/class diagram
```

---

## 🏗️ Architecture

This project is documented using the **C4 model** — a standard for communicating software architecture at four levels of detail.

| Level | Diagram | Description |
|-------|---------|-------------|
| C1 | [System Context](docs/C1-SystemContext.mermaid) | User, system, and external APIs |
| C2 | [Container](docs/C2-Container.mermaid) | Streamlit app, notebooks, config |
| C3 | [Component](docs/C3-Component.mermaid) | Internal components and data flow |
| C4 | [Code](docs/C4-Code.mermaid) | Functions, classes, and relationships |

---

## ☁️ Deployment

This app is deployed on **Streamlit Community Cloud** (free tier).

To deploy your own instance:

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and select `app.py`
4. Add your API keys under **Advanced Settings → Secrets**:

```toml
ANTHROPIC_API_KEY = "your_key"
OPENAI_API_KEY    = "your_key"
```

5. Hit **Deploy** — live in ~2 minutes

---

## 💡 Key Concepts Demonstrated

- **Prompt Engineering** — Crafting system prompts that reliably produce distinct, consistent character personalities across multiple turns
- **Multi-LLM Integration** — Connecting to two major AI providers in one application and understanding their API differences
- **Conversation Memory** — Maintaining separate per-model message histories for coherent multi-turn dialogue
- **Secure Secrets Management** — Using `.env` locally and `st.secrets` in production — never hardcoding credentials
- **Streamlit Development** — Building an interactive, stateful web application with `st.session_state`
- **Software Architecture** — Documenting a real project using the C4 model

---

## 🔮 What's Next

- [ ] Add streaming responses (token-by-token output)
- [ ] Export conversation as PDF
- [ ] Add voice input/output
- [ ] Support additional LLM providers (Gemini, Mistral)
- [ ] User-defined custom characters

---

## 📄 License

MIT License — free to fork, extend, and build on this project.

---

## 🙋 Author

**Ramz-AI** · [GitHub](https://github.com/ai-api-playground) · [LinkedIn](https://www.linkedin.com/in/ramakanth-reddy-padala/)

> 
