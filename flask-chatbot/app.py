from flask import Flask, render_template, request, jsonify, send_from_directory
from fuzzywuzzy import fuzz
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

app = Flask(__name__)

# --- NLTK Setup and Text Preprocessing ---
def setup_nltk():
    required_packages = ['punkt', 'stopwords']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}' if package == 'punkt' else f'corpora/{package}')
        except LookupError:
            nltk.download(package, quiet=True)

setup_nltk()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    return " ".join([t for t in tokens if t not in stop_words])


# --- Chatbot Intents and Responses ---
intents = [
    {
        "intent": "college_established",
        "patterns": ["when was college established", "founding year", "established", "year founded", "when started", "college history", "background"],
        "responses": ["SIES (Nerul) College of Arts, Science and Commerce was established in 1998."]
    },
    {
        "intent": "affiliation",
        "patterns": ["affiliated with", "university", "affiliation", "which university", "university of mumbai"],
        "responses": ["The college is affiliated with the University of Mumbai."]
    },
    {
        "intent": "autonomy",
        "patterns": ["autonomous", "autonomy status", "when became autonomous", "autonomous status", "ugc autonomy"],
        "responses": ["The college achieved autonomous status in May 2023, recognized by UGC."]
    },
    {
        "intent": "naac_grade",
        "patterns": ["naac grade", "naac rating", "accreditation", "naac", "grade", "naac a grade", "naac score"],
        "responses": ["The college holds a NAAC 'A' grade in its third cycle with a CGPA of 3.01/4.00."]
    },
    {
        "intent": "location",
        "patterns": ["address", "location", "where is college", "campus address", "nerul address", "navi mumbai", "college location"],
        "responses": ["SIES (Nerul) College is located at Sri Chandrasekarendra Saraswati Vidyapuram, Plot I-C, Sector V, Nerul, Navi Mumbai – 400706, INDIA."]
    },
    {
        "intent": "contact_info",
        "patterns": ["contact", "phone number", "email", "how to reach", "contact details", "get in touch", "phone", "email address"],
        "responses": ["You can reach us at: Phone: +91-22-61196409, 61196410, 61196402, 61196413, 61196414, 61196415, 27708371. Email: ascnsies@sies.edu.in / siesascn@yahoo.in. Website: www.siesascn.edu.in"]
    },
    {
        "intent": "principal",
        "patterns": ["who is principal", "principal name", "current principal", "principal contact", "dr koel"],
        "responses": ["The current Principal is Dr. Koel Roychoudhury (2021–Present). Email: principalascn@sies.edu.in"]
    },
    {
        "intent": "vice_principals",
        "patterns": ["vice principal", "vice principals", "who are vice principals", "vp names"],
        "responses": ["The Vice-Principals are: Ms. Sugandha Jha, Dr. Anu Thomas, and Ms. Sunita Ambhore."]
    },
    {
        "intent": "ug_courses",
        "patterns": ["ug courses", "undergraduate programs", "bachelor programs", "b.com", "b.sc", "b.a", "undergraduate courses", "courses for graduation", "bachelor degree"],
        "responses": [
            "UG programs include:\n"
            "• Commerce: B.Com (General, Entrepreneurship, Management Accounting with Finance, Accounting & Finance, Banking & Insurance, Financial Markets), B.M.S.\n"
            "• Arts: B.A.M.M.C. (Multimedia & Mass Communication)\n"
            "• Science: B.Sc. (Computer Science, Information Technology, Environmental Science, Packaging Technology, Data Science, Artificial Intelligence)"
        ]
    },
    {
        "intent": "pg_courses",
        "patterns": ["pg courses", "postgraduate programs", "master programs", "m.com", "m.sc", "m.a", "postgraduate courses", "masters degree", "pg courses"],
        "responses": [
            "PG programmes include:\n"
            "• Commerce: M.Com (Advanced Accountancy, Business Management)\n"
            "• Arts: M.A. (Business Economics, Multimedia and Mass Communication)\n"
            "• Science: M.Sc. (Computer Science, Information Technology, Environmental Science)"
        ]
    },
    {
        "intent": "junior_college",
        "patterns": ["junior college", "higher secondary", "11th 12th", "plus two", "junior college courses", "fyjc", "syjc"],
        "responses": ["Yes, the college includes a Junior College as part of its institution."]
    },
    {
        "intent": "admission_dates",
        "patterns": ["admission dates", "when to apply", "admission schedule", "form submission", "merit list dates", "admission 2025", "fy 2025-26", "admission process"],
        "responses": ["For FY 2025–26, the online admission form is available from May 8 to May 23, 2025. Merit lists will be published on: 1st - May 27, 2nd - May 31, 3rd - June 5, 2025."]
    },
    {
        "intent": "admission_process",
        "patterns": ["admission process", "how to apply", "application procedure", "samarth portal", "admission requirements", "eligibility criteria"],
        "responses": ["Admission form is available online via the college portal. Pre-admission via the University's Samarth Portal is mandatory. Document submission and fee payment follow each merit list announcement."]
    },
    {
        "intent": "campus_facilities",
        "patterns": ["campus facilities", "infrastructure", "amenities", "what facilities", "campus features", "college facilities", "labs", "library"],
        "responses": [
            "Our campus features:\n"
            "• Modern Classrooms\n"
            "• Computer Laboratory\n"
            "• Environmental Laboratory\n"
            "• Multipurpose Hall\n"
            "• Library with extensive collection\n"
            "• Gymkhana / Sports Complex\n"
            "• Vertical Garden (Biowall)\n"
            "• Bio-Composting Units\n"
            "• Smart Classrooms\n"
            "• Health cum Counseling Center"
        ]
    },
    {
        "intent": "departments",
        "patterns": ["departments", "list of departments", "what departments", "academic departments", "faculty departments"],
        "responses": [
            "Departments and Heads:\n"
            "• Economics: Dr. Koel Roychoudhury\n"
            "• Commerce: Mr. Girish Karnad\n"
            "• Accountancy: Dr. Priyanka Mohan\n"
            "• Banking & Insurance: Ms. Bhumika More\n"
            "• Management Studies: Mr. Chaitanya Songirkar\n"
            "• Information Technology: Dr. Meghna Bhatia\n"
            "• Computer Science: Dr. Sheeja Ravi\n"
            "• Multimedia & Mass Communication: Mr. Mithun Pillai\n"
            "• Environmental Science: Dr. Jyoti Koliyar\n"
            "• Packaging Technology: Prof. Prasad B. Iyer"
        ]
    },
    {
        "intent": "placement_info",
        "patterns": ["placements", "placement cell", "recruiters", "companies", "placement statistics", "top recruiters", "job opportunities"],
        "responses": [
            "Placement Cell Initiatives:\n"
            "• Corporate Readiness Programs\n"
            "• Resume Building & Mock Interviews\n"
            "• Industry Workshops\n"
            "\nTop Recruiters:\n"
            "• Arts/Commerce: ICICI Lombard, TCS BPO, MaxVal, Wipro, Bajaj Finance, HDFC\n"
            "• Science (CS/IT): TCS, Infosys, Accenture, L&T Infotech, Deloitte, Capgemini"
        ]
    },
    {
        "intent": "committees",
        "patterns": ["committees", "statutory committees", "iqac", "grievance cell", "anti-ragging", "student committees", "clubs"],
        "responses": [
            "Key Committees:\n"
            "• IQAC (Internal Quality Assurance Cell)\n"
            "• Equal Opportunity Cell\n"
            "• Internal Committee (Sexual Harassment Prevention)\n"
            "• Student Grievance Cell\n"
            "• Anti-Ragging Committee\n"
            "• Placement Cell\n"
            "• Students Council\n"
            "• Rotaract Club\n"
            "• NSS (National Service Scheme)\n"
            "• Marathi Vangmay Mandal\n"
            "• South Indian Association"
        ]
    },
    {
        "intent": "student_life",
        "patterns": ["student life", "extracurricular", "activities", "clubs", "events", "festivals", "cultural activities", "sports"],
        "responses": [
            "Student Life Highlights:\n"
            "• National Service Scheme (NSS) with 200+ volunteers\n"
            "• Students Council for leadership development\n"
            "• Rotaract Club for community service\n"
            "• Sports Committee for inter-college competitions\n"
            "• Marathi Vangmay Mandal for cultural events\n"
            "• South Indian Association for regional festivals\n"
            "• Music Club, Finance Club, Innovation Club\n"
            "• Annual cultural fest with dance, drama, music"
        ]
    },
    {
        "intent": "library",
        "patterns": ["library", "library facilities", "books", "digital resources", "library timings", "librarian"],
        "responses": ["The college library has an extensive collection of books and digital resources. Managed by Librarian Mr. Gulabchandra Sharma."]
    },
    {
        "intent": "website",
        "patterns": ["website", "official website", "college website", "online portal", "web address"],
        "responses": ["Visit our official website at: www.siesascn.edu.in"]
    },
    {
        "intent": "motto",
        "patterns": ["motto", "college motto", "vision", "mission", "philosophy"],
        "responses": ["Motto: \"Tirelessly strive towards perfection and scaling greater heights.\"\nVision: To create a better society by educating future generations through holistic, value-based, and industry-relevant education."]
    },
    {
        "intent": "past_principals",
        "patterns": ["past principals", "former principals", "previous principals", "history of principals"],
        "responses": [
            "Past Principals:\n"
            "• Dr. Koel Roychoudhury (Principal I/c, 2016–2017)\n"
            "• Dr. Milind Vaidya (2017–2021)\n"
            "• Dr. Rita Basu (2011–2016)\n"
            "• Dr. Meera Vijay (2009–2011)\n"
            "• Dr. Minu Thomas (2008–2009)\n"
            "• Dr. U.B. Jangam (2006–2008)\n"
            "• Prof. Y.B. Bhide (2005–2006)\n"
            "• Prof. G.V. Subramaniam (2000–2005)\n"
            "• Prof. S. Ramanathan (1998–1999)"
        ]
    },
    {
        "intent": "governing_body",
        "patterns": ["governing body", "trust", "management", "sies trust", "founders", "president"],
        "responses": [
            "Governing Body:\n"
            "• Dr. V. Shankar — President, SIES Trust\n"
            "• Shri. M. V. Ramnarayan — Working President\n"
        ]
    }
]

