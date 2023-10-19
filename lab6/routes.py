# routes.py
from __main__ import app
from flask import request, jsonify
from models.database import db
from flask import jsonify
from models.electro_scooter import ElectroScooter


@app.route('/api/electro-scooters', methods=['GET'])
def get_electro_scooters():
    # Query the database to retrieve all electro scooters
    scooters = ElectroScooter.query.all()

    # Convert the query results to a list of dictionaries
    electro_scooters = []
    for scooter in scooters:
        scooter_data = {
            "id": scooter.id,
            "name": scooter.name,
            "battery_level": scooter.battery_level
        }
        electro_scooters.append(scooter_data)
    return jsonify(electro_scooters)


# Update the API endpoint to accept JSON input
@app.route('/api/electro-scooters', methods=['POST'])
def create_electro_scooter():
    try:
        # Get data from the request body in JSON format
        data = request.get_json()

        # Validate and extract parameters
        name = data.get('name', "Default Name")
        battery_level = data.get('battery_level', 0.0)

        # Create a new Electro Scooter
        electro_scooter = ElectroScooter(name=name, battery_level=battery_level)

        # Add the Electro Scooter to the database
        db.session.add(electro_scooter)
        db.session.commit()

        return jsonify({"message": "Electro Scooter created successfully"}), 201

    except Exception as e:
        return jsonify({"error": "Invalid request data", "details": str(e)}), 400


# @app.route('/api/electro-scooters', methods=['POST'])
# def create_electro_scooter():
#     try:
#         # Get data from the request body
#         data = request.get_json()
#
#         # Validate and extract required parameters
#         name = data['name']
#         battery_level = data['battery_level']
#
#         # Create a new Electro Scooter
#         electro_scooter = ElectroScooter(name=name, battery_level=battery_level)
#
#         # Add the Electro Scooter to the database
#         db.session.add(electro_scooter)
#         db.session.commit()
#
#         return jsonify({"message": "Electro Scooter created successfully"}), 201
#
#     except KeyError:
#         return jsonify({"error": "Invalid request data"}), 400


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['GET'])
def get_electro_scooter_by_id(scooter_id):

    # Find the Electro Scooter by ID
    scooter = ElectroScooter.query.get(scooter_id)

    if scooter is not None:
        return jsonify({
            "id": scooter.id,
            "name": scooter.name,
            "battery_level": scooter.battery_level
        }), 200
    else:
        return jsonify({"error": "Electro Scooter not found"}), 404


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
def update_electro_scooter(scooter_id):
    try:
        # Find the Electro Scooter by ID
        scooter = ElectroScooter.query.get(scooter_id)

        if scooter is not None:
            # Get data from the request body
            data = request.get_json()

            # Update the Electro Scooter properties
            scooter.name = data.get('name', scooter.name)
            scooter.battery_level = data.get('battery_level', scooter.battery_level)
            db.session.commit()
            return jsonify({"message": "Electro Scooter updated successfully"}), 200
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
def delete_electro_scooter(scooter_id):
    try:
        # Find the Electro Scooter by ID
        scooter = ElectroScooter.query.get(scooter_id)

        if scooter is not None:
            # Get the password from the request headers
            password = request.headers.get('X-Auth-Token')
            # Check if the provided password is correct
            if password == 'password':  # Replace with your actual password
                db.session.delete(scooter)
                db.session.commit()
                return jsonify({"message": "Electro Scooter deleted successfully"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
