from main import app
from flask import render_template, request
from models.User import *
from models.Conexao import *
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
def users():
    return render_template("usuario/listUsers.html")

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
        return render_template("dashboard.html")
    except Exception as e:
        print(e)
        return render_template("usuario/sign-up.html",msg="Já existe um usuário")