# --- Chatbot Logic ---
def get_response(user_message):
    user_message = preprocess_text(user_message)
    best_intent, best_score, best_response = None, 0, None

    for intent in intents:
        for pattern in intent["patterns"]:
            score = fuzz.token_sort_ratio(user_message, preprocess_text(pattern))
            if score > best_score:
                best_score = score
                best_intent = intent
                best_response = intent["responses"][0]

    if best_score < 50:
        return {"reply": "I'm sorry, I don't have information about that. Try asking about admissions, courses, facilities, or contact details.", "intent": "unknown"}

    return {"reply": best_response, "intent": best_intent["intent"]}


# --- Flask Routes ---

# Serves the main college website as the homepage
@app.route('/')
def college_page():
    return render_template('sies.html')

# Serves the standalone chatbot page on a separate link
@app.route('/chatbot')
def index():
    return render_template('index.html')

# Serves the chatbot widget for the iframe
@app.route('/widget')
def widget():
    return render_template('widget.html')

# Serves the image and video files from the 'main' folder
@app.route('/main/<path:filename>')
def main_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'main'), filename)

# Handles chat messages from all interfaces
@app.route('/get', methods=['POST'])
def get_bot_response():
    user_message = request.json.get('message', '')
    return jsonify(get_response(user_message))

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)