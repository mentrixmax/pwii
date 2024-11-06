
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    name = request.args.get("name")
    age = request.args.get("age")
    if (name is not None and age is not None):
        return "Hello, "+name+" World!, yor age is: "+age
    return "Name and age is required!"

if __name__ == '__main__':
    app.run(debug=True)
