import io
import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
from knight_engine import ChivalryTranslator

# Load static ffmpeg paths for pydub
import static_ffmpeg
static_ffmpeg.add_paths()

# Configure the Streamlit page
st.set_page_config(
    page_title="Knightly Bot 🛡️",
    page_icon="⚔️",
    layout="centered"
)

# Custom Knightly / Medieval theme styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #d97706;
            font-family: Georgia, serif;
            font-size: 2.4rem;
            margin-bottom: 0px;
        }
        .sub-caption {
            text-align: center;
            color: #9ca3af;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        .chivalric-box {
            background-color: #1f2937;
            border-left: 5px solid #d97706;
            padding: 1.2rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-size: 1.15rem;
            color: #f3f4f6;
            font-style: italic;
        }
        .about-card {
            background-color: #111827;
            border: 1px solid #374151;
            padding: 1.2rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛡️ Knightly Bot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-caption">Prithee, speak or pen thy words, and receive courteous proclamation.</p>', unsafe_allow_html=True)

# Initialize the translation engine
@st.cache_resource
def load_translator():
    return ChivalryTranslator()

translator = load_translator()

# Navigation tabs: Scribe, Herald, and About
tab_text, tab_voice, tab_about = st.tabs([
    "📜 Scribe (Text Mode)", 
    "🎙️ Herald (Voice Mode)", 
    "🏰 About & Codex"
])

# -----------------------------------------------------------
# TAB 1: TEXT MODE
# -----------------------------------------------------------
with tab_text:
    st.subheader("Compose Thy Message")
    user_input = st.text_input(
        "Enter modern phrasing below:",
        placeholder="e.g., how the hell is this wrong, you're an idiot",
        key="text_input_box"
    )

    if st.button("Translate to Chivalric English", type="primary", use_container_width=True):
        if user_input.strip():
            translated = translator.transform(user_input)
            st.markdown("#### Courtly Proclamation:")
            st.markdown(f'<div class="chivalric-box">"{translated}"</div>', unsafe_allow_html=True)
        else:
            st.warning("Prithee, supply some text first.")

# -----------------------------------------------------------
# TAB 2: VOICE MODE (Direct Browser Microphone)
# -----------------------------------------------------------
with tab_voice:
    st.subheader("Speak into the Royal Horn")
    st.write("Click below to record your voice directly from the browser:")

    audio_record = mic_recorder(
        start_prompt="🎙️ Start Speaking",
        stop_prompt="🛑 Stop & Translate",
        key="knightly_mic"
    )

    if audio_record:
        raw_audio_bytes = audio_record['bytes']
        st.audio(raw_audio_bytes)

        recognizer = sr.Recognizer()
        try:
            # Convert incoming audio to 16-bit PCM WAV using pydub
            raw_buffer = io.BytesIO(raw_audio_bytes)
            sound = AudioSegment.from_file(raw_buffer)
            
            wav_buffer = io.BytesIO()
            sound.export(wav_buffer, format="wav")
            wav_buffer.seek(0)

            with sr.AudioFile(wav_buffer) as source:
                audio_data = recognizer.record(source)
                with st.spinner("Deciphering thy speech..."):
                    transcript = recognizer.recognize_google(audio_data)

            st.info(f"**Transcribed Speech:** \"{transcript}\"")

            translated = translator.transform(transcript)
            st.markdown("#### Courtly Proclamation:")
            st.markdown(f'<div class="chivalric-box">"{translated}"</div>', unsafe_allow_html=True)

        except sr.UnknownValueError:
            st.error("⚠️ Thy speech could not be discerned by the herald. Pray speak clearer.")
        except Exception as e:
            st.error(f"⚠️ An unexpected mishap occurred: {e}")

# -----------------------------------------------------------
# TAB 3: ABOUT & CODEX
# -----------------------------------------------------------
with tab_about:
    st.subheader("The Knightly Codex")
    
    st.markdown("""
    <div class="about-card">
        <h4>⚔️ What is Knightly Bot?</h4>
        <p><strong>Knightly Bot</strong> is an automated politeness filter that intercepts discourteous modern phrasing, slang, and curses, transforming them into noble Old and Early Modern English proclamation.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🛠️ Architecture**
        - **Engine:** Deterministic NLP & regex phrase-matching.
        - **Grammar Layer:** Second-person pronoun & copula transduction (`you` → `thou`, `your` → `thy`, `are` → `art`).
        - **Dictionary:** Decoupled JSON lookup repository for scalable vocabulary expansion.
        """)
    with col2:
        st.markdown("""
        **🎙️ Audio & Voice Stack**
        - **Ingestion:** Browser WebRTC stream via `streamlit-mic-recorder`.
        - **Decoding:** Audio stream normalization using `pydub` & `ffmpeg`.
        - **STT Engine:** Google Speech Recognition acoustic transcription.
        """)

    st.markdown("---")
    st.markdown("#### 📜 Courtly Vocabulary Reference")
    
    st.dataframe(
        [
            {"Modern Phrasing": "Shut up!", "Knightly Equivalent": "Prithee, still thy tongue, good sir."},
            {"Modern Phrasing": "How the hell is this wrong", "Knightly Equivalent": "How in Heaven's name is this in error"},
            {"Modern Phrasing": "You're an idiot", "Knightly Equivalent": "Thou art a simpleton"},
            {"Modern Phrasing": "This sucks", "Knightly Equivalent": "Verily, this displeaseth me greatly"},
            {"Modern Phrasing": "Damn it", "Knightly Equivalent": "Fie upon it!"},
        ],
        use_container_width=True
    )