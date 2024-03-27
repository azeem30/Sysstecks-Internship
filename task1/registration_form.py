import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class RegistrationApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Registration Application")

        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Name Label and Input
        tk.Label(self.master, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self.master, textvariable=self.name)
        self.name_entry.grid(row=0, column=1)

        # Error Label for Name
        self.name_error = tk.Label(self.master, text="", fg="red")
        self.name_error.grid(row=1, column=1, sticky="w")

        # Email Label and Input
        tk.Label(self.master, text="Email:").grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(self.master, textvariable=self.email)
        self.email_entry.grid(row=2, column=1)

        # Error Label for Email
        self.email_error = tk.Label(self.master, text="", fg="red")
        self.email_error.grid(row=3, column=1, sticky="w")

        # Phone Label and Input
        tk.Label(self.master, text="Phone:").grid(row=4, column=0, sticky="w")
        self.phone_entry = tk.Entry(self.master, textvariable=self.phone)
        self.phone_entry.grid(row=4, column=1)

        # Error Label for Phone
        self.phone_error = tk.Label(self.master, text="", fg="red")
        self.phone_error.grid(row=5, column=1, sticky="w")

        # Submit Button
        tk.Button(self.master, text="Submit", command=self.submit_form).grid(row=10, columnspan=2)

    def validate_data(self):
        valid = True

        if self.name.get() == "":
            self.name_error.config(text="Name cannot be empty")
            valid = False

        if self.email.get() == "":
            self.email_error.config(text="Email cannot be empty")
            valid = False

        if self.phone.get() == "":
            self.phone_error.config(text="Phone cannot be empty")
            valid = False

        if not self.validate_email(self.email.get()):
            self.email_error.config(text="Invalid email format!")
            valid = False

        if not self.validate_phone(self.phone.get()):
            self.phone_error.config(text="Invalid phone format")
            valid = False

        return valid

    def validate_email(self, email):
        if "@" in email and "." in email:
            return True
        else:
            return False

    def validate_phone(self, phone):
        if phone.isdigit() and len(phone) >= 10:
            return True
        else:
            return False

    def generate_pdf(self):
        # Create a PDF
        c = canvas.Canvas("registration_form.pdf", pagesize=letter)

        # Write data to PDF
        c.drawString(100, 750, "Name: " + self.name.get())
        c.drawString(100, 730, "Email: " + self.email.get())
        c.drawString(100, 710, "Phone: " + self.phone.get())

        c.save()

    def submit_form(self):
        self.clear_errors()
        if not self.validate_data():
            return
        self.generate_pdf()
        messagebox.showinfo("Success", "Form Submitted Successfully!")
        self.clear_form()

    def clear_form(self):
        # Clear all input fields in the form
        self.name.set("")
        self.email.set("")
        self.phone.set("")

        self.clear_errors()

    def clear_errors(self):
        # Clear all error messages
        self.name_error.config(text="")
        self.email_error.config(text="")
        self.phone_error.config(text="")


def main():
    root = tk.Tk()
    RegistrationApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

