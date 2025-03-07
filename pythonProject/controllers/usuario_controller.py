from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.sql.functions import user

from main import app
from flask import flash, render_template, request, jsonify, redirect, url_for
from models.User import *
from models.Conexao import *
from datetime import datetime
import bcrypt
@app.route("/usuario/create")
def inserir():
    return "chegou na rota"

@app.route('/', methods=['GET'])
def login():
    # name = request.args.get("name")
    # age = request.args.get("age")
    #if (name is not None and age is not None):
    #     return "Hello, "+name+" World!, yor age is: "+age
    return render_template("usuario/sign-in.html")

@app.route('/dash', methods=['POST','GET'])
@login_required
def dash():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
           # print(login,password)
        if login == "a@a" and password == "1":
           return render_template("dashboard.html")
        else:
            return render_template("usuario/sign-in.html")
    else:
        return render_template("dashboard.html")


@app.route('/users', methods=['GET'])
@login_required
def users():
    # abrir a conexao
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    db = SessionLocal()
    # pegar os usuarios do BD
    listaUsu = db.query(User).all()
    db.close()
    #devolver pra view
    return render_template("usuario/listUsers.html",users=listaUsu)

@app.route('/users/create', methods=['GET'])
def create_users():
    return render_template("usuario/sign-up.html")

@app.route('/users/create', methods=['POST'])
def save_user():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    try:
        new_user = User(nome=nome,  senha=senha, email=email)
        # Cria um novo usuário no banco de dados
        db = SessionLocal()
        # Adiciona o novo usuário ao banco de dados
        db.add(new_user)
        db.commit()
        login_user(new_user)
        return render_template("dashboard.html")
    except Exception as e:
        print(e)
        return render_template("usuario/sign-up.html",msg="Já existe um usuário")


#metodo de login usando aplicação monolitica
@app.route('/login/do', methods=['POST'])
def login_do():
    # recuperando os dados do formulário,
    email = request.form['email']
    senha = request.form['senha']

    #abrindo conexão com o banco de dados.
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    #consultando no Banco de Dados se tem um usuário com aquele email.
    userDB = db.query(User).filter(User.email==email).first()

    # nao existe o usuário
    if userDB is None:
        return render_template("usuario/sign-in.html", msg="Usuário não existe")
    else:
        #usuário existe e eu vou verificar se a senha está valida.
        if bcrypt.checkpw(senha.encode('utf-8'),userDB.senha.encode('utf_8')):
            login_user(userDB, remember=True)
            return render_template("/dashboard.html")
        else:
            return render_template("usuario/sign-in.html", msg="Senha inválida")
           

#usando aplicao restful
@app.route('/login/do/restful', methods=['POST'])
def login_do_restful():
    #utilizando o try excpet para eliminar a possibilidade de háver uma exceção não tratada no codigo.
    try:
        #obtendo os dados do json do request.
        data = request.get_json()
        #verificando se todos os campos necessários estão vindo.
        if not data or 'username' not in data or 'password' not in data:
                return jsonify({"status": "error", "message": "Username e password são obrigatórios"}), 400
        #recotando os dados do json e colocando nas váriaveis locais.
        userName = data['username']
        senha = data['password']
        #abrindo bd
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        #consultando se o usuário exite.
        userDB = db.query(User).filter(User.email == userName).first()
       # verificando se a senha está valida e logando o usuário.
        if (userDB and userDB.senha == senha):
            return jsonify({"status": "success", "message": "Login bem-sucedido!"}), 200
        else:
            return jsonify({"status": "erro", "message": "Senha ou usuário errados!"}), 400
    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 400

@app.route('/users/delete/<user_id>', methods=['GET'])
@login_required
def delete_user(user_id):
   # abre a conexao
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
   #filtra pelo id
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return "Usuário nao encontrado", 404
    
    if user.id == current_user.id:
        return "Usuário logado nao pode ser deletado", 404
    
    db.delete(user)
    db.commit()

    listaUsu = db.query(User).all()
    db.close()
    # devolver pra view
    return redirect(url_for('users'))

@app.route('/users/pre-update/<user_id>', methods=['GET'])
@login_required
def pre_update_user(user_id):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return "Usuário nao encontrado", 404

    return render_template("/usuario/update.html", user=user)

@app.route('/users/update/', methods=['POST'])
@login_required
def update_user():
   #obtendo os dados que o usuário digitou
    user_id = int(request.form['user_id'])
    username = request.form['nome']
    userEmail = request.form['email']
    userFuncao = request.form['funcao']
    userData = request.form['data']
    data_obj = datetime.strptime(userData, "%Y-%m-%d")

#pegando dados do BD
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return "Usuário nao encontrado", 404
    #substituindo os dados
    user.nome  = username
    user.email = userEmail
    user.funcao = userFuncao
    user.dataContratacao = data_obj
   # db.update(user)
    db.commit()
    db.close()

    return redirect(url_for('users'))
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/profile")
@login_required
def profile():
    return render_template("usuario/update.html",user=current_user);