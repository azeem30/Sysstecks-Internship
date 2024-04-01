import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for themed widgets
from internship.task1.pdf_generator import generate_pdf


class RegistrationApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Registration Application")
        self.master.configure(bg="white")  # Set background color to pure white

        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.aicte = tk.StringVar()
        self.address = tk.StringVar()  # New variable for address
        self.college = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Custom Style for Entry Fields
        style = ttk.Style()
        style.theme_use("clam")  # Use the "clam" theme for ttk widgets
        style.configure("Custom.TEntry", borderwidth=0, relief="solid", corner=5)  # Rounded corners

        # Custom Style for Submit Button
        style.configure("Custom.TButton", padding=(10, 5))
        style.map("Custom.TButton",
                  background=[("active", "black"), ("pressed", "!disabled", "black")],
                  foreground=[("active", "white"), ("pressed", "!disabled", "white")],
                  relief=[("pressed", "sunken")])

        # Name Label and Input
        tk.Label(self.master, text="Name:", bg="white", fg="black").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self.master, textvariable=self.name, width=40, style="Custom.TEntry")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Error Label for Name
        self.name_error = tk.Label(self.master, text="", fg="red", bg="white")
        self.name_error.grid(row=1, column=1, sticky="w")

        # AICTE Label and Input
        tk.Label(self.master, text="AICTE:", bg="white", fg="black").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.aicte_entry = ttk.Entry(self.master, textvariable=self.aicte, width=40, style="Custom.TEntry")
        self.aicte_entry.grid(row=2, column=1, padx=10, pady=5)

        # Error Label for AICTE
        self.aicte_error = tk.Label(self.master, text="", fg="red", bg="white")
        self.aicte_error.grid(row=3, column=1, sticky="w")

        # Email Label and Input
        tk.Label(self.master, text="Email:", bg="white", fg="black").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self.master, textvariable=self.email, width=40, style="Custom.TEntry")
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Error Label for Email
        self.email_error = tk.Label(self.master, text="", fg="red", bg="white")
        self.email_error.grid(row=5, column=1, sticky="w")

        # Phone Label and Input
        tk.Label(self.master, text="Phone:", bg="white", fg="black").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(self.master, textvariable=self.phone, width=40, style="Custom.TEntry")
        self.phone_entry.grid(row=6, column=1, padx=10, pady=5)

        # Error Label for Phone
        self.phone_error = tk.Label(self.master, text="", fg="red", bg="white")
        self.phone_error.grid(row=7, column=1, sticky="w")

        # Address Label and Input (Multiline Entry)
        tk.Label(self.master, text="Address:", bg="white", fg="black").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.address_entry = tk.Text(self.master, width=40, height=5, bg="white", fg="black", wrap="word")
        self.address_entry.grid(row=8, column=1, padx=10, pady=5)

        # College Name Label and Input
        tk.Label(self.master, text="College:", bg="white", fg="black").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.college_entry = ttk.Entry(self.master, textvariable=self.college, width=70, style="Custom.TEntry")
        self.college_entry.grid(row=10, column=1, padx=10, pady=5)

        # Error Label for College
        self.college_error = tk.Label(self.master, text="", fg="red", bg="white")
        self.college_error.grid(row=11, column=1, sticky="w")

        # Submit Button
        ttk.Button(self.master, text="Submit", command=self.submit_form, style="Custom.TButton").grid(row=12, columnspan=2, pady=10)

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

        if self.aicte.get() == "":
            self.aicte_error.config(text="AICTE ID cannot be empty")
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

    def submit_form(self):
        self.clear_errors()
        if not self.validate_data():
            return
        generate_pdf(
            self.name.get(),
            self.aicte.get(),
            self.email.get(),
            self.phone.get(),
            self.address_entry.get("1.0", "end-1c"),
            self.college.get()
        )
        messagebox.showinfo("Success", "Form Submitted Successfully!")
        self.clear_form()

    def clear_form(self):
        # Clear all input fields in the form
        self.name.set("")
        self.aicte.set("")
        self.email.set("")
        self.phone.set("")
        self.address_entry.delete("1.0", "end")  # Clear address entry
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
