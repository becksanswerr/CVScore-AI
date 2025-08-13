# CVScore AI - Intelligent Resume Analysis & Ranking System

CVScore AI is an intelligent resume analysis tool designed to speed up and optimize recruitment processes. Using AI (Google Gemini), it analyzes uploaded resumes (in PDF or image format) according to specified job descriptions and custom criteria, scores them, ranks them, and provides a detailed report about the candidate.

---

## ✨ Key Features
- **Multi-File Support:** Analyze multiple resumes (PDF, PNG, JPG) simultaneously.  
- **Dynamic Criteria:** Add custom titles, descriptions, and advanced criteria (must-have, nice-to-have, etc.) for each job position.  
- **AI-Powered Analysis:** Deep analysis of each candidate's resume using the Google Gemini 1.5 Flash model.  
- **Smart Scoring:** Assigns a fair and context-aware score between 0-100 based on a predefined scoring guide.  
- **Strengths & Weaknesses:** Automatically lists the candidate's advantages and missing points for the position.  
- **Custom Interview Questions:** Generates specific interview questions targeting the candidate’s missing qualifications.  
- **Candidate Ranking:** Sorts all candidates from highest to lowest score.  
- **User-Friendly Interface:** Built with Streamlit, offering a simple, modern, and interactive web UI.

---


## 🛠️ Technologies Used
- **Frontend:** Streamlit  
- **AI & Language Model:** Google Gemini 2.5 Flash  
- **AI Orchestration:** LangChain  
- **PDF Processing:** PyMuPDF (fitz)  
- **Image Processing (OCR):** Pillow & Google Tesseract  
- **Language:** Python 3.9+  

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.9 or higher:** [Download Python](https://www.python.org/downloads/)  
- **Tesseract OCR Engine:** Required to extract text from image-based resumes.  
  [Tesseract Installation Guide](https://github.com/tesseract-ocr/tesseract)  

---

### Step-by-Step Installation

1. **Clone the Project:**
```bash
git clone https://github.com/your-username/cv-ai-analyzer.git
cd cv-ai-analyzer
```
Create and Activate Virtual Environment (Recommended):

# Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```


# macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
Install Dependencies:
```
```
pip install -r requirements.txt
```

Note: If requirements.txt does not exist, create it with pip freeze > requirements.txt.


# Set Up the API Key:
Create a .env file in the project root directory and add your Google AI Studio Gemini API key:

```bash
GOOGLE_API_KEY="PASTE_YOUR_API_KEY_HERE"
```
IMPORTANT: .env contains sensitive information; never commit it to Git!

# Run the Application:
```bash
streamlit run app.py
```
Open the local web address in your browser to start using the application.


# 📁 Project Structure
```graphql
cv-ai-analyzer/
│
├── lib/
│   ├── __init__.py
│   ├── cv_parser.py        # Extracts raw text from PDF and image resumes
│   └── ai_handler.py       # Manages AI analysis with LangChain and Gemini
│
├── app.py                  # Streamlit UI code
├── requirements.txt        # Python dependencies
├── .env                    # Stores API key (excluded from Git)
└── README.md               # This file
```

# 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.