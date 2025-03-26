from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

cars = [
    {"ime": "Volkswagen Golf", "tip": "kombilimuzina", "cena": 20000, "razdalje": "kratke", "trg": ["Slovenija", "Tujina"], "sportnost": "sport", "modernost": "modern", "gorivo": "bencin"},
    {"ime": "Škoda Octavia", "tip": "limuzina", "cena": 25000, "druzinski": True, "razdalje": "dolge", "trg": ["Slovenija"], "sportnost": "space", "modernost": "modern", "gorivo": "dizel"},
    {"ime": "Tesla Model 3", "tip": "električni", "cena": 40000, "druzinski": True, "razdalje": "dolge", "trg": ["Tujina"], "sportnost": "sport", "modernost": "modern", "gorivo": "električni"},
    {"ime": "Tesla Model 2", "tip": "električni", "cena": 50000, "druzinski": True, "razdalje": "dolge", "trg": ["Tujina"], "sportnost": "space", "modernost": "modern", "gorivo": "električni"}
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

    filtered_cars = [car for car in cars if
                      car['cena'] <= budget and
                      (sport_space == '' or car['sportnost'] == sport_space) and
                      (modern_old == '' or car['modernost'] == modern_old) and
                      (fuel == '' or car['gorivo'] == fuel) and
                      (market == '' or market in car['trg']) and
                      (family == '' or (family == 'yes' and car['druzinski']) or (family == 'no' and not car['druzinski']))]
    
    return jsonify(filtered_cars)

if __name__ == '__main__':
    app.run(debug=True)
