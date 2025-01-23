from main import app
from flask import render_template, request

@app.route('/produtos', methods=['GET'])
def produtos():
    return render_template("produto/listProdutos.html")
