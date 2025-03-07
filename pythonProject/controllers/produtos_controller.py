from flask_login import login_required
from main import app
from flask import render_template, request


@app.route('/produtos', methods=['GET'])
@login_required
def produtos():
    return render_template("produto/listProdutos.html")
