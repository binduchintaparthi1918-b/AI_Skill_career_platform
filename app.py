import streamlit as st
import random

from database import (
    create_tables,
    register_user,
    login_user,
    get_user,
    update_profile,
    save_assessment_result,
    get_assessment_results,
    save_career_recommendation,
    get_career_recommendations,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

create_tables()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "logged_in": False,
    "user_id": None,
    "user_name": "",
    "page": "Login",

    "assessment_started": False,
    "assessment_questions": [],
    "assessment_answers": {},
    "assessment_index": 0,

    "review_questions": [],
    "review_answers": {},
    "review_skill": "",
    "review_score": 0,

    "last_assessment_id": None,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(124, 58, 237, 0.14),
            transparent 30%
        ),
        radial-gradient(
            circle at 100% 0%,
            rgba(37, 99, 235, 0.13),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8f7ff 0%,
            #eef4ff 50%,
            #f8faff 100%
        );

    color: #172033;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   HEADINGS
============================================================ */

h1 {
    color: #312e81 !important;
    font-weight: 800 !important;
    letter-spacing: -0.6px;
}

h2 {
    color: #3730a3 !important;
    font-weight: 750 !important;
}

h3 {
    color: #4338ca !important;
    font-weight: 700 !important;
}


/* ============================================================
   SIDEBAR
============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #171342 0%,
            #21165f 48%,
            #312e81 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    background: rgba(255,255,255,0.08) !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.07) !important;

    border-radius: 12px !important;

    font-weight: 600 !important;

    margin-bottom: 5px;

    transition: 0.2s ease;
}

[data-testid="stSidebar"] .stButton > button:hover {

    background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        ) !important;

    transform: translateX(3px);

    box-shadow:
        0 6px 18px rgba(99,102,241,0.25);
}


/* ============================================================
   NORMAL BUTTONS
============================================================ */

.stButton > button {

    border: none !important;

    border-radius: 11px !important;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    padding: 0.65rem 1.2rem !important;

    box-shadow:
        0 5px 15px rgba(79,70,229,0.20);

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 22px rgba(79,70,229,0.30);
}


/* ============================================================
   INPUTS
============================================================ */

.stTextInput input,
.stTextArea textarea {

    border-radius: 10px !important;

    border: 1px solid #dbe3f0 !important;

    background: white !important;

    color: #172033 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {

    border-color: #6366f1 !important;

    box-shadow:
        0 0 0 2px rgba(99,102,241,0.12) !important;
}


/* ============================================================
   SELECT BOX
============================================================ */

.stSelectbox div[data-baseweb="select"] > div {

    border-radius: 10px !important;

    border: 1px solid #dbe3f0 !important;

    background: white !important;
}


/* ============================================================
   DASHBOARD CARDS
============================================================ */

.dashboard-card {

    background:
        rgba(255,255,255,0.94);

    border-radius: 18px;

    padding: 24px;

    min-height: 145px;

    border: 1px solid #e0e7ff;

    box-shadow:
        0 8px 25px rgba(30,41,59,0.07);

    transition: 0.25s ease;
}

.dashboard-card:hover {

    transform: translateY(-4px);

    box-shadow:
        0 14px 30px rgba(79,70,229,0.14);
}


/* ============================================================
   SKILL CARD
============================================================ */

.skill-card {

    background: white;

    border-radius: 18px;

    padding: 22px;

    margin-bottom: 18px;

    border-left: 5px solid #6366f1;

    border-top: 1px solid #e0e7ff;

    border-right: 1px solid #e0e7ff;

    border-bottom: 1px solid #e0e7ff;

    box-shadow:
        0 7px 22px rgba(30,41,59,0.07);
}


/* ============================================================
   GAP CARD
============================================================ */

.gap-card {

    background: white !important;

    color: #172033 !important;

    border-radius: 18px;

    padding: 22px;

    margin-bottom: 20px;

    border: 1px solid #dbe3ff;

    box-shadow:
        0 8px 25px rgba(30,41,59,0.07);
}

.gap-card h3,
.gap-card p,
.gap-card li,
.gap-card span,
.gap-card div {

    color: #172033 !important;
}


/* ============================================================
   GAP POINT
============================================================ */

.gap-point {

    background: #f8faff !important;

    color: #172033 !important;

    border: 1px solid #dbe3ff;

    border-left: 5px solid #6366f1;

    border-radius: 10px;

    padding: 11px 15px;

    margin: 8px 0;

    font-size: 15px;

    font-weight: 600;

    box-shadow:
        0 4px 12px rgba(30,41,59,0.05);
}

.gap-point * {

    color: #172033 !important;
}


/* ============================================================
   CAREER CARD
============================================================ */

.career-card {

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f5f3ff
        );

    border-radius: 18px;

    padding: 24px;

    margin-bottom: 20px;

    border: 1px solid #ddd6fe;

    box-shadow:
        0 8px 25px rgba(79,70,229,0.08);
}


/* ============================================================
   PROJECT CARD
============================================================ */

.project-card {

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #eff6ff
        );

    border-radius: 18px;

    padding: 24px;

    margin-bottom: 20px;

    border: 1px solid #dbeafe;

    box-shadow:
        0 8px 25px rgba(37,99,235,0.08);
}


/* ============================================================
   ROADMAP CARD
============================================================ */

.roadmap-card {

    background: white;

    border-radius: 16px;

    padding: 20px;

    margin-bottom: 15px;

    border-left: 5px solid #7c3aed;

    border-top: 1px solid #e0e7ff;

    border-right: 1px solid #e0e7ff;

    border-bottom: 1px solid #e0e7ff;

    box-shadow:
        0 6px 20px rgba(30,41,59,0.06);
}


/* ============================================================
   QUESTION CARD
============================================================ */

.question-card {

    background: white;

    border-radius: 18px;

    padding: 25px;

    border: 1px solid #e0e7ff;

    box-shadow:
        0 8px 25px rgba(30,41,59,0.08);
}


/* ============================================================
   SCORE CARD
============================================================ */

.score-card {

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );

    color: white;

    border-radius: 20px;

    padding: 28px;

    text-align: center;

    box-shadow:
        0 12px 30px rgba(79,70,229,0.25);
}

.score-card h1,
.score-card h2,
.score-card h3,
.score-card p {

    color: white !important;
}


/* ============================================================
   METRICS
============================================================ */

div[data-testid="stMetric"] {

    background: rgba(255,255,255,0.94);

    padding: 18px;

    border-radius: 15px;

    border: 1px solid #e0e7ff;

    box-shadow:
        0 5px 16px rgba(30,41,59,0.06);
}


/* ============================================================
   EXPANDERS
============================================================ */

[data-testid="stExpander"] {

    background: white;

    border: 1px solid #e0e7ff !important;

    border-radius: 14px !important;

    margin-bottom: 12px;

    box-shadow:
        0 5px 18px rgba(30,41,59,0.05);
}


/* ============================================================
   PROGRESS
============================================================ */

div[data-testid="stProgress"] > div > div {

    background:
        linear-gradient(
            90deg,
            #4f46e5,
            #8b5cf6
        );
}


/* ============================================================
   ALERTS
============================================================ */

div[data-testid="stAlert"] {

    border-radius: 13px !important;
}


/* ============================================================
   DIVIDER
============================================================ */

hr {

    border: none;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #c7d2fe,
            transparent
        );
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    text-align: center;

    color: #64748b;

    font-size: 13px;

    margin-top: 35px;

    padding: 20px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# QUESTION BANK
