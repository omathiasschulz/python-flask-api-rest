from flask_jwt_extended import JWTManager
from flask import Flask, jsonify, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import (
    Usuario,
    UsuarioConfirmar,
    UsuarioRegistro,
    UsuarioLogin,
    UsuarioLogout,
)
from resources.site import Sites, Site
from sql_alchemy import banco

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "IPhe4NuRn*hgrxPriGYX%8*2MZ"
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    """Inicia o banco de dados no primeiro request"""
    banco.create_all()


@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    """Método responsável por validar se token está na blacklist

    Args:
        token (dict): Token

    Returns:
        bool: Está na blacklist ou não
    """
    return token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def token_acesso_invalidado(jwt_header, jwt_payload):
    """Método responsável por retornar uma mensagem de erro quando usuário está deslogado
    e tentou acessar uma rotina que deve estar logado

    Returns:
        string: String no padrão JSON
    """
    return (
        jsonify({"message": "Você deve estar logado para realizar essa operação!"}),
        401,
    )


api.add_resource(Hoteis, "/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")
api.add_resource(Usuario, "/usuarios/<string:usuario_id>")
api.add_resource(UsuarioRegistro, "/cadastro")
api.add_resource(UsuarioLogin, "/login")
api.add_resource(UsuarioLogout, "/logout")
api.add_resource(Sites, "/sites")
api.add_resource(Site, "/sites/<string:url>")
api.add_resource(UsuarioConfirmar, "/confirmacao/<int:usuario_id>")


if __name__ == "__main__":
    banco.init_app(app)
    app.run(debug=True)
