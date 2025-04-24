import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import customtkinter as ctk

# Initialize the voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Evaluate the expression
def calculate(expression):
    try:
        result = str(eval(expression))
        return result
    except:
        return "Error"

# Recognize voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Speak now")
        status_label.configure(text="Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            input_entry.delete(0, tk.END)
            input_entry.insert(0, text)
            result = calculate(text)
            result_label.configure(text=f"Answer: {result}")
            speak(f"The answer is {result}")
        except sr.UnknownValueError:
            result_label.configure(text="Sorry, I didn't catch that.")
        except sr.RequestError:
            result_label.configure(text="Could not connect to service.")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")
        status_label.configure(text="")

# Start recognition in a separate thread
def start_voice_thread():
    threading.Thread(target=recognize_speech).start()

# GUI Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("400x400")
app.title("🎙️ Voice Calculator")

input_entry = ctk.CTkEntry(app, placeholder_text="Speak or type expression...", width=300, height=40, font=("Arial", 16))
input_entry.pack(pady=20)

mic_button = ctk.CTkButton(app, text="🎤 Speak", command=start_voice_thread, width=150, height=40, font=("Arial", 14))
mic_button.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 18))
result_label.pack(pady=20)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 12), text_color="gray")
status_label.pack()

# Run the app
app.mainloop()