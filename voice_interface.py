import speech_recognition as sr
import pyttsx3


class KnightVoice:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()

        # Slow down speech rate for a noble, deliberate cadence
        current_rate = self.tts.getProperty("rate")
        self.tts.setProperty("rate", max(120, current_rate - 25))

    def speak(self, text: str):
        print(f"🛡️ Knight says: \"{text}\"")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("\n🎙️ Listening... Speak into the microphone (or say 'exit' to quit):")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("⚡ Translating thy words...")
                return self.recognizer.recognize_google(audio)
            except sr.WaitTimeoutError:
                print("⚠️ Silence lingered too long.")
            except sr.UnknownValueError:
                print("⚠️ Could not discern thy speech.")
            except sr.RequestError as exc:
                print(f"⚠️ Speech service error: {exc}")
            return ""