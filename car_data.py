import json
import uuid

cars = [
    {
        'id': 'c1',
        'brand': 'Volkswagen',
        'model': 'Golf',
        'year': 2020,
        'price': 18000,
        'type': 'practical',
        'fuel': 'diesel',
        'age': 'modern',
        'market': 'german',
        'image': 'https://via.placeholder.com/300x200?text=VW+Golf',
        'description': 'Volkswagen Golf je eden najpopularnejših avtomobilov v Evropi. Ta model ponuja odlično razmerje med kakovostjo in ceno.'
    },
    {
        'id': 'c2',
        'brand': 'BMW',
        'model': '3 Series',
        'year': 2021,
        'price': 32000,
        'type': 'sport',
        'fuel': 'petrol',
        'age': 'modern',
        'market': 'german',
        'image': 'https://via.placeholder.com/300x200?text=BMW+3+Series',
        'description': 'BMW serije 3 je dinamičen športni sedan, ki ponuja vrhunsko vozno izkušnjo in luksuz.'
    },
    {
        'id': 'c3',
        'brand': 'Renault',
        'model': 'Clio',
        'year': 2019,
        'price': 12000,
        'type': 'practical',
        'fuel': 'petrol',
        'age': 'modern',
        'market': 'slovenian',
        'image': 'https://via.placeholder.com/300x200?text=Renault+Clio',
        'description': 'Renault Clio je kompakten mestni avtomobil, ki je zelo priljubljen na slovenskem trgu.'
    },
    {
        'id': 'c4',
        'brand': 'Audi',
        'model': 'A5',
        'year': 2022,
        'price': 38000,
        'type': 'sport',
        'fuel': 'petrol',
        'age': 'modern',
        'market': 'german',
        'image': 'https://via.placeholder.com/300x200?text=Audi+A5',
        'description': 'Audi A5 je eleganten športni kupe, ki združuje luksuz in zmogljivost.'
    },
    {
        'id': 'c5',
        'brand': 'Toyota',
        'model': 'Yaris',
        'year': 2018,
        'price': 10000,
        'type': 'practical',
        'fuel': 'hybrid',
        'age': 'modern',
        'market': 'slovenian',
        'image': 'https://via.placeholder.com/300x200?text=Toyota+Yaris',
        'description': 'Toyota Yaris je zanesljiv mestni avtomobil z nizko porabo goriva.'
    },
    {
        'id': 'c6',
        'brand': 'Mercedes-Benz',
        'model': 'C-Class',
        'year': 2016,
        'price': 22000,
        'type': 'sport',
        'fuel': 'diesel',
        'age': 'older',
        'market': 'german',
        'image': 'https://via.placeholder.com/300x200?text=Mercedes+C-Class',
        'description': 'Mercedes-Benz C razred je luksuzni sedan nemške izdelave, ki ponuja udobje in prestiž.'
    },
    {
        'id': 'c7',
        'brand': 'Opel',
        'model': 'Corsa',
        'year': 2015,
        'price': 7000,
        'type': 'practical',
        'fuel': 'petrol',
        'age': 'older',
        'market': 'slovenian',
        'image': 'https://via.placeholder.com/300x200?text=Opel+Corsa',
        'description': 'Opel Corsa je zanesljiv in ekonomičen avtomobil, primeren za vsakodnevno vožnjo.'
    },
    {
        'id': 'c8',
        'brand': 'Porsche',
        'model': '911',
        'year': 2020,
        'price': 95000,
        'type': 'sport',
        'fuel': 'petrol',
        'age': 'modern',
        'market': 'german',
        'image': 'https://via.placeholder.com/300x200?text=Porsche+911',
        'description': 'Porsche 911 je ikoničen športni avtomobil, ki združuje tradicijo in najnovejšo tehnologijo.'
    },
    {
        'id': 'c9',
        'brand': 'Škoda',
        'model': 'Octavia',
        'year': 2019,
        'price': 17000,
        'type': 'practical',
        'fuel': 'diesel',
        'age': 'modern',
        'market': 'slovenian',
        'image': 'https://via.placeholder.com/300x200?text=Skoda+Octavia',
        'description': 'Škoda Octavia je prostoren in praktičen avtomobil, priljubljen na slovenskem trgu.'
    },
    {
        'id': 'c10',
        'brand': 'Mercedes-Benz',
        'model': 'E-Class',
        'year': 2015,
        'price': 25000,
        'type': 'practical',
        'fuel': 'diesel',
        'age': 'older',
        'market': 'german',
        'image': 'https://via.placeholder.com/300x200?text=Mercedes+E-Class',
        'description': 'Mercedes-Benz E razred je udoben in eleganten avto, primeren za daljše poti.'
    }
]

car_ratings = []

def get_cars_by_criteria(budget, car_type, fuel_type, car_age, market):
    """Vrne avtomobile po izbranih kriterijih."""
    max_budget = float(budget) if budget else float('inf')
    
    filtered_cars = []
    for car in cars:
        if car['price'] > max_budget:
            continue
        
        if car_type != 'any' and car['type'] != car_type:
            continue
            
        if fuel_type != 'any' and car['fuel'] != fuel_type:
            continue
            
        if car_age != 'any' and car['age'] != car_age:
            continue
            
        if market != 'any' and car['market'] != market:
            continue
            
        filtered_cars.append(car)
    
    return filtered_cars

def get_car_details(car_id):
    """Pridobi podrobnosti o avtomobilu iz "API-ja"."""
    for car in cars:
        if car['id'] == car_id:
            car_details = car.copy()
            
            if car['brand'] == 'Volkswagen':
                car_details['engine'] = '2.0 TDI'
                car_details['power'] = '150 HP'
                car_details['acceleration'] = '8.5s (0-100 km/h)'
                car_details['consumption'] = '5.2 l/100km'
            elif car['brand'] == 'BMW':
                car_details['engine'] = '2.0 Turbo'
                car_details['power'] = '190 HP'
                car_details['acceleration'] = '7.2s (0-100 km/h)'
                car_details['consumption'] = '6.8 l/100km'
            elif car['brand'] == 'Renault':
                car_details['engine'] = '1.2 TCe'
                car_details['power'] = '100 HP'
                car_details['acceleration'] = '10.8s (0-100 km/h)'
                car_details['consumption'] = '5.7 l/100km'
            else:
                car_details['engine'] = '2.0'
                car_details['power'] = '150 HP'
                car_details['acceleration'] = '9.0s (0-100 km/h)'
                car_details['consumption'] = '6.0 l/100km'
                
            return car_details
    return None

def rate_car(car_id, user_id, rating):
    """Doda ali posodobi oceno uporabnika za določen avto."""
    for idx, rate in enumerate(car_ratings):
        if rate['car_id'] == car_id and rate['user_id'] == user_id:
            car_ratings[idx]['rating'] = rating
            return
    car_ratings.append({
        'id': str(uuid.uuid4()),
        'car_id': car_id,
        'user_id': user_id,
        'rating': rating
    })

def get_car_ratings(car_id):
    """Vrne vse ocene za določen avto."""
    return [rating for rating in car_ratings if rating['car_id'] == car_id]

def get_car_technical_data(brand, model):
    technical_data = {
        'engine_type': 'Inline-4',
        'transmission': 'Automatic',
        'drive': 'Front-wheel drive',
        'weight': '1350 kg',
        'length': '4.3 m',
        'width': '1.8 m',
        'height': '1.5 m',
        'fuel_tank': '50 l',
        'trunk_capacity': '380 l',
    }
    
    return technical_data
