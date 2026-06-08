from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "secretkey"

model = load_model("sql_injection_cnn_model.h5", compile=False)

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

labels = ['Error-Based', 'None_Type', 'Time-Based', 'Union-Based',
          'boolean-based', 'meta_based', 'stackqueries_based']

with open("model_settings.pkl", "rb") as f:
    settings = pickle.load(f)

max_len = settings["max_len"]

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        query TEXT,
        result TEXT,
        attack_type TEXT,
        confidence_score TEXT,
        timestamp TEXT
        
                   
    )
    """)

    conn.commit()
    conn.close()

init_db()
# after imports and setup, before routes

def fix_labels():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE logs SET attack_type='Error-Based' WHERE attack_type='Error-based'")
    cursor.execute("UPDATE logs SET attack_type='Stacked-Queries-Based' WHERE attack_type='stackqueries_based'")

    conn.commit()
    conn.close()

fix_labels()   # 👈 call it once


def save_log(username, query, result, attack_type, confidence):
    # ✅ Standardize attack names
    attack_map = {
    "error-based": "Error-Based",
    "Error-based": "Error-Based",
    "error_based": "Error-Based",

    "stackqueries_based": "Stacked-Queries-Based",
    "stacked-queries-based": "Stacked-Queries-Based",

    "union-based": "Union-Based",
    "boolean-based": "Boolean-Based",
    "time-based": "Time-Based",
    "meta-based": "Meta-Based",
    "none-type": "None-type"
    }

    # Convert to standard format
    attack_type = attack_map.get(attack_type, attack_type)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO logs (username, query, result, attack_type, confidence_score, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
""", (username, query, result, attack_type, confidence, timestamp))

    conn.commit()
    conn.close()

# LOGIN PAGE
@app.route('/')
def login():
    return render_template('login.html')

# REGISTER PAGE
@app.route('/register')
def register():
    return render_template('register.html')

# HANDLE REGISTER
@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return render_template('register.html', error="Username already exists. Please choose another one.")

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return redirect('/')

# HANDLE LOGIN
@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session['user'] = username
        return redirect('/dashboard')
    else:
        return render_template('login.html', error="Incorrect username or password.")

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT attack_type, COUNT(*)
            FROM logs
            WHERE username=?
            GROUP BY attack_type
        """, (session['user'],))

        chart_data = cursor.fetchall()
        print("CHART DATA:", chart_data)
        conn.close()

        labels = [row[0] for row in chart_data]
        values = [row[1] for row in chart_data]

        print("LABELS:", labels)
        print("VALUES:", values)

        return render_template(
            'dashboard.html',
            user=session['user'],
            labels=labels,
            values=values
        )

    return redirect('/')
# DETECTION PAGE
@app.route('/detect')
def detect():
    if 'user' in session:
        return render_template('detect.html')
    return redirect('/')

def normalize_attack_type(attack_type):
    label_map = {
        "None_Type": "None-Type",
        "None-type": "None-Type",
        "none_type": "None-Type",
        "Error-Based": "Error-Based",
        "Time-Based": "Time-Based",
        "Union-Based": "Union-Based",
        "boolean-based": "Boolean-Based",
        "Boolean-Based": "Boolean-Based",
        "meta_based": "Meta-Based",
        "Meta-Based": "Meta-Based",
        "stackqueries_based": "Stacked-Queries-Based",
        "Stacked-Queries-Based": "Stacked-Queries-Based"
    }

    return label_map.get(attack_type, attack_type)

def classify_attack(query):
    seq = tokenizer.texts_to_sequences([query])
    padded = pad_sequences(seq, maxlen=max_len, padding='post', truncating='post')

    prediction = model.predict(padded)
    predicted_index = prediction.argmax(axis=1)[0]
    confidence = float(prediction[0][predicted_index])

    attack_type = normalize_attack_type(labels[predicted_index])

    return attack_type, round(confidence, 2)

# HANDLE QUERY (TEMP LOGIC)
@app.route('/predict', methods=['POST'])
def predict():
    query = request.form['query']

    try:
        attack_type, confidence = classify_attack(query)

        if attack_type == "None-Type":
            result = "Safe Query"
        else:
            result = "SQL Injection Detected"

    except Exception:
        result = "Safe Query"
        attack_type = "None_Type"
        confidence = 0.0

    save_log(session['user'], query, result, attack_type, confidence)

    return render_template(
        'result.html',
        query=query,
        result=result,
        attack_type=attack_type,
        confidence=confidence
    )

@app.route('/logs')
def logs():
    if 'user' in session:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
    SELECT query, result, attack_type, confidence_score, timestamp
    FROM logs
    WHERE username=?
    ORDER BY id DESC
""", (session['user'],))
        data = cursor.fetchall()

        conn.close()

        return render_template('logs.html', logs=data)

    return redirect('/')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)