from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')
users_table = db.table('uporabniki')

cars = [
    {"id": 1, "ime": "Volkswagen Golf", "tip": "kombilimuzina", "cena": 20000, "trg": ["Slovenija", "Tujina"], "sportnost": "sport", "modernost": "modern", "gorivo": "bencin", "druzinski": False},
    {"id": 2, "ime": "Škoda Octavia", "tip": "limuzina", "cena": 25000, "trg": ["Slovenija"], "sportnost": "space", "modernost": "modern", "gorivo": "dizel", "druzinski": True},
    {"id": 3, "ime": "Tesla Model 3", "tip": "električni", "cena": 40000, "trg": ["Tujina"], "sportnost": "sport", "modernost": "modern", "gorivo": "električni", "druzinski": True},
    {"id": 4, "ime": "Tesla Model 2", "tip": "električni", "cena": 50000, "trg": ["Tujina"], "sportnost": "space", "modernost": "modern", "gorivo": "električni", "druzinski": True}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_cars():
    data = request.json
    budget = int(data.get('budget', 0))
    sport_space = data.get('sportSpace', '')
    modern_old = data.get('modernOld', '')
    fuel = data.get('fuel', '')
    family = data.get('family', '')
    market = data.get('market', '')

    filtered = [c for c in cars if c['cena'] <= budget and
                (sport_space == '' or c['sportnost'] == sport_space) and
                (modern_old == '' or c['modernost'] == modern_old) and
                (fuel == '' or c['gorivo'] == fuel) and
                (market == '' or market in c['trg']) and
                (family == '' or (family == 'yes' and c['druzinski']) or (family == 'no' and not c['druzinski']))]

    return jsonify(filtered)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_code = request.form.get('admin_code', '')

        is_admin = admin_code == 'Mila'
        if admin_code and not is_admin:
            return "Napaka: Napačna admin koda!"

        if users_table.get(Query().username == username):
            return "Uporabnik že obstaja."

        users_table.insert({
            'username': username,
            'password': generate_password_hash(password),
            'is_admin': is_admin
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
            session['is_admin'] = user['is_admin']
            return redirect('/')
        return "Prijava neuspešna."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
