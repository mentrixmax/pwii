
from flask_login import login_required
from main import app
from flask import render_template, request, redirect, url_for

from models.Conexao import *
from models.User import *
@app.route('/produtos', methods=['GET'])
@login_required
def produtos():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    db = SessionLocal()

    '''p = Produto(descricao="Pao",preco=12.5,estoque=15, estmin=10)
    db.add(p)
    db.commit()'''
    
    
    # pegar os usuarios do BD
    listaProdutos = db.query(Produto).all()
    return render_template("produto/listProdutos.html",produtos=listaProdutos)

@app.route('/produtos/edit/<product_id>', methods=['GET'])
@login_required
def edit_products(product_id):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    db = SessionLocal()
    prd = db.query(Produto).get(int(product_id))
    db.close()
    return render_template("produto/editproduto.html",produto=prd)


@app.route('/produtos/delete/<product_id>', methods=['GET'])
@login_required
def delete_produto(product_id):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    db = SessionLocal()
    prd = db.query(Produto).get(int(product_id))
    db.delete(prd)
    db.commit()
    return redirect(url_for('produtos'))


@app.route('/produtos/save/<product_id>', methods=['POST'])
@login_required
def save_products(product_id):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    db = SessionLocal()
    prd = db.query(Produto).get(int(product_id))
    print(prd.id)
    prd.id = int(product_id)
    prd.descricao = request.form['descricao']
    prd.preco = float(request.form['preco'])
    prd.estoque = float(request.form['estoque'])
    prd.estoqueMinimo = float(request.form['estMin'])
    db.commit()
    return redirect(url_for('produtos'))

@app.route("/produtos/novo", methods=['GET'])
@login_required
def novo():
    return render_template("produto/new.html")

@app.route("/produtos/save", methods=['POST'])
@login_required
def novo_save():
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    db = SessionLocal()
    
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    estoque = float(request.form['estoque'])
    estoqueMinimo = float(request.form['estMin'])
    prd = Produto(descricao=descricao, preco=preco, estoque=estoque, estmin=estoqueMinimo)
    db.add(prd)
    db.commit()
    return redirect(url_for('produtos'))
    return render_template("produto/new.html")

