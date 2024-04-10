import os
import threading
from tkinter import *
from tkinter import filedialog, messagebox
import socket

root = Tk()
root.title("Share")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

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
        file = open(filename, 'rb')
        file_data = file.read(1024)
        while file_data:
            conn.send(file_data)
            file_data = file.read(1024)
        file.close()
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
        file = open(filename_dup, 'wb')
        file_data = s.recv(1024)
        file.write(file_data)
        file.close()
        print("File Received Successfully!")

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

icon = PhotoImage(file="icons/share.png")
root.iconphoto(False, icon)

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send_icon = PhotoImage(file="icons/send.png").subsample(17)  # Resizes the image by a factor of 2
send = Button(root, image=send_icon, bg="#f4fdfe", bd=0, command=Send)
send.place(x=50, y=95)

receive_icon = PhotoImage(file="icons/receive.png").subsample(3)  # Resizes the image by a factor of 2
receive = Button(root, image=receive_icon, bg="#f4fdfe", bd=0, command=Receive)
receive.place(x=300, y=100)

Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=55, y=190)
Label(root, text="Receive", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=295, y=190)

background = PhotoImage(file="icons/background.png")
Label(root, image=background).place(x=-2, y=323, relwidth=1, relheight=0.43)

root.mainloop()