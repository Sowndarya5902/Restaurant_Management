from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_session import Session

app = Flask(__name__)

app.secret_key = '12345'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

ADMIN_CREDENTIALS = {
    'Admin': 'xxx',
    'key1': '1234'
}

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS hotel(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           mail TEXT NOT NULL,
           phone TEXT NOT NULL,
           address TEXT NOT NULL)""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mail = request.form['mail']
    phone = request.form['phone']
    address = request.form['address']

    # Connect to the database and save the appointment
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO hotel (name, mail, phone, address) VALUES (?, ?, ?, ?)", (name, mail, phone, address))
    conn.commit()
    conn.close()

    flash('Order placed successfully!')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['logged_in'] = True
            flash('Successfully logged in')
            return redirect(url_for('result'))
        else:
            flash('Invalid credentials, please try again')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/result')
def result():
    if not session.get('logged_in'):
        flash('You need to log in to access this page')
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hotel')
    data = cursor.fetchall()
    conn.close()
    return render_template('result.html', data=data)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True, host='0.0.0.0', port=8000)
