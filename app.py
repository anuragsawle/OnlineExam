from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Required for session management

# --- Database Configuration ---
db_config = {
    'host': '192.168.31.236',
    'user': 'Anurag',  # Change if your username is different
    'password': 'Anurag@123',  # <--- PUT YOUR MYSQL PASSWORD HERE
    'database': 'quiz_app'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


# --- Quiz Data (Hardcoded for simplicity) ---
QUESTIONS = [
    {
        "id": 1,
        "question": "Which SQL statement is used to extract data from a database?",
        "options": ["GET", "OPEN", "SELECT", "EXTRACT"],
        "answer": "SELECT"
    },
    {
        "id": 2,
        "question": "Which key is used to uniquely identify a record in a table?",
        "options": ["Primary Key", "Foreign Key", "Unique Key", "Super Key"],
        "answer": "Primary Key"
    },
    {
        "id": 3,
        "question": "What does DDL stand for?",
        "options": ["Data Definition Language", "Data Derivation Language", "Dynamic Data Language",
                    "Detailed Data Language"],
        "answer": "Data Definition Language"
    }
]


# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    name = request.form.get('student_name')
    student_class = request.form.get('student_class')
    if not name or not student_class:
        return redirect(url_for('index'))
    session['student_name'] = name
    session['student_class'] = student_class
    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    if 'student_name' not in session:
        return redirect(url_for('index'))
    return render_template('quiz.html', questions=QUESTIONS, name=session['student_name'])


CURRENT_TEST_ID = "SQL-101"


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'student_name' not in session:
        return redirect(url_for('index'))

    score = 0
    for q in QUESTIONS:
        user_answer = request.form.get(f"q_{q['id']}")
        if user_answer == q['answer']:
            score += 1

    # Save to Database with TEST ID
    conn = get_db_connection()
    cursor = conn.cursor()

    # UPDATED QUERY: Added test_id and student_class
    query = """
        INSERT INTO attempts (test_id, student_name, student_class, score, total_questions) 
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (CURRENT_TEST_ID, session['student_name'], session.get('student_class', 'Unknown'), score, len(QUESTIONS)))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('result.html', score=score, total=len(QUESTIONS), name=session['student_name'])

# --- Teacher Portal Routes ---

@app.route('/teacher')
def teacher_login():
    return render_template('teacher_login.html')


@app.route('/teacher_auth', methods=['POST'])
def teacher_auth():
    password = request.form.get('password')
    # Simple hardcoded password for demonstration
    if password == "admin123":
        session['is_teacher'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('teacher_login.html', error="Invalid Password")


@app.route('/dashboard')
def dashboard():
    if not session.get('is_teacher'):
        return redirect(url_for('teacher_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attempts ORDER BY timestamp DESC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('dashboard.html', results=results)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)