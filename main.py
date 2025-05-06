from google import genai
from docx import Document
from PyPDF2 import PdfReader
from tkinter import Tk, filedialog
from apikey import APIKEY

# Initialize Gemini client
client = genai.Client(api_key=APIKEY)

# Get user info
userName = input("Enter your name: ").strip()
userRegNo = input("Enter your registration number: ").strip()

# Notify user before file selection
print("Please select your Digital Assignment PDF file...")

# Setup file dialog
root = Tk()
root.withdraw()  # Hide root window
root.attributes('-topmost', True)  # Bring dialog to front

pdf_path = filedialog.askopenfilename(
    title="Select your DA PDF file",
    filetypes=[("PDF files", "*.pdf")]
)

root.destroy()

if not pdf_path:
    print("No file selected. Exiting.")
    exit(1)

# Load and read the PDF file
reader = PdfReader(pdf_path)
if len(reader.pages) == 0:
    print("Error: PDF file is empty.")
    exit(1)

page = reader.pages[0]
text_from_pdf = page.extract_text()

# Create prompt for Gemini
input2Gemini = (
    f"My name is {userName}. My registration number is {userRegNo}. "
    "Below is my homework. Put my name and registration number at the top of the assignment and solve it.\n"
    + text_from_pdf
)

# Query Gemini API
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input2Gemini
    )
    outputGemini = response.text
except Exception as e:
    print("Error communicating with Gemini API:", str(e))
    exit(1)

# Save output to a DOCX file
output_filename = f"{userName}_{userRegNo}_DA.docx"
document = Document()
document.add_paragraph(outputGemini)
document.add_page_break()
document.save(output_filename)

print(f"DA executed successfully. File saved as '{output_filename}'")
