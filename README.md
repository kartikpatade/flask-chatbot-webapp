# Flask Chatbot Web Application

A Flask-based web application featuring an intelligent chatbot designed to assist students and visitors of **SIES (Nerul) College of Arts, Science, and Commerce**. The chatbot uses Natural Language Processing (NLP) and fuzzy string matching to answer common queries related to admissions, courses, facilities, placements, and campus life.


---

## 🚀 Features

- Intelligent intent recognition using fuzzy string matching to handle typos and variations in user queries
- NLP-based text preprocessing using NLTK for better keyword extraction
- Dual user interface:
  - College website–style homepage with an embedded floating chat widget
  - Standalone full-page chatbot interface for focused interaction
- Rich knowledge base capable of answering questions about:
  - Admission timelines (FY 2025–26)
  - Undergraduate and postgraduate courses
  - Campus infrastructure (labs, library, gymkhana)
  - Placements and recruiters
  - Contact information and general college details

---

## 🛠️ Tech Stack

**Backend**
- Python
- Flask

**Frontend**
- HTML5
- CSS3
- JavaScript

**NLP & Logic**
- fuzzywuzzy (string matching)
- python-Levenshtein (performance optimization)
- nltk (tokenization and stop-word removal)

---

## 📂 Project Structure

chatbott2/
- app.py                Main Flask application with routes and chatbot logic  
- requirements.txt      Python dependencies  
- static/  
  - style.css            Styling for chatbot interfaces  
  - script.js            Frontend logic and API calls  
- templates/  
  - sies.html            College-style landing page with embedded chatbot widget  
  - index.html           Standalone full-page chatbot interface  
  - widget.html          Chat widget iframe content  
- main/                 Images and media assets (college building, logo, etc.)

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

git clone https://github.com/kartikpatade/flask-chatbot-webapp.git  
cd flask-chatbot-webapp  

---

### 2. Create a Virtual Environment (Recommended)

**Windows**
python -m venv venv  
venv\Scripts\activate  

**Mac / Linux**
python3 -m venv venv  
source venv/bin/activate  

---

### 3. Install Dependencies

pip install -r requirements.txt  

This installs Flask, fuzzywuzzy, python-Levenshtein, and nltk.

---

### 4. Run the Application

python app.py  

On first run, the application automatically downloads required NLTK datasets such as `punkt` and `stopwords`.

---

### 5. Access the Application

- College homepage with chatbot widget:  
  http://127.0.0.1:5000/

- Standalone chatbot interface:  
  http://127.0.0.1:5000/chatbot

---

## 🧠 How It Works

1. User input is sent from the frontend to the Flask backend via a POST request.
2. The input text is cleaned by removing punctuation and stop words using NLTK.
3. Fuzzy string matching compares the processed input against predefined intent patterns.
4. The intent with the highest similarity score is selected.
5. If the confidence score is low, a fallback response suggests valid topics to the user.

---

## 🚫 Limitations

- Designed primarily for local execution
- Not hosted on GitHub Pages (Flask backend required)
- Knowledge base is rule-based and not ML-trained

---

## 🔮 Future Enhancements

- Improve chatbot intelligence with ML or transformer-based models
- Add database integration for dynamic content
- Admin dashboard for updating FAQs
- User authentication
- Cloud deployment (Render / Railway / PythonAnywhere)
- UI and accessibility improvements

---
