import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import pyttsx3
import os

root = tk.Tk()
root.title("Text to Speech Application")
root.geometry("900x450+200+200")
root.resizable(width=False, height=False)
root.configure(bg="#f0f0f0")

# Fonts
title_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 14)
button_font = ("Helvetica", 14)

# Create a style
style = ttk.Style()
style.configure('TButton', font=button_font, background="#4CAF50", foreground="white", borderwidth=0, relief="raised")

engine = pyttsx3.init()

def speak():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def set_voice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
            engine.say(text)
            engine.runAndWait()
        else:
            engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()

    if text:
        if speed == 'Fast':
            engine.setProperty('rate', 250)
            set_voice()
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
            set_voice()
        else:
            engine.setProperty('rate', 60)
            set_voice()

def download():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def set_voice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()
        else:
            engine.setProperty('voice', voices[1].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()

    if text:
        if speed == 'Fast':
            engine.setProperty('rate', 250)
            set_voice()
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
            set_voice()
        else:
            engine.setProperty('rate', 60)
            set_voice()
    messagebox.showinfo("Success", "File saved successfully")

top_frame = Frame(root, bg="#4CAF50", width=900, height=100)
top_frame.place(x=0, y=0)
mic_logo = PhotoImage(file="icons/mic.png").subsample(17)
Label(top_frame, image=mic_logo, bg="#4CAF50").place(x=10, y=20)
Label(top_frame, text="Text to Speech", font=title_font, bg="#4CAF50", fg="white").place(x=80, y=30)

text_area = Text(root, font=("Roboto", 14), bg="white", fg="black", relief=GROOVE, wrap=WORD)
text_area.place(x=10, y=140, width=500, height=250)

Label(root, text="VOICE", font=label_font, bg="#f0f0f0", fg="black").place(x=550, y=160)

gender_combobox = Combobox(root, values=["Male", "Female"], font=label_font, state='readonly', width=10)
gender_combobox.place(x=550, y=200)
gender_combobox.set('Male')

Label(root, text="SPEED", font=label_font, bg="#f0f0f0", fg="black").place(x=740, y=160)

speed_combobox = Combobox(root, values=["Fast", "Normal", "Slow"], font=label_font, state='readonly', width=10)
speed_combobox.place(x=740, y=200)
speed_combobox.set('Normal')

speak_icon = PhotoImage(file="icons/speak.png").subsample(17)
btn = Button(root, text="SPEAK", compound=LEFT, image=speak_icon, font=button_font, command=speak)
btn.place(x=550, y=280)

save_icon = PhotoImage(file="icons/save.png").subsample(32)
save = Button(root, text="SAVE", compound=LEFT, image=save_icon, font=button_font, bg="#4CAF50", command=download)
save.place(x=690, y=280)

root.mainloop()