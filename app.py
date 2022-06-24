"""Imports
"""
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, UsuarioRegistro
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def cria_banco():
    """Inicia o banco de dados no primeiro request
    """
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/usuarios/<string:usuario_id>')
api.add_resource(UsuarioRegistro, '/cadastro')


if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True)
