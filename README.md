
# Dobby: Digital Assignment Automator

**Dobby** is a Python-based tool that automates the process of solving digital assignments. It integrates with Google’s Gemini API to process PDF assignments, extracts content, and generates answers with personalized details (name and registration number). The results are saved into a DOCX file.

## Features

- Upload your Digital Assignment (DA) PDF.
- Automatically process and solve your assignment using the Gemini API.
- Generate a DOCX file with the solution.

## Requirements

- Python 3.9+  
- `google-genai`  
- `docx`  
- `PyPDF2`  
- `tkinter` (for file dialog)  

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/StrongCapybara/Dobby.git
   cd Dobby
   ```

2. **Install dependencies:**

   Install the required libraries using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**

   To use the Gemini API, you will need an API key from Google Cloud.

   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project (or select an existing project).
   - Navigate to **API & Services > Credentials**.
   - Create an **API key**.
   - Store your API key securely and update the `apikey.py` file with your key.

   Example:
   ```python
   APIKEY = "YOUR_API_KEY"
   ```

## Usage

1. Run the script:

   ```bash
   python main.py
   ```

2. The script will prompt you to enter your **name** and **registration number**.
3. A file dialog will open for you to select your **Digital Assignment PDF**.
4. The tool will communicate with Gemini API, process the assignment, and generate a solution.
5. The solution will be saved in a DOCX file with your name and registration number as the filename.

## Example Output

The generated DOCX file will contain the processed assignment with your name and registration number on top, followed by the solved content.
