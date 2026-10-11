import sys
from knight_engine import ChivalryTranslator
from voice_interface import KnightVoice


def run_text_mode(engine: ChivalryTranslator):
    print("\n--- Knightly Bot: Text Mode ---")
    print("Type your message below (or type 'exit' to quit):\n")
    while True:
        try:
            msg = input("You: ").strip()
            if not msg:
                continue
            if msg.lower() in ["exit", "quit"]:
                print("Knight: Fare thee well!")
                break
            translated = engine.transform(msg)
            print(f"Knightly Bot: {translated}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nKnight: Fare thee well!")
            break


def run_voice_mode(engine: ChivalryTranslator):
    voice = KnightVoice()
    voice.speak("Greetings, traveler. Speak into thy microphone, and I shall make thy words courteous.")

    while True:
        spoken = voice.listen()
        if not spoken:
            continue

        print(f"You said: \"{spoken}\"")
        if spoken.lower().strip() in ["exit", "quit", "farewell"]:
            voice.speak("Fare thee well, good soul!")
            break

        translated = engine.transform(spoken)
        voice.speak(translated)


if __name__ == "__main__":
    translator = ChivalryTranslator()

    print("=== Welcome to Knightly Bot ===")
    print("1. Text Mode (Keyboard Input)")
    print("2. Voice Mode (Microphone Input)")
    choice = input("Select mode (1 or 2): ").strip()

    if choice == "2":
        run_voice_mode(translator)
    else:
        run_text_mode(translator)