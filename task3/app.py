import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
from gtts import gTTS
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

def speak():
    text = text_area.get(1.0, END)
    language = language_combobox.get()
    speed = speed_combobox.get()

    if text:
        tts = gTTS(text=text, lang=language, slow=False if speed=="Fast" else True)
        tts.save("output.mp3")
        os.system("output.mp3")

def download():
    text = text_area.get(1.0, END)
    language = language_combobox.get()
    speed = speed_combobox.get()

    if text:
        tts = gTTS(text=text, lang=language, slow=False if speed=="Fast" else True)
        path = filedialog.askdirectory()
        os.chdir(path)
        tts.save("output.mp3")
        messagebox.showinfo("Success", "File saved successfully")

top_frame = Frame(root, bg="#4CAF50", width=900, height=100)
top_frame.place(x=0, y=0)
mic_logo = PhotoImage(file="icons/mic.png").subsample(17)
Label(top_frame, image=mic_logo, bg="#4CAF50").place(x=10, y=20)
Label(top_frame, text="Text to Speech", font=title_font, bg="#4CAF50", fg="white").place(x=80, y=30)

text_area = Text(root, font=("Roboto", 14), bg="white", fg="black", relief=GROOVE, wrap=WORD)
text_area.place(x=10, y=140, width=500, height=250)

Label(root, text="LANGUAGE", font=label_font, bg="#f0f0f0", fg="black").place(x=550, y=120)

language_combobox = ttk.Combobox(root, values=["en", "fr", "de"], font=label_font, state='readonly', width=10)
language_combobox.place(x=550, y=160)
language_combobox.set('en')

Label(root, text="SPEED", font=label_font, bg="#f0f0f0", fg="black").place(x=740, y=120)

speed_combobox = ttk.Combobox(root, values=["Fast", "Normal"], font=label_font, state='readonly', width=10)
speed_combobox.place(x=740, y=160)
speed_combobox.set('Normal')

speak_icon = PhotoImage(file="icons/speak.png").subsample(17)
btn = Button(root, text="SPEAK", compound=LEFT, image=speak_icon, font=button_font, command=speak)
btn.place(x=550, y=320)

save_icon = PhotoImage(file="icons/save.png").subsample(32)
save = Button(root, text="SAVE", compound=LEFT, image=save_icon, font=button_font, bg="#4CAF50", command=download)
save.place(x=690, y=320)

root.mainloop()
