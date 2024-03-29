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
        self.aicte = tk.StringVar()
        self.college = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Name Label and Input
        tk.Label(self.master, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.master, textvariable=self.name, width=40)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Error Label for Name
        self.name_error = tk.Label(self.master, text="", fg="red")
        self.name_error.grid(row=1, column=1, sticky="w")

        # AICTE Label and Input
        tk.Label(self.master, text="AICTE:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.aicte_entry = tk.Entry(self.master, textvariable=self.aicte, width=40)
        self.aicte_entry.grid(row=2, column=1, padx=10, pady=5)

        # Error Label for AICTE
        self.aicte_error = tk.Label(self.master, text="", fg="red")
        self.aicte_error.grid(row=3, column=1, sticky="w")

        # Email Label and Input
        tk.Label(self.master, text="Email:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(self.master, textvariable=self.email, width=40)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Error Label for Email
        self.email_error = tk.Label(self.master, text="", fg="red")
        self.email_error.grid(row=5, column=1, sticky="w")

        # Phone Label and Input
        tk.Label(self.master, text="Phone:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = tk.Entry(self.master, textvariable=self.phone, width=40)
        self.phone_entry.grid(row=6, column=1, padx=10, pady=5,)

        # Error Label for Phone
        self.phone_error = tk.Label(self.master, text="", fg="red")
        self.phone_error.grid(row=7, column=1, sticky="w")

        # College Name Label and Input
        tk.Label(self.master, text="College:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.college_entry = tk.Entry(self.master, textvariable=self.college, width=70)
        self.college_entry.grid(row=8, column=1, padx=10, pady=5)

        # Error Label for College
        self.college_error = tk.Label(self.master, text="", fg="red")
        self.college_error.grid(row=9, column=1, sticky="w")

        # Submit Button
        tk.Button(self.master, text="Submit", command=self.submit_form, width=20).grid(row=11, columnspan=2, pady=10)

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
        # Create a PDF with user's name as part of the filename
        # Create a PDF with user's name as part of the filename
        filename = f"{self.aicte.get()}_registration_form.pdf"
        c = canvas.Canvas(filename, pagesize=letter)

        # Heading
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, 750, "Registration Form")

        # Divider below heading
        c.line(50, 740, 550, 740)

        # Write data to PDF
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, "Name: ")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(90, 720, self.name.get())
        c.setFont("Helvetica", 12)

        c.drawString(50, 700, "AICTE ID: ")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(110, 700, self.aicte.get())
        c.setFont("Helvetica", 12)

        c.drawString(50, 680, "Email: ")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(90, 680, self.email.get())
        c.setFont("Helvetica", 12)

        c.drawString(50, 660, "Phone: ")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(90, 660, self.phone.get())
        c.setFont("Helvetica", 12)

        c.drawString(50, 640, "College: ")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 640, self.college.get())
        c.setFont("Helvetica", 12)

        # Divider for footer
        c.line(50, 50, 550, 50)

        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 30, "Systecks IT Solutions")

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
        self.aicte.set("")
        self.email.set("")
        self.phone.set("")
        self.college.set("")
        self.clear_errors()

    def clear_errors(self):
        # Clear all error messages
        self.name_error.config(text="")
        self.aicte_error.config(text="")
        self.email_error.config(text="")
        self.phone_error.config(text="")
        self.college_error.config(text="")


def main():
    root = tk.Tk()
    RegistrationApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

