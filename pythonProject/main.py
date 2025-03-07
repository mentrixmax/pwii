from flask import Flask
app = Flask(__name__)
app.secret_key="mateus"

from controllers.usuario_controller import *
from controllers.produtos_controller import *
from controllers.tipo_produto_controller import *
from models.Conexao import  *
from flask_login import LoginManager

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine )
    db = SessionLocal()
    return db.get(User,int(user_id))


if __name__ == '__main__':
    app.run(debug=True)