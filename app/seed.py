from faker import Faker
from app import create_app, db
from models import Restaurant, Pizza, RestaurantPizza

fake = Faker()

#Create an application context
app = create_app()
app.app_context().push()

def create_seed_data():
    with app.app_context():
        # Create a sample data
        for _ in range(3):
            restaurant = Restaurant(name=fake.company())
            pizza = Pizza(name=fake.word())

            # Add restaurant and pizza to the session
            db.session.add(restaurant)
            db.session.add(pizza)
            
            # Commit the changes to get the IDs
            db.session.commit()

            # Create restaurant_pizza with correct IDs
            restaurant_pizza = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id)

            # Add restaurant_pizza to the session
            db.session.add(restaurant_pizza)

        # Commit the changes
        db.session.commit()


if __name__ == '__main__':
    create_seed_data()


