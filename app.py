from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy, declarative_base
from flask_migrate import Migrate
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Mirav:postgres@localhost:5432/cars_api'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"


@app.route('/status', methods=['GET'])
def status():
    return {'Status': 'UP'}


@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {"id": car.id,
             "name": car.name,
             "model": car.model,
             "doors": car.doors
             } for car in cars]

        return {"count": len(results), "cars": results}


@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_specific_car(car_id):
    car = CarsModel.query.get_or_404(car_id)
    print(car)

    if request.method == 'GET':
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return {"message": "success", "car": response}

    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return {"message": f"Car {car.name} successfully deleted."}


@app.route('/doors/<total>', methods=['GET'])
def door_limit(total):
    cars = CarsModel.query.filter(CarsModel.doors == total).all()
    print('-----return --{0}'.format(cars))

    results = [
        {"id": car.id,
         "name": car.name,
         } for car in cars]

    return {"cars": results}


if __name__ == "__main__":
    app.run(debug=True)
