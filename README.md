# Dobby ✍️📄

**Dobby** is your personal Digital Assignment Assistant. It reads your assignment from a PDF, solves it using Google's Gemini AI and exports the solution as both a DOCX file and a **realistic handwritten-style PDF**. Great for students looking to save time without sacrificing presentation.

---

## 🔧 Features

- 📥 Selects and reads questions from your assignment PDF.
- 🤖 Automatically solves the questions using **Gemini (Google GenAI)**.
- 📄 Generates a `.docx` with clean, editable answers.
- ✍️ Outputs a **handwritten-style PDF** using a handwriting font.
- 🧑‍🎓 Adds your name and registration number on each page.

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/dobby.git
cd dobby
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get the handwriting font

Dobby uses the **Patrick Hand** font to simulate handwriting.

#### Option 1: Download manually

- Download `PatrickHand-Regular.ttf` from Google Fonts:
  👉 https://fonts.google.com/specimen/Patrick+Hand
- Click **"Download family"**.
- Extract the `.zip`, and copy `PatrickHand-Regular.ttf` to the root folder of this project.

#### Option 2: Use curl (Linux/macOS)

```bash
curl -o PatrickHand-Regular.ttf https://github.com/google/fonts/raw/main/ofl/patrickhand/PatrickHand-Regular.ttf
```

---

### 4. Add your Gemini API key

Create a file named `apikey.py` in the root directory with the following content:

```python
APIKEY = "your_gemini_api_key_here"
```

---

## 🚀 Usage

```bash
python main.py
```

1. Enter your **name** and **registration number**.
2. Select your **assignment PDF**.
3. Get:
   - `YourName_YourRegNo_DA.docx` – solved answers.
   - `YourName_YourRegNo_DA_Handwritten.pdf` – handwritten-style version.

---

## 🧠 Notes

- All pages of the input PDF are processed.
- Requires an active internet connection for Gemini API.
- Ensure your font file (`PatrickHand-Regular.ttf`) is present in the project directory.

---

## 📜 License

MIT License
