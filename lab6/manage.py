from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/mydb'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your routes and other Flask configurations here.
if __name__ == '__main__':
    app.run(debug=True)
