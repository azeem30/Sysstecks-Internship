import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gtts import gTTS
import threading
import os
import pyttsx3

root = tk.Tk()
root.title("Text to Speech Application")
root.geometry("900x450+200+200")
root.resizable(width=False, height=False)
root.configure(bg="#f0f0f0")

# Fonts
title_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 14)
button_font = ("Helvetica", 14)

def text_to_speech(download=False):
    text = text_area.get(1.0, tk.END)
    language = language_combobox.get()
    speed = speed_combobox.get()
    voice = voice_combobox.get()

    if not text:
        messagebox.showerror("Error", "Please enter some text.")
        return

    if language != 'en':
        tts = gTTS(text=text, lang=language, slow=(speed == "Slow"))
    else:
        engine = pyttsx3.init()
        engine.setProperty('rate', 100 if speed == 'Normal' else 250)
        voices = engine.getProperty('voices')
        voice_id = voices[0].id if voice == 'Male' else voices[1].id
        engine.setProperty('voice', voice_id)
        engine.say(text)
        engine.runAndWait()
        return

    if download:
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if not file_path:
            return
        tts.save(file_path)
        messagebox.showinfo("Success", "File saved successfully")
    else:
        tts.save("output.mp3")
        os.system("output.mp3")
        messagebox.showinfo("Success", "Speech generated successfully")

def speak():
    threading.Thread(target=text_to_speech).start()

def download():
    threading.Thread(target=text_to_speech, kwargs={'download': True}).start()

top_frame = tk.Frame(root, bg="#4CAF50", width=900, height=100)
top_frame.place(x=0, y=0)
mic_logo = tk.PhotoImage(file="icons/mic.png").subsample(17)
tk.Label(top_frame, image=mic_logo, bg="#4CAF50").place(x=10, y=20)
tk.Label(top_frame, text="Text to Speech", font=title_font, bg="#4CAF50", fg="white").place(x=80, y=30)

text_area = tk.Text(root, font=("Roboto", 14), bg="white", fg="black", relief=tk.GROOVE, wrap=tk.WORD)
text_area.place(x=10, y=140, width=500, height=250)

tk.Label(root, text="LANGUAGE", font=label_font, bg="#f0f0f0", fg="black").place(x=550, y=120)

language_combobox = ttk.Combobox(root, values=["en", "fr"], font=label_font, state='readonly', width=10)
language_combobox.place(x=550, y=160)
language_combobox.set('en')

tk.Label(root, text="VOICE", font=label_font, bg="#f0f0f0", fg="black").place(x=550, y=200)

voice_combobox = ttk.Combobox(root, values=["Male", "Female"], font=label_font, state='readonly', width=10)
voice_combobox.place(x=550, y=240)
voice_combobox.set('Male')

tk.Label(root, text="SPEED", font=label_font, bg="#f0f0f0", fg="black").place(x=740, y=120)

speed_combobox = ttk.Combobox(root, values=["Fast", "Normal", "Slow"], font=label_font, state='readonly', width=10)
speed_combobox.place(x=740, y=160)
speed_combobox.set('Normal')

speak_icon = tk.PhotoImage(file="icons/speak.png").subsample(17)
btn = tk.Button(root, text="SPEAK", compound=tk.LEFT, image=speak_icon, font=button_font, command=speak)
btn.place(x=550, y=320)

save_icon = tk.PhotoImage(file="icons/save.png").subsample(32)
save = tk.Button(root, text="SAVE", compound=tk.LEFT, image=save_icon, font=button_font, bg="#4CAF50", command=download)
save.place(x=690, y=320)

root.mainloop()
