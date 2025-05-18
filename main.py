from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from db import init_db, register_user, login_user, get_user, add_comment, get_comments, delete_comment
from car_data import get_cars_by_criteria, get_car_details, rate_car, get_car_ratings
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    budget = request.form.get('budget')
    car_type = request.form.get('car_type')
    fuel_type = request.form.get('fuel_type')
    car_age = request.form.get('car_age')
    market = request.form.get('market')
    
    cars = get_cars_by_criteria(budget, car_type, fuel_type, car_age, market)
    
    return render_template('results.html', cars=cars)

@app.route('/car/<car_id>')
def car_detail(car_id):
    car = get_car_details(car_id)
    comments = get_comments(car_id)
    ratings = get_car_ratings(car_id)
    
    avg_rating = 0
    if ratings:
        avg_rating = sum(rating['rating'] for rating in ratings) / len(ratings)
    
    return render_template('car_detail.html', car=car, comments=comments, avg_rating=round(avg_rating, 1))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_code = request.form.get('admin_code')
        
        is_admin = False
        if admin_code:
            if admin_code == "Mila":
                is_admin = True
            else:
                flash('Napačna admin koda!', 'error')
                return render_template('register.html')
        
        if register_user(username, password, is_admin):
            flash('Registracija uspešna! Sedaj se lahko prijavite.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Uporabniško ime že obstaja!', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Prijava uspešna!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Napačno uporabniško ime ali geslo!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Odjava uspešna!', 'success')
    return redirect(url_for('index'))

@app.route('/add_comment', methods=['POST'])
def add_comment_route():
    if 'user_id' not in session:
        flash('Za komentiranje se morate prijaviti!', 'error')
        return redirect(url_for('login'))
    
    car_id = request.form.get('car_id')
    comment_text = request.form.get('comment')
    user_id = session['user_id']
    username = session['username']
    
    add_comment(car_id, user_id, username, comment_text)
    
    flash('Komentar uspešno dodan!', 'success')
    return redirect(url_for('car_detail', car_id=car_id))

@app.route('/rate_car', methods=['POST'])
def rate_car_route():
    if 'user_id' not in session:
        flash('Za ocenjevanje se morate prijaviti!', 'error')
        return redirect(url_for('login'))
    
    car_id = request.form.get('car_id')
    rating = int(request.form.get('rating'))
    user_id = session['user_id']
    
    rate_car(car_id, user_id, rating)
    
    flash('Ocena uspešno dodana!', 'success')
    return redirect(url_for('car_detail', car_id=car_id))

@app.route('/delete_comment/<comment_id>/<car_id>')
def delete_comment_route(comment_id, car_id):
    if 'user_id' not in session or not session['is_admin']:
        flash('Za brisanje komentarjev potrebujete admin pravice!', 'error')
        return redirect(url_for('car_detail', car_id=car_id))
    
    delete_comment(comment_id)
    
    flash('Komentar uspešno izbrisan!', 'success')
    return redirect(url_for('car_detail', car_id=car_id))

if __name__ == '__main__':
    app.run(debug=True)