# ============================================================

QUESTION_BANK = {

    "Python": [

        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "define", "fun"],
            "answer": "def",
            "level": "Beginner"
        },

        {
            "question": "Which data type stores key-value pairs?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary",
            "level": "Beginner"
        },

        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#",
            "level": "Beginner"
        },

        {
            "question": "Which keyword is used to handle exceptions?",
            "options": ["catch", "try", "handle", "error"],
            "answer": "try",
            "level": "Intermediate"
        },

        {
            "question": "Which method adds an item to the end of a list?",
            "options": ["add()", "insert()", "append()", "push()"],
            "answer": "append()",
            "level": "Beginner"
        },

        {
            "question": "Which concept allows a class to inherit another class?",
            "options": [
                "Encapsulation",
                "Inheritance",
                "Iteration",
                "Compilation"
            ],
            "answer": "Inheritance",
            "level": "Intermediate"
        },

        {
            "question": "Which library is commonly used for numerical computing?",
            "options": [
                "NumPy",
                "Django",
                "Flask",
                "BeautifulSoup"
            ],
            "answer": "NumPy",
            "level": "Intermediate"
        },

        {
            "question": "What does len() return?",
            "options": [
                "Memory size",
                "Number of elements",
                "Data type",
                "Index"
            ],
            "answer": "Number of elements",
            "level": "Beginner"
        },

        {
            "question": "Which keyword creates a class?",
            "options": ["object", "class", "struct", "new"],
            "answer": "class",
            "level": "Beginner"
        },

        {
            "question": "Which collection does not allow duplicate values?",
            "options": ["List", "Tuple", "Set", "Dictionary"],
            "answer": "Set",
            "level": "Beginner"
        },

        {
            "question": "Which keyword is used to create an anonymous function?",
            "options": ["anonymous", "lambda", "func", "inline"],
            "answer": "lambda",
            "level": "Advanced"
        },

        {
            "question": "What does PEP stand for in Python?",
            "options": [
                "Python Enhancement Proposal",
                "Python Execution Program",
                "Programming Enhancement Process",
                "Python Evaluation Protocol"
            ],
            "answer": "Python Enhancement Proposal",
            "level": "Advanced"
        }
    ],


    "Java": [

        {
            "question": "Which keyword is used to create a class in Java?",
            "options": ["class", "Class", "object", "define"],
            "answer": "class",
            "level": "Beginner"
        },

        {
            "question": "Which method is the entry point of a Java application?",
            "options": [
                "start()",
                "main()",
                "run()",
                "execute()"
            ],
            "answer": "main()",
            "level": "Beginner"
        },

        {
            "question": "Which concept allows multiple forms of a method?",
            "options": [
                "Inheritance",
                "Polymorphism",
                "Encapsulation",
                "Abstraction"
            ],
            "answer": "Polymorphism",
            "level": "Intermediate"
        },

        {
            "question": "Which keyword is used for inheritance?",
            "options": [
                "inherits",
                "extends",
                "implements",
                "super"
            ],
            "answer": "extends",
            "level": "Beginner"
        },

        {
            "question": "Which collection does not allow duplicate elements?",
            "options": [
                "ArrayList",
                "HashSet",
                "LinkedList",
                "Vector"
            ],
            "answer": "HashSet",
            "level": "Intermediate"
        },

        {
            "question": "Which keyword is used to create an object?",
            "options": ["create", "new", "object", "instance"],
            "answer": "new",
            "level": "Beginner"
        },

        {
            "question": "Which keyword prevents inheritance?",
            "options": ["static", "final", "private", "constant"],
            "answer": "final",
            "level": "Intermediate"
        },

        {
            "question": "Which framework is commonly used for Java backend development?",
            "options": [
                "Spring Boot",
                "Django",
                "Flask",
                "React"
            ],
            "answer": "Spring Boot",
            "level": "Intermediate"
        },

        {
            "question": "Which keyword is used to implement an interface?",
            "options": [
                "extends",
                "implements",
                "interface",
                "inherit"
            ],
            "answer": "implements",
            "level": "Intermediate"
        },

        {
            "question": "What does JVM stand for?",
            "options": [
                "Java Virtual Machine",
                "Java Variable Method",
                "Java Visual Machine",
                "Java Version Manager"
            ],
            "answer": "Java Virtual Machine",
            "level": "Beginner"
        },

        {
            "question": "Which block handles exceptions?",
            "options": [
                "try-catch",
                "if-else",
                "switch-case",
                "for-loop"
            ],
            "answer": "try-catch",
            "level": "Intermediate"
        }
    ],


    "HTML/CSS": [

        {
            "question": "Which tag creates the largest heading?",
            "options": ["<h1>", "<h6>", "<head>", "<title>"],
            "answer": "<h1>",
            "level": "Beginner"
        },

        {
            "question": "Which tag creates a hyperlink?",
            "options": ["<link>", "<a>", "<href>", "<url>"],
            "answer": "<a>",
            "level": "Beginner"
        },

        {
            "question": "Which property changes text color?",
            "options": [
                "font-color",
                "text-color",
                "color",
                "foreground"
            ],
            "answer": "color",
            "level": "Beginner"
        },

        {
            "question": "Which CSS layout system is designed for one-dimensional layouts?",
            "options": [
                "Grid",
                "Flexbox",
                "Float",
                "Position"
            ],
            "answer": "Flexbox",
            "level": "Intermediate"
        },

        {
            "question": "Which CSS property changes the background color?",
            "options": [
                "background-color",
                "bg-color",
                "color-background",
                "background"
            ],
            "answer": "background-color",
            "level": "Beginner"
        },

        {
            "question": "Which HTML tag creates a form?",
            "options": [
                "<input>",
                "<form>",
                "<fieldset>",
                "<data>"
            ],
            "answer": "<form>",
            "level": "Beginner"
        },

        {
            "question": "Which CSS property controls spacing inside an element?",
            "options": [
                "margin",
                "padding",
                "spacing",
                "gap"
            ],
            "answer": "padding",
            "level": "Beginner"
        },

        {
            "question": "Which layout system is useful for two-dimensional layouts?",
            "options": [
                "Flexbox",
                "Grid",
                "Float",
                "Inline"
            ],
            "answer": "Grid",
            "level": "Intermediate"
        },

        {
            "question": "Which attribute provides alternative text for an image?",
            "options": [
                "src",
                "alt",
                "title",
                "href"
            ],
            "answer": "alt",
            "level": "Beginner"
        },

        {
            "question": "Which CSS rule is commonly used for responsive design?",
            "options": [
                "@media",
                "@screen",
                "@responsive",
                "@device"
            ],
            "answer": "@media",
            "level": "Intermediate"
        }
    ],


    "JavaScript": [

        {
            "question": "Which keyword declares a variable that can be reassigned?",
            "options": ["const", "let", "fixed", "static"],
            "answer": "let",
            "level": "Beginner"
        },

        {
            "question": "Which keyword declares a constant?",
            "options": ["constant", "let", "const", "fixed"],
            "answer": "const",
            "level": "Beginner"
        },

        {
            "question": "Which method adds an element to an array?",
            "options": [
                "append()",
                "push()",
                "add()",
                "insert()"
            ],
            "answer": "push()",
            "level": "Beginner"
        },

        {
            "question": "Which method selects an element by ID?",
            "options": [
                "getElementById()",
                "selectById()",
                "findId()",
                "queryId()"
            ],
            "answer": "getElementById()",
            "level": "Beginner"
        },

        {
            "question": "Which format is commonly used for exchanging data with APIs?",
            "options": [
                "HTML",
                "JSON",
                "CSS",
                "XML only"
            ],
            "answer": "JSON",
            "level": "Beginner"
        },

        {
            "question": "Which keyword defines an asynchronous function?",
            "options": [
                "async",
                "await",
                "promise",
                "future"
            ],
            "answer": "async",
            "level": "Intermediate"
        },

        {
            "question": "Which method converts JSON text into a JavaScript object?",
            "options": [
                "JSON.parse()",
                "JSON.convert()",
                "JSON.object()",
                "JSON.decode()"
            ],
            "answer": "JSON.parse()",
            "level": "Intermediate"
        },

        {
            "question": "Which event occurs when a button is clicked?",
            "options": [
                "hover",
                "click",
                "press",
                "select"
            ],
            "answer": "click",
            "level": "Beginner"
        },

        {
            "question": "Which keyword is used to define a function?",
            "options": [
                "function",
                "def",
                "fun",
                "method"
            ],
            "answer": "function",
            "level": "Beginner"
        },

        {
            "question": "Which method removes the last array element?",
            "options": [
                "remove()",
                "delete()",
                "pop()",
                "last()"
            ],
            "answer": "pop()",
            "level": "Beginner"
        }
    ],


    "SQL": [

        {
            "question": "Which command retrieves data from a database?",
            "options": [
                "GET",
                "SELECT",
                "FETCH",
                "READ"
            ],
            "answer": "SELECT",
            "level": "Beginner"
        },

        {
            "question": "Which command adds a new record?",
            "options": [
                "ADD",
                "INSERT",
                "CREATE",
                "APPEND"
            ],
            "answer": "INSERT",
            "level": "Beginner"
        },

        {
            "question": "Which command changes existing records?",
            "options": [
                "CHANGE",
                "MODIFY",
                "UPDATE",
                "ALTER"
            ],
            "answer": "UPDATE",
            "level": "Beginner"
        },

        {
            "question": "Which command removes records?",
            "options": [
                "REMOVE",
                "DELETE",
                "DROP",
                "CLEAR"
            ],
            "answer": "DELETE",
            "level": "Beginner"
        },

        {
            "question": "Which clause filters rows?",
            "options": [
                "FILTER",
                "WHERE",
                "HAVING",
                "SELECT"
            ],
            "answer": "WHERE",
            "level": "Beginner"
        },

        {
            "question": "Which clause groups rows?",
            "options": [
                "GROUP BY",
                "ORDER BY",
                "SORT BY",
                "COLLECT BY"
            ],
            "answer": "GROUP BY",
            "level": "Intermediate"
        },

        {
            "question": "Which keyword combines rows from related tables?",
            "options": [
                "JOIN",
                "COMBINE",
                "MERGE",
                "CONNECT"
            ],
            "answer": "JOIN",
            "level": "Intermediate"
        },

        {
            "question": "Which function counts rows?",
            "options": [
                "TOTAL()",
                "COUNT()",
                "NUMBER()",
                "ROWS()"
            ],
            "answer": "COUNT()",
            "level": "Beginner"
        },

        {
            "question": "Which key uniquely identifies a row?",
            "options": [
                "Foreign key",
                "Primary key",
                "Unique row",
                "Index key"
            ],
            "answer": "Primary key",
            "level": "Beginner"
        },

        {
            "question": "Which clause sorts query results?",
            "options": [
                "SORT BY",
                "ORDER BY",
                "GROUP BY",
                "ARRANGE BY"
            ],
            "answer": "ORDER BY",
            "level": "Beginner"
        },

        {
            "question": "Which operation combines matching rows from two tables?",
            "options": [
                "INNER JOIN",
                "MATCH",
                "LINK",
                "PAIR"
            ],
            "answer": "INNER JOIN",
            "level": "Intermediate"
        }
    ],


    "Data Science": [

        {
            "question": "Which Python library is commonly used for data analysis?",
            "options": [
                "Pandas",
                "Django",
                "Flask",
                "Tkinter"
            ],
            "answer": "Pandas",
            "level": "Beginner"
        },

        {
            "question": "Which library is commonly used for numerical operations?",
            "options": [
                "NumPy",
                "Django",
                "Requests",
                "Flask"
            ],
            "answer": "NumPy",
            "level": "Beginner"
        },

        {
            "question": "Which library is commonly used for plotting?",
            "options": [
                "Matplotlib",
                "SQLite",
                "Requests",
                "Django"
            ],
            "answer": "Matplotlib",
            "level": "Beginner"
        },

        {
            "question": "What is data cleaning?",
            "options": [
                "Deleting all data",
                "Preparing data by fixing errors and inconsistencies",
                "Creating a database",
                "Encrypting data"
            ],
            "answer": "Preparing data by fixing errors and inconsistencies",
            "level": "Intermediate"
        },

        {
            "question": "Which technique is used to predict continuous values?",
            "options": [
                "Regression",
                "Classification",
                "Clustering",
                "Sorting"
            ],
            "answer": "Regression",
            "level": "Intermediate"
        },

        {
            "question": "Which technique groups similar data points?",
            "options": [
                "Regression",
                "Clustering",
                "Classification",
                "Encoding"
            ],
            "answer": "Clustering",
            "level": "Intermediate"
        },

        {
            "question": "What is the purpose of a training dataset?",
            "options": [
                "To train a model",
                "To delete data",
                "To display HTML",
                "To create passwords"
            ],
            "answer": "To train a model",
            "level": "Beginner"
        },

        {
            "question": "Which measure represents the average?",
            "options": [
                "Mean",
                "Median only",
                "Mode only",
                "Range"
            ],
            "answer": "Mean",
            "level": "Beginner"
        },

        {
            "question": "Which metric is commonly used for classification?",
            "options": [
                "Accuracy",
                "Average",
                "Variance only",
                "Range"
            ],
            "answer": "Accuracy",
            "level": "Intermediate"
        },

        {
            "question": "What is feature selection?",
            "options": [
                "Selecting useful input variables",
                "Deleting the dataset",
                "Changing the model name",
                "Creating a website"
            ],
            "answer": "Selecting useful input variables",
            "level": "Advanced"
        },

        {
            "question": "Which library is commonly used for machine learning in Python?",
            "options": [
                "Scikit-learn",
                "Tkinter",
                "Django",
                "BeautifulSoup"
            ],
            "answer": "Scikit-learn",
            "level": "Intermediate"
        }
    ]
}


