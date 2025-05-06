from google import genai
from docx import Document
from PyPDF2 import PdfReader
from tkinter import Tk, filedialog
from PIL import Image, ImageDraw, ImageFont
import random
import textwrap
from apikey import APIKEY

# Initialize Gemini client
client = genai.Client(api_key=APIKEY)

# Get user info
userName = input("Enter your name: ").strip()
userRegNo = input("Enter your registration number: ").strip()

print("Please select your Digital Assignment PDF file...")

# File dialog setup
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
pdf_path = filedialog.askopenfilename(
    title="Select your DA PDF file",
    filetypes=[("PDF files", "*.pdf")]
)
root.destroy()

if not pdf_path:
    print("No file selected. Exiting.")
    exit(1)

# Read all pages from PDF
reader = PdfReader(pdf_path)
if len(reader.pages) == 0:
    print("Error: PDF file is empty.")
    exit(1)

# Extract text from all pages
text_from_pdf = ""
for page in reader.pages:
    text_from_pdf += page.extract_text() + "\n\n"

print(f"Successfully extracted text from {len(reader.pages)} pages.")

# Gemini prompt
input2Gemini = (
    f"My name is {userName} and my registration number is {userRegNo}. "
    "Below is my assignment. Please solve the questions. "
    "Do not include any formatting, headings, titles, or introductions. "
    "Just give the solution to the questions only, clearly separated if there are multiple questions.\n\n"
    + text_from_pdf
)

# Gemini API call
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input2Gemini
    )
    outputGemini = response.text
except Exception as e:
    print("Error communicating with Gemini API:", str(e))
    exit(1)

# Save to DOCX
output_filename = f"{userName}_{userRegNo}_DA.docx"
document = Document()
document.add_paragraph(outputGemini)
document.add_page_break()
document.save(output_filename)
print(f"DA saved as DOCX: '{output_filename}'")

# --- Handwritten PDF Generation ---

font_path = "PatrickHand-Regular.ttf"  # Ensure this file is available in the same directory
font_size = 36  # Increased font size for better readability
margin = 80
line_spacing = 30  # Adjusted line spacing
page_width, page_height = 1654, 2339  # A4 at 150 DPI

# Load font
try:
    font = ImageFont.truetype(font_path, font_size)
except Exception as e:
    print("Failed to load font. Make sure PatrickHand-Regular.ttf is in the same folder.")
    exit(1)

# Function to calculate how many pixels wide a string will be
def get_text_width(text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]

# Function to properly wrap text based on pixel width rather than character count
def wrap_text_by_width(text, font, max_width):
    words = text.split()
    if not words:
        return []
    
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        # Check if adding another word would exceed the width
        test_line = current_line + " " + word
        if get_text_width(test_line, font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)  # Add the last line
    return lines

# Calculate the available width for text (adjusted for margins)
available_width = page_width - 2 * margin

# Wrap text with proper width calculation
wrapped_lines = []
for paragraph in outputGemini.split("\n"):
    if paragraph.strip():
        wrapped_lines.extend(wrap_text_by_width(paragraph, font, available_width))
    else:
        wrapped_lines.append("")

# Create pages
pages = []
current_y = margin

# Create new image for the page
img = Image.new("RGB", (page_width, page_height), "white")
draw = ImageDraw.Draw(img)

# Add Name and Reg No to top-right corner (Name on top, Reg No below it)
top_right_margin = 40  # Adjust the margin for name and reg no positioning
name_text = userName
reg_no_text = userRegNo

# Calculate text size using getbbox for both name and registration number
name_bbox = font.getbbox(name_text)
reg_no_bbox = font.getbbox(reg_no_text)

# Adjust space for the name and reg number
name_y = top_right_margin
reg_no_y = top_right_margin + (name_bbox[3] - name_bbox[1])

# Draw the name and registration number
draw.text((page_width - top_right_margin - (name_bbox[2] - name_bbox[0]), name_y), name_text, font=font, fill="black")
draw.text((page_width - top_right_margin - (reg_no_bbox[2] - reg_no_bbox[0]), reg_no_y), reg_no_text, font=font, fill="black")

# Adjust the starting position of the text so that it starts below the name and reg no
current_y = reg_no_y + (reg_no_bbox[3] - reg_no_bbox[1]) + 20  # 20 pixels of spacing after reg no

for line in wrapped_lines:
    if current_y + font_size + line_spacing > page_height - margin:
        pages.append(img)
        img = Image.new("RGB", (page_width, page_height), "white")
        draw = ImageDraw.Draw(img)
        current_y = margin

        # Add Name and Reg No to the new page (again in top-right corner)
        draw.text((page_width - top_right_margin - (name_bbox[2] - name_bbox[0]), name_y), name_text, font=font, fill="black")
        draw.text((page_width - top_right_margin - (reg_no_bbox[2] - reg_no_bbox[0]), reg_no_y), reg_no_text, font=font, fill="black")
        
        # Ensure text starts below the header on subsequent pages
        current_y = reg_no_y + (reg_no_bbox[3] - reg_no_bbox[1]) + 20

    # Add slight random variation to the Y position to simulate imperfect handwriting
    y_offset = random.randint(-2, 2)  # Small random vertical shift
    draw.text((margin, current_y + y_offset), line, font=font, fill="black")
    current_y += font_size + line_spacing

# Add the last page
pages.append(img)

# Save as PDF
pdf_filename = f"{userName}_{userRegNo}_DA_Handwritten.pdf"
pages[0].save(pdf_filename, "PDF", resolution=150.0, save_all=True, append_images=pages[1:])
print(f"Handwritten version saved as PDF: '{pdf_filename}'")
