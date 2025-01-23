from main import app
from flask import render_template, request

@app.route('/tipoprodutos', methods=['GET'])
def tipoprodutos():
    return render_template("tipoproduto/listTipoProdutos.html")