# ============================================================
# CAREER DATA
# ============================================================

CAREERS = {

    "Python": [

        {
            "name": "Python Developer",
            "technologies": [
                "Python",
                "OOP",
                "SQL",
                "REST APIs",
                "Git"
            ],
            "topics": [
                "Python fundamentals",
                "Functions",
                "Data structures",
                "OOP",
                "Exception handling",
                "APIs",
                "Database connectivity"
            ],
            "process": [
                "Learn Python fundamentals",
                "Practice functions and data structures",
                "Learn OOP",
                "Learn SQL",
                "Learn REST APIs",
                "Build Python projects",
                "Use Git and GitHub",
                "Create a portfolio"
            ]
        },

        {
            "name": "Backend Developer",
            "technologies": [
                "Python",
                "Django or Flask",
                "SQL",
                "REST API",
                "Git"
            ],
            "topics": [
                "Python",
                "HTTP",
                "REST APIs",
                "CRUD",
                "Authentication",
                "Databases"
            ],
            "process": [
                "Learn Python",
                "Learn HTTP and REST APIs",
                "Learn Flask or Django",
                "Learn databases",
                "Build CRUD applications",
                "Build APIs",
                "Add authentication",
                "Deploy a project"
            ]
        },

        {
            "name": "AI/ML Developer",
            "technologies": [
                "Python",
                "NumPy",
                "Pandas",
                "Machine Learning",
                "SQL"
            ],
            "topics": [
                "Python",
                "Statistics",
                "Data preprocessing",
                "Machine learning",
                "Model evaluation"
            ],
            "process": [
                "Strengthen Python",
                "Learn NumPy and Pandas",
                "Learn statistics",
                "Learn machine learning",
                "Practice data preprocessing",
                "Train models",
                "Build AI projects"
            ]
        }
    ],

    "Java": [

        {
            "name": "Java Developer",
            "technologies": [
                "Java",
                "OOP",
                "Collections",
                "SQL",
                "Git"
            ],
            "topics": [
                "Java fundamentals",
                "OOP",
                "Inheritance",
                "Polymorphism",
                "Collections",
                "Database connectivity"
            ],
            "process": [
                "Learn Java fundamentals",
                "Practice OOP",
                "Learn collections",
                "Learn exception handling",
                "Learn SQL",
                "Build Java applications",
                "Create a portfolio"
            ]
        },

        {
            "name": "Backend Java Developer",
            "technologies": [
                "Java",
                "Spring Boot",
                "REST API",
                "SQL",
                "Git"
            ],
            "topics": [
                "Java",
                "Spring Boot",
                "REST APIs",
                "CRUD",
                "Authentication",
                "Database connectivity"
            ],
            "process": [
                "Learn Core Java",
                "Learn OOP",
                "Learn Spring Boot",
                "Build REST APIs",
                "Learn databases",
                "Build CRUD applications",
                "Add authentication"
            ]
        }
    ],

    "HTML/CSS": [

        {
            "name": "Frontend Developer",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript",
                "Git",
                "Responsive Design"
            ],
            "topics": [
                "HTML",
                "CSS",
                "Flexbox",
                "Grid",
                "Responsive design",
                "JavaScript"
            ],
            "process": [
                "Learn HTML",
                "Learn CSS",
                "Practice Flexbox and Grid",
                "Build responsive pages",
                "Learn JavaScript",
                "Build frontend projects",
                "Create a portfolio"
            ]
        },

        {
            "name": "Web Designer",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript",
                "Responsive Design",
                "UI Design"
            ],
            "topics": [
                "Layouts",
                "Typography",
                "Colors",
                "Responsive design",
                "Navigation",
                "Forms"
            ],
            "process": [
                "Learn HTML",
                "Learn CSS",
                "Practice layouts",
                "Learn responsive design",
                "Create landing pages",
                "Build website interfaces",
                "Create a portfolio"
            ]
        }
    ],

    "JavaScript": [

        {
            "name": "JavaScript Developer",
            "technologies": [
                "JavaScript",
                "HTML",
                "CSS",
                "DOM",
                "REST APIs",
                "Git"
            ],
            "topics": [
                "Variables",
                "Functions",
                "Arrays",
                "Objects",
                "DOM",
                "Events",
                "APIs",
                "Async JavaScript"
            ],
            "process": [
                "Learn JavaScript fundamentals",
                "Practice arrays and objects",
                "Learn functions",
                "Learn DOM",
                "Learn events",
                "Learn APIs",
                "Build interactive applications"
            ]
        },

        {
            "name": "Full Stack Developer",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript",
                "Node.js",
                "SQL",
                "REST API"
            ],
            "topics": [
                "Frontend",
                "JavaScript",
                "Backend",
                "APIs",
                "Databases",
                "Authentication"
            ],
            "process": [
                "Learn HTML and CSS",
                "Learn JavaScript",
                "Learn backend development",
                "Learn databases",
                "Build APIs",
                "Connect frontend and backend",
                "Build full-stack applications"
            ]
        }
    ],

    "SQL": [

        {
            "name": "SQL Developer",
            "technologies": [
                "SQL",
                "MySQL or PostgreSQL",
                "Database Design",
                "Python"
            ],
            "topics": [
                "SELECT",
                "WHERE",
                "GROUP BY",
                "JOIN",
                "Subqueries",
                "Indexes",
                "Database design"
            ],
            "process": [
                "Learn SQL fundamentals",
                "Practice SELECT",
                "Learn filtering",
                "Learn GROUP BY",
                "Learn JOIN",
                "Learn subqueries",
                "Learn database design",
                "Build database projects"
            ]
        },

        {
            "name": "Data Analyst",
            "technologies": [
                "SQL",
                "Excel",
                "Python",
                "Pandas",
                "Power BI"
            ],
            "topics": [
                "SQL",
                "Data cleaning",
                "Statistics",
                "Visualization",
                "Dashboards"
            ],
            "process": [
                "Learn SQL",
                "Learn Excel",
                "Learn Python",
                "Learn Pandas",
                "Learn statistics",
                "Create dashboards",
                "Analyze real datasets"
            ]
        }
    ],

    "Data Science": [

        {
            "name": "Data Scientist",
            "technologies": [
                "Python",
                "NumPy",
                "Pandas",
                "Matplotlib",
                "Scikit-learn",
                "SQL"
            ],
            "topics": [
                "Python",
                "Statistics",
                "Data cleaning",
                "EDA",
                "Visualization",
                "Machine learning"
            ],
            "process": [
                "Learn Python",
                "Learn NumPy and Pandas",
                "Learn statistics",
                "Practice data cleaning",
                "Perform EDA",
                "Learn machine learning",
                "Evaluate models",
                "Build data science projects"
            ]
        },

        {
            "name": "Data Analyst",
            "technologies": [
                "Python",
                "Pandas",
                "SQL",
                "Excel",
                "Power BI"
            ],
            "topics": [
                "Data cleaning",
                "SQL",
                "Statistics",
                "Visualization",
                "EDA",
                "Dashboards"
            ],
            "process": [
                "Learn SQL",
                "Learn Excel",
                "Learn Python",
                "Learn Pandas",
                "Practice data cleaning",
                "Create visualizations",
                "Build dashboards"
            ]
        }
    ]
}


