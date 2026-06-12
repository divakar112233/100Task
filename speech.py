import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak now...")
    
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("\n📝 You said:")
    print(text)

except sr.UnknownValueError:
    print("❌ Could not understand audio")

except sr.RequestError:
    print("❌ Internet connection required")