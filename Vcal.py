import speech_recognition as sr
import pyttsx3

# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def get_voice_input():
    with sr.Microphone() as source:
        speak("Say your calculation.")
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")

    return ""

def calculate(expression):
    try:
        # Replace words with symbols if needed
        expression = expression.lower().replace("x", "*").replace("plus", "+")\
                                       .replace("minus", "-").replace("into", "*")\
                                       .replace("divided by", "/").replace("by", "/")
        result = eval(expression)
        return result
    except:
        return "Sorry, I couldn't calculate that."

# Main loop
if __name__ == "__main__":
    while True:
        voice_input = get_voice_input()
        if voice_input:
            if "exit" in voice_input.lower():
                speak("Goodbye!")
                break
            result = calculate(voice_input)
            speak(f"The answer is {result}")
