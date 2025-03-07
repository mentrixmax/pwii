from flask_login import login_required
from main import app
from flask import render_template, request

@app.route('/tipoprodutos', methods=['GET'])
@login_required
def tipoprodutos():
    return render_template("tipoproduto/listTipoProdutos.html")
