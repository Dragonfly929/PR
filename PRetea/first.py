from flask import Flask, request

app = Flask(__name__)
@app.route("/Hello")
def hello():
    return "Hello world"

app.run()