# ============================================================
# PROJECT DATA
# ============================================================

PROJECTS = {

    "Python": [

        {
            "name": "Student Management System",
            "technologies": [
                "Python",
                "SQLite",
                "OOP"
            ],
            "topics": [
                "Functions",
                "Lists",
                "Dictionaries",
                "OOP",
                "CRUD",
                "Database"
            ],
            "process": [
                "Create the student database",
                "Create student fields",
                "Create Python classes",
                "Implement Add Student",
                "Implement View Student",
                "Implement Update Student",
                "Implement Delete Student",
                "Connect Python with SQLite",
                "Add exception handling",
                "Test the application"
            ]
        },

        {
            "name": "Expense Tracker",
            "technologies": [
                "Python",
                "SQLite",
                "OOP"
            ],
            "topics": [
                "Functions",
                "Lists",
                "Dictionaries",
                "OOP",
                "CRUD",
                "Database"
            ],
            "process": [
                "Create expense database",
                "Create categories",
                "Add expenses",
                "View expenses",
                "Update expenses",
                "Delete expenses",
                "Calculate totals",
                "Generate summaries"
            ]
        },

        {
            "name": "AI Chatbot",
            "technologies": [
                "Python",
                "API",
                "JSON",
                "Streamlit"
            ],
            "topics": [
                "Python",
                "Functions",
                "API",
                "JSON",
                "Exception handling"
            ],
            "process": [
                "Create chatbot interface",
                "Accept questions",
                "Connect an AI API",
                "Send user input",
                "Receive response",
                "Display response",
                "Handle errors",
                "Improve the interface"
            ]
        }
    ],

    "Java": [

        {
            "name": "Library Management System",
            "technologies": [
                "Java",
                "OOP",
                "MySQL"
            ],
            "topics": [
                "Classes",
                "Objects",
                "Inheritance",
                "Collections",
                "CRUD",
                "SQL"
            ],
            "process": [
                "Design database",
                "Create Book class",
                "Create Student class",
                "Add books",
                "Search books",
                "Issue books",
                "Return books",
                "Connect Java with database",
                "Test application"
            ]
        },

        {
            "name": "Bank Management System",
            "technologies": [
                "Java",
                "OOP",
                "MySQL"
            ],
            "topics": [
                "Classes",
                "Objects",
                "Inheritance",
                "Database",
                "CRUD"
            ],
            "process": [
                "Create customer database",
                "Create account class",
                "Create customer registration",
                "Implement deposit",
                "Implement withdrawal",
                "Implement balance checking",
                "Connect database",
                "Test transactions"
            ]
        }
    ],

    "HTML/CSS": [

        {
            "name": "Personal Portfolio Website",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript"
            ],
            "topics": [
                "HTML",
                "CSS",
                "Flexbox",
                "Grid",
                "Responsive design",
                "JavaScript"
            ],
            "process": [
                "Create HTML structure",
                "Create navigation",
                "Add About section",
                "Add Skills section",
                "Add Projects section",
                "Add Contact section",
                "Style with CSS",
                "Make responsive",
                "Add JavaScript interactions"
            ]
        },

        {
            "name": "Online Shopping Website",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript"
            ],
            "topics": [
                "HTML",
                "CSS",
                "Responsive design",
                "JavaScript",
                "Product cards",
                "Search",
                "Shopping cart"
            ],
            "process": [
                "Create product page",
                "Create product cards",
                "Add product images",
                "Add search",
                "Add category filtering",
                "Create shopping cart",
                "Add quantity controls",
                "Create checkout interface",
                "Make responsive"
            ]
        }
    ],

    "JavaScript": [

        {
            "name": "To-Do Application",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript"
            ],
            "topics": [
                "Variables",
                "Functions",
                "Arrays",
                "DOM",
                "Events",
                "Local Storage"
            ],
            "process": [
                "Create HTML interface",
                "Style application",
                "Create task input",
                "Add tasks",
                "Display tasks",
                "Implement completion",
                "Implement deletion",
                "Store tasks locally"
            ]
        },

        {
            "name": "Weather Dashboard",
            "technologies": [
                "HTML",
                "CSS",
                "JavaScript",
                "Weather API"
            ],
            "topics": [
                "JavaScript",
                "DOM",
                "APIs",
                "JSON",
                "Async programming"
            ],
            "process": [
                "Create weather interface",
                "Create search input",
                "Connect weather API",
                "Send city request",
                "Read JSON response",
                "Display weather",
                "Handle invalid cities"
            ]
        }
    ],

    "SQL": [

        {
            "name": "Student Database System",
            "technologies": [
                "SQL",
                "SQLite",
                "Python"
            ],
            "topics": [
                "Database design",
                "Tables",
                "Primary keys",
                "Foreign keys",
                "SELECT",
                "INSERT",
                "UPDATE",
                "DELETE",
                "JOIN"
            ],
            "process": [
                "Design student tables",
                "Create database",
                "Create primary keys",
                "Insert records",
                "Write SELECT queries",
                "Update records",
                "Delete records",
                "Create JOIN queries",
                "Generate reports"
            ]
        },

        {
            "name": "Online Shopping Database",
            "technologies": [
                "SQL",
                "MySQL",
                "Database Design"
            ],
            "topics": [
                "Customers",
                "Products",
                "Orders",
                "Relationships",
                "Primary keys",
                "Foreign keys",
                "JOIN"
            ],
            "process": [
                "Design customer table",
                "Design product table",
                "Design order table",
                "Create relationships",
                "Insert sample data",
                "Write queries",
                "Create JOIN queries",
                "Generate sales reports"
            ]
        }
    ],

    "Data Science": [

        {
            "name": "Student Performance Analysis",
            "technologies": [
                "Python",
                "Pandas",
                "NumPy",
                "Matplotlib"
            ],
            "topics": [
                "Data loading",
                "Data cleaning",
                "Pandas",
                "Statistics",
                "Visualization",
                "EDA"
            ],
            "process": [
                "Collect student data",
                "Load dataset",
                "Clean missing values",
                "Analyze marks",
                "Calculate averages",
                "Identify weak subjects",
                "Create charts",
                "Find patterns",
                "Prepare report"
            ]
        },

        {
            "name": "House Price Prediction",
            "technologies": [
                "Python",
                "Pandas",
                "NumPy",
                "Scikit-learn",
                "Matplotlib"
            ],
            "topics": [
                "Data preprocessing",
                "Statistics",
                "Feature selection",
                "Regression",
                "Model training",
                "Evaluation"
            ],
            "process": [
                "Collect house price data",
                "Load dataset",
                "Clean data",
                "Select features",
                "Split data",
                "Train regression model",
                "Evaluate model",
                "Predict prices",
                "Visualize results"
            ]
        }
    ]
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_user():

    if not st.session_state.user_id:
        return None

    return get_user(
        st.session_state.user_id
    )


