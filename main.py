from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'skrivnost'
db = TinyDB('db.json')
users_table = db.table('users')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users_table.get(Query().username == username):
            return "Uporabnik že obstaja."
        users_table.insert({
            'username': username,
            'password': generate_password_hash(password),
        })
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_table.get(Query().username == username)
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect('/')
        return "Prijava neuspešna."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
