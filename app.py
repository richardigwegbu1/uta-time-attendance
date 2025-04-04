from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'uta-secret'

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    is_admin INTEGER DEFAULT 0
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/attendance')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user'] = username
            session['is_admin'] = user[3]
            return redirect('/admin' if user[3] else '/attendance')
        else:
            msg = 'Invalid credentials'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect('database.db')
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            msg = 'Username already exists.'
    return render_template('register.html', msg=msg)

@app.route('/attendance')
def attendance():
    if 'user' not in session or session.get('is_admin'):
        return redirect('/login')
    return render_template('attendance.html')

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    if 'user' in session:
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO attendance (username, timestamp) VALUES (?, ?)",
                     (session['user'], datetime.now().isoformat()))
        conn.commit()
        conn.close()
    return redirect('/attendance')

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect('/login')
    conn = sqlite3.connect('database.db')
    rows = conn.execute("SELECT * FROM attendance ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template('admin.html', records=rows)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

