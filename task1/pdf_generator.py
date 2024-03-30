from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(name, aicte, email, phone, address, college):
    filename = f"{aicte}_registration_form.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Registration Form")
    c.line(50, 740, 550, 740)

    # Split the address into lines
    lines = address.split('\n')

    data = [
        ("Name", name),
        ("AICTE ID", aicte),
        ("Email", email),
        ("Phone", phone),
        ("Address", lines),  # Use the lines directly
        ("College", college)
    ]

    y_position = 720
    for label, value in data:
        c.setFont("Helvetica", 12)
        c.drawString(50, y_position, f"{label}: ")
        c.setFont("Helvetica-Bold", 12)
        if label == "Address":
            y_position -= 15  # Adjust vertical position for multi-line address
            for line in value:
                c.drawString(50, y_position, line)
                y_position -= 15
        else:
            c.drawString(110, y_position, value)
        y_position -= 20

    c.line(50, 50, 550, 50)
    c.setFont("Helvetica", 10)
    c.drawString(50, 30, "Systecks IT Solutions")

    c.save()