def get_all_assessment_results(user_id):

    return get_assessment_results(user_id)


def get_overall_skill_scores(user_id):

    results = get_all_assessment_results(user_id)

    skill_scores = {}

    for skill, score, created_at in results:

        if skill not in skill_scores:
            skill_scores[skill] = []

        skill_scores[skill].append(
            float(score)
        )

    overall_scores = {}

    for skill, scores in skill_scores.items():

        if scores:

            overall_scores[skill] = round(
                sum(scores) / len(scores),
                2
            )

    return overall_scores


def get_skill_status(score):

    if score >= 80:
        return "Strong"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Needs Improvement"

    return "Weak"


def get_gap_details(skill, score):

    if score >= 80:

        return {
            "level": "Minor Gap",
            "message": f"You are strong in {skill}. Focus on advanced topics.",
            "points": [
                "Strengthen advanced concepts",
                "Practice real-world problems",
                "Build advanced projects",
                "Practice interview-level questions",
                "Improve project architecture"
            ]
        }

    if score >= 60:

        return {
            "level": "Moderate Gap",
            "message": f"You have a good foundation in {skill}.",
            "points": [
                "Strengthen intermediate concepts",
                "Practice problem-solving",
                "Build practical projects",
                "Review difficult topics",
                "Improve consistency"
            ]
        }

    if score >= 40:

        return {
            "level": "Significant Gap",
            "message": f"You need more practice in {skill}.",
            "points": [
                "Revise fundamental concepts",
                "Practice basic concepts regularly",
                "Practice intermediate concepts gradually",
                "Solve more exercises",
                "Build a beginner-level project",
                "Review previous mistakes"
            ]
        }

    return {
        "level": "High Gap",
        "message": f"{skill} requires significant improvement.",
        "points": [
            "Start with fundamentals",
            "Learn basic concepts step by step",
            "Practice simple examples",
            "Solve beginner exercises",
            "Build a small project",
            "Review concepts regularly",
            "Gradually move to intermediate topics"
        ]
    }


