from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # You can use any database here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # if object changed and not saved to DB
# This will turn off Flask_SQLAlchemy, it does not effect SQLAlchemy library tracking
app.secret_key = 'jose'  # Secret phrase
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # will create new endpoint "/auth"

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # To prvent the next line from running on import
    from db import db  # Import SQLAlchemy here to avoid "circular import"
    db.init_app(app)
    app.run(port=5000, debug=True)  # Start the Flask app & Server & Enable debug mode
