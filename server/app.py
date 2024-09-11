#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
class Home(Resource):
    def get(self):
        response_body = {
            'message' : 'Welcome to the RESTful API',
        }
        response = make_response(
            response_body,
            200
        )
        return response
api.add_resource(Home, '/') 

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]

        response = make_response(
            plants,
            200
        )
        return response
    
    def post(self):
        json_data = request.get_json()
        new_plant = Plant(
            name = json_data.get('name'),
            image = json_data.get('image'),
            price = json_data.get('price'),
        )
        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()

        response = make_response(
            response_dict,
            201
        )
        return response
    
api.add_resource(Plants, '/plants')
    
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by( id = id).first().to_dict()

        response = make_response(
            plant,
            200
        )
        return response
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
