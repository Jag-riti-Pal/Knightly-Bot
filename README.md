# 🛡️ Knightly Bot: Chivalric Politeness Filter

> **A real-time speech and text filter converting modern discourteous language into noble Early Modern English proclamation.**

---

## 📌 Executive Summary
**Knightly Bot** intercepts modern rude phrasing, profanity, and informal slang, translating them into courteous, Old and Early Modern English speech. The system combines deterministic multi-word regex phrase mapping, lexical substitution, grammatical pronoun/copula transduction, and browser-level speech ingestion into an interactive Streamlit application.

---

## 🏗️ System Architecture

```text
[ Browser Client ]
       │
       ├── Text Mode ──────────────┐
       │                           │
       └── Audio Mode (WebRTC)     ▼
                 │        [ ChivalryTranslator Engine ]
                 ▼        ├── 1. Phrase Mapping (JSON lookup)
        [ PCM Conversion ] ├── 2. Vocabulary Normalization
        (pydub + ffmpeg)  ├── 3. Pronoun Transduction (thou/thy/art)
                 │        └── 4. Capitalization & Punctuation
                 ▼                 │
        [ Google STT Engine ] ─────┘
                                   │
                                   ▼
                       [ Courtly Proclamation HUD ]
```
---

## 💡 Core Features
* Multi-Tier Rule Transduction: High-priority phrase lookup prevents broken partial substitutions before single-word vocabulary replacement.

* Deterministic Grammar Adaptation: Maps second-person pronouns and archaic auxiliary verbs (you → thou, your → thy, are → art, don't → dost not).

* Decoupled Dictionary: Phrases and vocabulary live in data/dictionary.json, allowing dictionary expansion without code edits or model training.

* Dual Ingestion (Text & Voice): Type directly or speak through the browser horn with automatic WebM-to-PCM conversion and Google Speech Recognition transcription.

---

## 🚀 Quickstart Guide
### 1. Clone & Set Up Virtual Environment
```Bash
git clone [https://github.com/](https://github.com/)<your-username>/Knightly-Bot.git
cd Knightly-Bot

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```
### 2. Install Dependencies
```Bash
pip install -r requirements.txt
```
### 3. Launch the Web Interface
```Bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.