import os
import threading
from tkinter import *
from tkinter import filedialog, messagebox
import sqlite3
import socket
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


root = Tk()
root.title("Share")
root.geometry("500x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

conn = sqlite3.connect('sysstecks.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)''')
conn.commit()

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_file(key, filename, output_filename):
    with open(filename, 'rb') as f:
        plaintext = f.read()

    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    with open(output_filename, 'wb') as f:
        f.write(ciphertext)

def decrypt_file(key, filename, output_filename):
    with open(filename, 'rb') as f:
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(output_filename, 'wb') as f:
        f.write(plaintext)

def register_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def authenticate_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password_hash))
    if c.fetchone():
        return True
    else:
        return False

def Register():
    def register_attempt():
        user = new_username_entry.get()
        pwd = new_password_entry.get()
        register_user(user, pwd)
        register_window.destroy()

    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.geometry("250x140")
    register_window.configure(bg="#f4fdfe")
    register_window.resizable(False, False)

    register_icon = PhotoImage(file="icons/register.png")
    register_window.iconphoto(False, register_icon)

    Label(register_window, text="Username", bg="#f4fdfe").grid(row=0, column=0, padx=10, pady=10)
    Label(register_window, text="Password", bg="#f4fdfe").grid(row=1, column=0, padx=10, pady=10)

    new_username_entry = Entry(register_window, width=20)
    new_username_entry.grid(row=0, column=1, padx=10, pady=10)
    new_password_entry = Entry(register_window, width=20, show="*")
    new_password_entry.grid(row=1, column=1, padx=10, pady=10)

    register_button = Button(register_window, text="Register", command=register_attempt)
    register_button.grid(row=2, columnspan=2, padx=10, pady=10)

def Login():
    def login_attempt():
        user = username_entry.get()
        pwd = password_entry.get()
        if authenticate_user(user, pwd):
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            send.config(state=NORMAL)
            receive.config(state=NORMAL)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("250x140")
    login_window.configure(bg="#f4fdfe")
    login_window.resizable(False, False)

    login_icon = PhotoImage(file="icons/login.png")
    login_window.iconphoto(False, login_icon)

    Label(login_window, text="Username", bg="#f4fdfe").grid(row=0, column=0, padx=10, pady=10)
    Label(login_window, text="Password", bg="#f4fdfe").grid(row=1, column=0, padx=10, pady=10)

    username_entry = Entry(login_window, width=20)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry = Entry(login_window, width=20, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = Button(login_window, text="Login", command=login_attempt)
    login_button.grid(row=2, columnspan=2, padx=10, pady=10)

def Send():
    window = Toplevel(root)
    window.title("Send")
    window.geometry("450x560+500+200")
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetype=(('file_type', '*.txt'), ('all files', '*.*')))

    def send_file():
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print('Waiting for connections')
        conn, address = s.accept()
        encrypt_file(key, filename, filename)
        with open(filename, 'rb') as f:
            file_data = f.read(1024)
            while file_data:
                conn.send(file_data)
                file_data = f.read(1024)
        conn.close()
        print("File sent successfully!")

    def sender():
        thread = threading.Thread(target=send_file)
        thread.start()

    window_icon = PhotoImage(file="icons/send.png")
    window.iconphoto(False, window_icon)

    send_background = PhotoImage(file="icons/send_background.png")
    Label(window, image=send_background).place(x=-2, y=0, relwidth=1)

    main_background = PhotoImage(file="icons/main_background.png")
    Label(window, image=main_background, bg="#f4fdfe").place(x=100, y=260)

    host = socket.gethostname()
    Label(window,text=f"ID: {host}", bg='white', fg='black').place(x=140, y=290)

    Button(window, text="+ Select File", width=10, height=1, font='arial 14 bold', bg="#fff", fg="#000", command=select_file).place(x=160, y=150)
    Button(window, text="Send", width=8, height=1, font='arial 14 bold', bg="#000", fg="#fff", command=sender).place(x=300, y=150)

    window.mainloop()

def Receive():
    window = Toplevel(root)
    window.title("Receive")
    window.geometry("450x560+500+200")
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def receiver():
        id = sender_id.get()
        filename_dup = file_name.get()
        s = socket.socket()
        port = 8080
        s.connect((id, port))
        with open(filename_dup, 'wb') as f:
            while True:
                file_data = s.recv(1024)
                if not file_data:
                    break
                f.write(file_data)
        s.close()
        decrypt_file(key, filename_dup, filename_dup)
        print("File Received and Decrypted Successfully!")

    window_icon = PhotoImage(file="icons/receive.png")
    window.iconphoto(False, window_icon)

    receive_background = PhotoImage(file="icons/receive_background.png").subsample(2)
    Label(window, image=receive_background).place(x=-2, y=0)

    receive_main_background = PhotoImage(file="icons/avatar.png").subsample(2)
    Label(window, image=receive_main_background).place(x=190, y=390)

    Label(window, text="Receive", font=('arial', 17), bg="#f4fdfe").place(x=20, y=280)
    Label(window, text="Input Sender ID", font=('arial', 17), bg="#f4fdfe").place(x=20, y=310)
    sender_id = Entry(window, width=20, fg='black', border=2, bg='white', font=('arial', 15))
    sender_id.place(x=184, y=310)
    sender_id.focus()

    Label(window, text="Filename", font=('arial', 17), bg="#f4fdfe").place(x=20, y=340)
    file_name = Entry(window, width=20, fg='black', border=2, bg='white', font=('arial', 15))
    file_name.place(x=124, y=340)

    download = PhotoImage(file="icons/receive.png").subsample(5)
    download_button = Button(window, image=download, compound=LEFT, text='Receive', width=130, bg="#39c790", font='arial 14 bold', command=receiver)
    download_button.place(x=20, y=380)

    window.mainloop()

password = b'ThisIsMyPasswordPleaseDoNotShare'
salt = b'ThisIsMySalt'
key = generate_key(password, salt)

icon = PhotoImage(file="icons/share.png")
root.iconphoto(False, icon)

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send_icon = PhotoImage(file="icons/send.png").subsample(17)  # Resizes the image by a factor of 2
send = Button(root, image=send_icon, bg="#f4fdfe", bd=0, state=DISABLED, command=Send)
send.place(x=50, y=95)

register_icon = PhotoImage(file="icons/register.png").subsample(3)  # Resizes the image by a factor of 2
register_button = Button(root, image=register_icon, bg="#f4fdfe", bd=0, command=Register)
register_button.place(x=170, y=100)

login_icon = PhotoImage(file="icons/login.png").subsample(3)  # Resizes the image by a factor of 2
login_button = Button(root, image=login_icon, bg="#f4fdfe", bd=0, command=Login)
login_button.place(x=270, y=98)

receive_icon = PhotoImage(file="icons/receive.png").subsample(3)  # Resizes the image by a factor of 2
receive = Button(root, image=receive_icon, bg="#f4fdfe", bd=0, state=DISABLED, command=Receive)
receive.place(x=370, y=100)


Label(root, text="Send", font=('Acumin Variable Concept', 14), bg="#f4fdfe").place(x=70, y=190)
Label(root, text="Register", font=('Acumin Variable Concept', 14), bg="#f4fdfe").place(x=170, y=190)
Label(root, text="Login", font=('Acumin Variable Concept', 14), bg="#f4fdfe").place(x=278, y=190)
Label(root, text="Receive", font=('Acumin Variable Concept', 14), bg="#f4fdfe").place(x=370, y=190)

background = PhotoImage(file="icons/background.png")
Label(root, image=background).place(x=-2, y=323, relwidth=1, relheight=0.43)

root.mainloop()