def get_recommended_careers(user_id):

    scores = get_overall_skill_scores(user_id)

    recommendations = []

    for skill, score in scores.items():

        career_list = CAREERS.get(
            skill,
            []
        )

        for career in career_list:

            recommendations.append(
                {
                    "career": career,
                    "skill": skill,
                    "score": score
                }
            )

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return recommendations


def get_recommended_projects(user_id):

    scores = get_overall_skill_scores(user_id)

    projects = []

    for skill, score in scores.items():

        project_list = PROJECTS.get(
            skill,
            []
        )

        for project in project_list:

            projects.append(
                {
                    "project": project,
                    "skill": skill,
                    "score": score
                }
            )

    projects.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return projects


# ============================================================
# LOGIN PAGE
# ============================================================

def show_login():

    st.title("🎓 CareerAI")

    st.subheader(
        "AI-Powered Career Guidance Platform"
    )

    st.write(
        "Assess your skills, identify gaps, "
        "follow a personalized roadmap and discover suitable careers."
    )

    st.divider()

    tab1, tab2 = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )

    with tab1:

        st.subheader("Welcome Back")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                user = login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True

                    st.session_state.user_id = user[0]

                    st.session_state.user_name = user[1]

                    st.session_state.page = "Dashboard"

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

    with tab2:

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email Address",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill all required fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        message
                    )

                else:

                    st.error(
                        message
                    )


# ============================================================
# SIDEBAR
# ============================================================

def show_sidebar():

    with st.sidebar:

        st.markdown(
            "# 🎓 CareerAI"
        )

        st.caption(
            "Smart Career Guidance"
        )

        st.divider()

        st.markdown(
            f"### 👋 Hello, {st.session_state.user_name}"
        )

        st.divider()

        menu_items = [

            ("🏠 Dashboard", "Dashboard"),

            ("📝 Skill Assessment", "Skill Assessment"),

            ("📊 Assessment Result", "Assessment Result"),

            ("🔍 Skill Gap", "Skill Gap"),

            ("🚀 Roadmap", "Roadmap"),

            ("💼 Career Recommendations",
             "Career Recommendations"),

            ("📁 Project Recommendations",
             "Project Recommendations"),

            ("📚 History", "History"),

            ("👤 Profile", "Profile")
        ]

        for label, page_name in menu_items:

            if st.button(
                label,
                key=f"sidebar_{page_name}",
                use_container_width=True
            ):

                st.session_state.page = page_name

                st.rerun()

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.user_id = None

            st.session_state.user_name = ""

            st.session_state.page = "Login"

            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    st.title(
        "🏠 CareerAI Dashboard"
    )

    st.write(
        f"Welcome back, **{st.session_state.user_name}**!"
    )

    scores = get_overall_skill_scores(
        st.session_state.user_id
    )

    results = get_all_assessment_results(
        st.session_state.user_id
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Skills Assessed",
            len(scores)
        )

    with col2:

        st.metric(
            "Assessments",
            len(results)
        )

    with col3:

        if scores:

            average = sum(
                scores.values()
            ) / len(scores)

        else:

            average = 0

        st.metric(
            "Average Score",
            f"{average:.1f}%"
        )

    with col4:

        if scores:

            strongest = max(
                scores,
                key=scores.get
            )

        else:

            strongest = "None"

        st.metric(
            "Strongest Skill",
            strongest
        )

    st.divider()

    st.subheader(
        "✨ Career Development Center"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="dashboard-card">

            <h3>📝 Skill Assessment</h3>

            <p>
            Test your knowledge with 10 randomly selected questions.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Start Assessment",
            key="dashboard_assessment",
            use_container_width=True
        ):

            st.session_state.page = "Skill Assessment"

            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="dashboard-card">

            <h3>🔍 Skill Gap</h3>

            <p>
            Discover the areas where you need more practice.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "View Skill Gap",
            key="dashboard_gap",
            use_container_width=True
        ):

            st.session_state.page = "Skill Gap"

            st.rerun()

    st.divider()

    st.subheader(
        "🧭 Explore Your Career Path"
    )

    option = st.selectbox(
        "Choose an option",
        [
            "Skill Gap",
            "Roadmap",
            "Career Recommendations",
            "Project Recommendations",
            "Assessment History"
        ]
    )

    if st.button(
        "Open Selected Section",
        use_container_width=True
    ):

        if option == "Assessment History":

            st.session_state.page = "History"

        else:

            st.session_state.page = option

        st.rerun()

    st.divider()

    if scores:

        st.subheader(
            "📈 Your Skills"
        )

        for skill, score in sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        ):

            col1, col2 = st.columns(
                [3, 1]
            )

            with col1:

                st.write(
                    f"**{skill}**"
                )

                st.progress(
                    min(score / 100, 1.0)
                )

            with col2:

                st.metric(
                    "Score",
                    f"{score:.1f}%"
                )

    else:

        st.info(
            "Complete your first assessment to start your career journey."
        )


# ============================================================
# SKILL ASSESSMENT
# ============================================================

