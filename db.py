from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

db = TinyDB('database.json')
users_table = db.table('users')
comments_table = db.table('comments')
ratings_table = db.table('ratings')

User = Query()
Comment = Query()
Rating = Query()

def init_db():
    """Inicializira bazo, če je potrebno."""
    if not users_table.search(User.is_admin == True):
        admin_id = str(uuid.uuid4())
        users_table.insert({
            'id': admin_id,
            'username': 'admin',
            'password': generate_password_hash('admin'),
            'is_admin': True
        })
        print("Admin uporabnik ustvarjen!")

def register_user(username, password, is_admin=False):
    """Registrira novega uporabnika."""
    if users_table.search(User.username == username):
        return False
    
    user_id = str(uuid.uuid4())
    users_table.insert({
        'id': user_id,
        'username': username,
        'password': generate_password_hash(password),
        'is_admin': is_admin
    })
    
    return True

def login_user(username, password):
    """Preveri uporabniške podatke in vrne uporabnika, če so podatki pravilni."""
    user = users_table.search(User.username == username)
    if user and check_password_hash(user[0]['password'], password):
        return user[0]
    return None

def get_user(user_id):
    """Vrne uporabnika glede na ID."""
    user = users_table.search(User.id == user_id)
    if user:
        return user[0]
    return None

def add_comment(car_id, user_id, username, comment_text):
    """Doda komentar za določen avto."""
    comment_id = str(uuid.uuid4())
    comments_table.insert({
        'id': comment_id,
        'car_id': car_id,
        'user_id': user_id,
        'username': username,
        'text': comment_text,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return comment_id

def get_comments(car_id):
    """Vrne vse komentarje za določen avto."""
    return comments_table.search(Comment.car_id == car_id)

def delete_comment(comment_id):
    """Izbriše komentar."""
    comments_table.remove(Comment.id == comment_id)

def rate_car(car_id, user_id, rating):
    """Doda ali posodobi oceno uporabnika za določen avto."""
    existing_rating = ratings_table.search((Rating.car_id == car_id) & (Rating.user_id == user_id))
    
    if existing_rating:
        ratings_table.update({'rating': rating}, (Rating.car_id == car_id) & (Rating.user_id == user_id))
    else:
        ratings_table.insert({
            'id': str(uuid.uuid4()),
            'car_id': car_id,
            'user_id': user_id,
            'rating': rating
        })

def get_car_ratings(car_id):
    """Vrne vse ocene za določen avto."""
    return ratings_table.search(Rating.car_id == car_id)
