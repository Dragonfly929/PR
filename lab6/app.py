from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from models.electro_scooter import ElectroScooter
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)

    # Configure SQLAlchemy to use SQLite
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

    # PostgresSql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/mydb'

    db.init_app(app)

    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Flask Swagger UI"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###

    # @app.errorhandler(400)
    # def handle_400_error(_error):
    #     """Return a http 400 error to the client"""
    #     return make_response(jsonify({'error': 'Misunderstood'}), 400)
    #
    # @app.errorhandler(401)
    # def handle_401_error(_error):
    #     """Return a http 401 error to the client"""
    #     return make_response(jsonify({'error': 'Unauthorised'}), 401)

    # @app.errorhandler(404)
    # def handle_404_error(_error):
    #     """Return a http 404 error to the client"""
    #     return make_response(jsonify({'error': 'Not found'}), 404)

    # @app.errorhandler(500)
    # def handle_500_error(_error):
    #     """Return a http 500 error to the client"""
    #     return make_response(jsonify({'error': 'Server error'}), 500)

    # Initialize Swagger
    Swagger(app)

    return app

if __name__ == "__main__":
    app = create_app()
    import routes

    app.run()