def show_skill_assessment():

    st.title("📝 Skill Assessment")

    if not st.session_state.assessment_started:

        st.write(
            "Choose a skill and complete a 10-question assessment."
        )

        skill = st.selectbox(
            "Select Skill",
            list(QUESTION_BANK.keys())
        )

        st.info(
            "Each assessment contains 10 randomly selected questions."
        )

        if st.button(
            "🚀 Start Assessment",
            use_container_width=True
        ):

            question_bank = QUESTION_BANK[skill]

            selected_questions = random.sample(
                question_bank,
                min(10, len(question_bank))
            )

            st.session_state.assessment_questions = (
                selected_questions
            )

            st.session_state.assessment_answers = {}

            st.session_state.assessment_index = 0

            st.session_state.assessment_started = True

            st.session_state.current_assessment_skill = skill

            st.rerun()

        return

    questions = st.session_state.assessment_questions

    current_index = st.session_state.assessment_index

    total_questions = len(questions)

    if current_index >= total_questions:

        submit_assessment()

        return

    question = questions[current_index]

    st.progress(
        (current_index + 1) / total_questions
    )

    st.write(
        f"Question **{current_index + 1}** of **{total_questions}**"
    )

    st.markdown(
        f"""
        <div class="question-card">

        <h3>
        {question["question"]}
        </h3>

        <p>
        Difficulty:
        <strong>{question["level"]}</strong>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ANSWER OPTIONS
    # --------------------------------------------------------

    option_list = [
        "Select an answer..."
    ] + question["options"]

    previous_answer = st.session_state.assessment_answers.get(
        current_index,
        "Select an answer..."
    )

    try:
        default_index = option_list.index(previous_answer)
    except ValueError:
        default_index = 0

    selected_answer = st.radio(
        "Choose your answer",
        option_list,
        index=default_index,
        key=f"question_{current_index}"
    )

    # Save only a real answer
    if selected_answer != "Select an answer...":

        st.session_state.assessment_answers[
            current_index
        ] = selected_answer

    elif current_index in st.session_state.assessment_answers:

        del st.session_state.assessment_answers[
            current_index
        ]

    st.write("")

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if current_index > 0:

            if st.button(
                "⬅️ Previous",
                use_container_width=True
            ):

                st.session_state.assessment_index -= 1

                st.rerun()

    with col2:

        if current_index < total_questions - 1:

            if st.button(
                "Next Question ➡️",
                use_container_width=True
            ):

                if selected_answer == "Select an answer...":

                    st.warning(
                        "Please select an answer before continuing."
                    )

                else:

                    st.session_state.assessment_index += 1

                    st.rerun()

        else:

            if st.button(
                "✅ Submit Assessment",
                use_container_width=True
            ):

                if selected_answer == "Select an answer...":

                    st.warning(
                        "Please select an answer before submitting."
                    )

                else:

                    # Make sure the current answer is saved
                    st.session_state.assessment_answers[
                        current_index
                    ] = selected_answer

                    submit_assessment()
# ============================================================
# SUBMIT ASSESSMENT
# ============================================================

def submit_assessment():

    questions = st.session_state.assessment_questions

    answers = st.session_state.assessment_answers

    correct = 0

    for index, question in enumerate(questions):

        user_answer = answers.get(
            index,
            ""
        )

        if user_answer == question["answer"]:

            correct += 1

    total = len(questions)

    percentage = round(
        (correct / total) * 100,
        2
    )

    skill = st.session_state.get(
        "current_assessment_skill",
        "Python"
    )

    # Save review information
    st.session_state.review_questions = (
        questions.copy()
    )

    st.session_state.review_answers = (
        answers.copy()
    )

    st.session_state.review_skill = skill

    st.session_state.review_score = percentage

    # Save assessment
    save_assessment_result(
        st.session_state.user_id,
        skill,
        percentage
    )

    # Save career history
    careers = CAREERS.get(
        skill,
        []
    )

    if careers:

        save_career_recommendation(
            st.session_state.user_id,
            careers[0]["name"],
            percentage
        )

    # Reset current assessment
    st.session_state.assessment_started = False

    st.session_state.assessment_questions = []

    st.session_state.assessment_answers = {}

    st.session_state.assessment_index = 0

    st.session_state.last_assessment_id = True

    # Go to REVIEW first
    st.session_state.page = "Assessment Review"

    st.rerun()


# ============================================================
# ASSESSMENT REVIEW
# ============================================================

def show_assessment_review():

    st.title(
        "📝 Assessment Review"
    )

    questions = st.session_state.review_questions

    answers = st.session_state.review_answers

    skill = st.session_state.review_skill

    score = float(
        st.session_state.review_score
    )

    if not questions:

        st.info(
            "No assessment review is available."
        )

        if st.button(
            "Take Skill Assessment",
            use_container_width=True
        ):

            st.session_state.page = "Skill Assessment"

            st.rerun()

        return

    st.write(
        f"Review your answers for the **{skill}** assessment."
    )

    st.divider()

    correct_count = 0

    for index, question in enumerate(questions):

        user_answer = answers.get(
            index,
            "Not answered"
        )

        if user_answer == question["answer"]:

            correct_count += 1

    total_questions = len(questions)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Skill",
            skill
        )

    with col2:

        st.metric(
            "Correct Answers",
            f"{correct_count}/{total_questions}"
        )

    with col3:

        st.metric(
            "Score",
            f"{score:.2f}%"
        )

    st.divider()

    st.subheader(
        "🔍 Detailed Answer Review"
    )

    for index, question in enumerate(questions):

        user_answer = answers.get(
            index,
            "Not answered"
        )

        correct_answer = question["answer"]

        is_correct = (
            user_answer == correct_answer
        )

        if is_correct:

            title = (
                f"Question {index + 1}  •  ✅ Correct"
            )

        else:

            title = (
                f"Question {index + 1}  •  ❌ Incorrect"
            )

        with st.expander(
            title,
            expanded=False
        ):

            st.markdown(
                f"### {question['question']}"
            )

            st.write(
                f"**Difficulty:** {question['level']}"
            )

            st.write(
                f"**Your Answer:** {user_answer}"
            )

            if is_correct:

                st.success(
                    f"Correct Answer: {correct_answer}"
                )

            else:

                st.error(
                    f"Correct Answer: {correct_answer}"
                )

    st.divider()

    st.subheader(
        "📊 Performance Summary"
    )

    if score >= 80:

        st.success(
            f"Excellent! You scored {score:.2f}% in {skill}. "
            "You have a strong foundation and can move toward advanced topics."
        )

    elif score >= 60:

        st.info(
            f"Good work! You scored {score:.2f}% in {skill}. "
            "Focus on intermediate concepts and practical projects."
        )

    elif score >= 40:

        st.warning(
            f"You scored {score:.2f}% in {skill}. "
            "Review the fundamentals and practice more questions."
        )

    else:

        st.error(
            f"You scored {score:.2f}% in {skill}. "
            "Start with the fundamentals and practice step by step."
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📊 View Assessment Result",
            use_container_width=True
        ):

            st.session_state.page = "Assessment Result"

            st.rerun()

    with col2:

        if st.button(
            "📉 View Skill Gap",
            use_container_width=True
        ):

            st.session_state.page = "Skill Gap"

            st.rerun()


# ============================================================
# ASSESSMENT RESULT
# ============================================================

def show_assessment_result():

    st.title(
        "📊 Assessment Result"
    )

    results = get_all_assessment_results(
        st.session_state.user_id
    )

    if not results:

        st.info(
            "Complete an assessment to see your result."
        )

        return

    latest_skill = results[0][0]

    latest_score = float(
        results[0][1]
    )

    st.markdown(
        f"""
        <div class="score-card">

        <h1>{latest_score:.2f}%</h1>

        <h3>{latest_skill} Assessment</h3>

        <p>Your latest assessment score</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if latest_score >= 80:

        st.success(
            "Excellent performance!"
        )

    elif latest_score >= 60:

        st.info(
            "Good performance. Keep improving!"
        )

    elif latest_score >= 40:

        st.warning(
            "You have a foundation, but more practice is needed."
        )

    else:

        st.error(
            "Focus on fundamentals and practice regularly."
        )

    st.divider()

    st.subheader(
        "📈 Overall Skill Performance"
    )

    scores = get_overall_skill_scores(
        st.session_state.user_id
    )

    for skill, score in sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.write(
                f"**{skill}**"
            )

            st.progress(
                min(score / 100, 1.0)
            )

        with col2:

            st.write(
                f"**{score:.1f}%**"
            )

    st.divider()

    if st.button(
        "📝 Review Latest Assessment",
        use_container_width=True
    ):

        st.session_state.page = "Assessment Review"

        st.rerun()


# ============================================================
# SKILL GAP
# ============================================================

def show_skill_gap():

    st.title(
        "🔍 Skill Gap Analysis"
    )

    scores = get_overall_skill_scores(
        st.session_state.user_id
    )

    if not scores:

        st.info(
            "Complete at least one assessment to generate your Skill Gap Analysis."
        )

        return

    st.write(
        "Your skill gaps are calculated using your complete assessment history."
    )

    st.divider()

    sorted_skills = sorted(
        scores.items(),
        key=lambda item: item[1]
    )

    for skill, score in sorted_skills:

        score = float(score)

        status = get_skill_status(
            score
        )

        gap = get_gap_details(
            skill,
            score
        )

        with st.container():

            st.markdown(
                f"""
                <div class="gap-card">

                <h2>📚 {skill}</h2>

                <p>
                <strong>Overall Score:</strong>
                {score:.2f}%
                </p>

                <p>
                <strong>Status:</strong>
                {status}
                </p>

                <p>
                <strong>Gap Level:</strong>
                {gap["level"]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                min(score / 100, 1.0)
            )

            st.subheader(
                "🎯 Gap Points"
            )

            for point_index, point in enumerate(
                gap["points"]
            ):

                st.markdown(
                    f"""
                    <div class="gap-point">
                    🎯 {point}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.subheader(
                "🚀 Recommended Action"
            )

            if score >= 80:

                st.success(
                    f"You are strong in {skill}. "
                    "Focus on advanced topics, real-world projects and interviews."
                )

            elif score >= 60:

                st.info(
                    f"You have a good foundation in {skill}. "
                    "Focus on intermediate concepts and practical projects."
                )

            elif score >= 40:

                st.warning(
                    f"You need more practice in {skill}. "
                    "Revise fundamentals and build projects."
                )

            else:

                st.error(
                    f"{skill} requires significant improvement. "
                    "Start with fundamentals and practice step by step."
                )

        st.divider()


# ============================================================
# ROADMAP
# ============================================================

def show_roadmap():

    st.title(
        "🚀 Personalized Learning Roadmap"
    )

    scores = get_overall_skill_scores(
        st.session_state.user_id
    )

    if not scores:

        st.info(
            "Complete an assessment first to generate your roadmap."
        )

        return

    st.write(
        "Your roadmap is prioritized using your assessment history."
    )

    st.divider()

    for skill, score in sorted(
        scores.items(),
        key=lambda item: item[1]
    ):

        career_list = CAREERS.get(
            skill,
            []
        )

        st.subheader(
            f"📚 {skill} — {score:.1f}%"
        )

        if not career_list:

            st.info(
                "No roadmap is available for this skill yet."
            )

            continue

        career = career_list[0]

        for index, step in enumerate(
            career["process"],
            start=1
        ):

            st.markdown(
                f"""
                <div class="roadmap-card">

                <strong>
                Step {index}
                </strong>

                <br>

                {step}

                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()


# ============================================================
# CAREER RECOMMENDATIONS
# ============================================================

def show_career_recommendations():

    st.title(
        "💼 Career Recommendations"
    )

    recommendations = get_recommended_careers(
        st.session_state.user_id
    )

    if not recommendations:

        st.info(
            "Complete an assessment to receive career recommendations."
        )

        return

    st.write(
        "These recommendations are based on your complete assessment history."
    )

    st.divider()

    shown = set()

    for item in recommendations:

        career = item["career"]

        career_name = career["name"]

        if career_name in shown:

            continue

        shown.add(career_name)

        score = item["score"]

        st.markdown(
            f"""
            <div class="career-card">

            <h2>💼 {career_name}</h2>

            <p>
            <strong>Based on:</strong>
            {item["skill"]}
            </p>

            <p>
            <strong>Skill Score:</strong>
            {score:.1f}%
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "🛠 Technologies"
        )

        st.write(
            " • ".join(
                career["technologies"]
            )
        )

        st.subheader(
            "📚 Important Topics"
        )

        for topic in career["topics"]:

            st.write(
                f"• {topic}"
            )

        st.subheader(
            "🧭 Career Process"
        )

        for index, step in enumerate(
            career["process"],
            start=1
        ):

            st.write(
                f"**{index}.** {step}"
            )

        st.divider()


# ============================================================
# PROJECT RECOMMENDATIONS
# ============================================================

def show_project_recommendations():

    st.title(
        "📁 Project Recommendations"
    )

    projects = get_recommended_projects(
        st.session_state.user_id
    )

    if not projects:

        st.info(
            "Complete an assessment to receive project recommendations."
        )

        return

    st.write(
        "Recommended projects are based on your complete assessment history."
    )

    st.divider()

    shown = set()

    for item in projects:

        project = item["project"]

        project_name = project["name"]

        if project_name in shown:

            continue

        shown.add(project_name)

        st.markdown(
            f"""
            <div class="project-card">

            <h2>📁 {project_name}</h2>

            <p>
            <strong>Related Skill:</strong>
            {item["skill"]}
            </p>

            <p>
            <strong>Skill Score:</strong>
            {item["score"]:.1f}%
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "🛠 Technologies"
        )

        st.write(
            " • ".join(
                project["technologies"]
            )
        )

        st.subheader(
            "📚 Topics"
        )

        for topic in project["topics"]:

            st.write(
                f"• {topic}"
            )

        st.subheader(
            "🚀 Project Development Process"
        )

        for index, step in enumerate(
            project["process"],
            start=1
        ):

            st.write(
                f"**{index}.** {step}"
            )

        st.divider()


# ============================================================
# HISTORY
# ============================================================

def show_history():

    st.title(
        "📚 Assessment History"
    )

    results = get_all_assessment_results(
        st.session_state.user_id
    )

    if not results:

        st.info(
            "No assessment history available."
        )

        return

    st.write(
        "Your previous assessment results are shown below."
    )

    st.divider()

    for index, result in enumerate(
        results,
        start=1
    ):

        skill = result[0]

        score = float(
            result[1]
        )

        created_at = result[2]

        if score >= 80:

            status = "🟢 Strong"

        elif score >= 60:

            status = "🔵 Good"

        elif score >= 40:

            status = "🟡 Needs Improvement"

        else:

            status = "🔴 Weak"

        with st.expander(
            f"{index}. {skill} — {score:.1f}% — {status}"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Skill",
                    skill
                )

            with col2:

                st.metric(
                    "Score",
                    f"{score:.1f}%"
                )

            with col3:

                st.write(
                    "**Date**"
                )

                st.write(
                    created_at
                )


# ============================================================
# PROFILE
# ============================================================

def show_profile():

    st.title(
        "👤 Profile"
    )

    user = get_current_user()

    if not user:

        st.error(
            "Unable to load profile."
        )

        return

    user_id = user[0]

    name = user[1]

    email = user[2]

    education = user[3]

    skills = user[4]

    interests = user[5]

    st.subheader(
        "Personal Information"
    )

    st.write(
        f"**Name:** {name}"
    )

    st.write(
        f"**Email:** {email}"
    )

    st.divider()

    st.subheader(
        "Career Information"
    )

    education_input = st.text_area(
        "Education",
        value=education
    )

    skills_input = st.text_area(
        "Skills",
        value=skills
    )

    interests_input = st.text_area(
        "Interests",
        value=interests
    )

    if st.button(
        "💾 Save Profile",
        use_container_width=True
    ):

        update_profile(
            user_id,
            education_input,
            skills_input,
            interests_input
        )

        st.success(
            "Profile updated successfully."
        )

        st.rerun()


# ============================================================
# MAIN APPLICATION ROUTING
# ============================================================

if not st.session_state.logged_in:

    show_login()

else:

    show_sidebar()

    if st.session_state.page == "Dashboard":

        show_dashboard()

    elif st.session_state.page == "Skill Assessment":

        show_skill_assessment()

    elif st.session_state.page == "Assessment Review":

        show_assessment_review()

    elif st.session_state.page == "Assessment Result":

        show_assessment_result()

    elif st.session_state.page == "Skill Gap":

        show_skill_gap()

    elif st.session_state.page == "Roadmap":

        show_roadmap()

    elif st.session_state.page == "Career Recommendations":

        show_career_recommendations()

    elif st.session_state.page == "Project Recommendations":

        show_project_recommendations()

    elif st.session_state.page == "History":

        show_history()

    elif st.session_state.page == "Profile":

        show_profile()

    else:

        show_dashboard()