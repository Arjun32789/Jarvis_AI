import speech_recognition as sr

print("=" * 50)
print("MICROPHONE TEST")
print("=" * 50)

# Saare mics ki list dikhao
print("\nAvailable microphones:")
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"  [{i}] {name}")

print("\n" + "=" * 50)

# Har mic ko test karo
r = sr.Recognizer()

for index in [1, 2, 6, 11]:
    try:
        print(f"\n🎤 Testing index {index}...")
        with sr.Microphone(device_index=index) as source:
            r.energy_threshold = 100
            r.dynamic_energy_threshold = False
            print(f"   Name: {sr.Microphone.list_microphone_names()[index]}")
            print("   Bolo 'Hello' 4 sec mein...")
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
        
        try:
            text = r.recognize_google(audio)
            print(f"   ✅ SUCCESS! Suna: '{text}'")
            print(f"   👉 USE MIC_INDEX = {index}")
        except sr.UnknownValueError:
            print(f"   ❓ Suna par samjha nahi (awaaz dheemi?)")
        except sr.RequestError as e:
            print(f"   ⚠️ Internet error: {e}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

print("\n" + "=" * 50)
print("Test complete. Best index upar ✅ wala hai.")