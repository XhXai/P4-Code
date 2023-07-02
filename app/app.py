#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    migrate = Migrate(app, db)

    db.init_app(app)

    @app.route('/')
    def home():
        return ''
    
    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        data = [
            {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address
            }
            for restaurant in restaurants
        ]
        return jsonify(data)
    
    @app.route('/restaurant/<int:id>', methods=['GET'])
    def get_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [
                {
                    'id': pizza.id,
                    'name': pizza.name,
                }
                for pizza in restaurant.pizzas
            ]
        }
        return jsonify(data)
    
    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()

        return make_response('', 204)
    
    @app.route('/pizzas', methods=['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        data = [
            {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            }
            for pizza in pizzas
        ]
        return jsonify(data)
    
    @app.route('/restaurant_pizzas', method=['POST'])
    def create_restaurant_pizza():
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        if not price or not pizza_id or not restaurant_id:
            return jsonify({'errors': ['validation errors']}), 400
        
        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)

        if restaurant is None or pizza is None:
            return jsonify({'errors': ['validation errors']}), 400
        
        restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
        db.session.add(restaurant_pizza)
        db.session.commit()

        data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        return jsonify(data), 201

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(port=5555)
