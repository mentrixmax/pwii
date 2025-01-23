from flask import Flask
app = Flask(__name__)

from controllers.usuario_controller import *
from controllers.produtos_controller import *
from controllers.tipo_produto_controller import *
from models.Conexao import  *
if __name__ == '__main__':
    app.run(debug=True)