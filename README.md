# TA_chatbot
This is a simple chatbot that answers questions based on your class lecture PDFs.

## Python Version
- Python 3.12.7

---

## Setup Instructions

1. Create and activate a Mac virtual environment:
```bash
python3 -m venv venv # on Windows (Command Prompt): python -m venv venv
source venv/bin/activate # on Windows (Command Prompt): venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Make sure your lecture slides are inside a folder named `data/` in the same folder as your code.

---

## Run the Chatbot
```bash
./venv/bin/streamlit run app.py 
# on Windows (Command Prompt): venv\Scripts\streamlit run app.py
```

This will open the chatbot in your web browser in about 30 seconds.

---

## Files in the Project
- `app.py`: Chatbot user interface
- `main.py`: Backend logic that finds answers
- `utils.py`: PDF text extraction and splitting
- `requirements.txt`: List of packages to install
- `data/`: Folder where your lecture PDFs go

---

Made by:
- Shrujal Mogadati
- Disha Srinivasa
- Kavya Avula
