import traceback
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.usuario import UsuarioModel


args = reqparse.RequestParser()
args.add_argument("login", type=str, required=True, help="Campo login obrigatório!")
args.add_argument("senha", type=str, required=True, help="Campo senha obrigatório!")
args.add_argument("email", type=str)
args.add_argument("ativado", type=bool, help="Campo ativado obrigatório!")


class Usuario(Resource):
    """Usuario class"""

    def get(self, usuario_id):
        """Método GET que retorna um usuario pelo ID

        Args:
            usuario_id (string): ID do usuario para retornar

        Returns:
            dict: Usuario encontrado
        """
        usuario = UsuarioModel.find_usuario(usuario_id)
        if usuario:
            return usuario.to_json()
        return {"message": "Usuário não encontrado"}, 404  # HTTP Status CODE: Not Found

    @jwt_required()
    def delete(self, usuario_id):
        """Método DELETE para deletar um usuario

        Args:
            usuario_id (string): ID do usuario para deletar

        Returns:
            dict: Usuario encontrado
        """
        usuario = UsuarioModel.find_usuario(usuario_id)
        if usuario:
            try:
                usuario.delete_usuario()
            except:
                return {"message": "Falha ao deletar usuário!"}, 500
            return {"message": "Usuário removido"}, 200

        return {"message": "Usuário não encontrado"}, 404


class UsuarioRegistro(Resource):
    """UsuarioRegistro class"""

    def post(self):
        """Método responsável por cadastrar um novo usuário"""
        dados = args.parse_args()
        if not dados.get("email") or dados.get("email") is None:
            return {"message": "Campo email obrigatório!"}, 400

        if UsuarioModel.find_by_email(dados.get("email")):
            return {"message": "Email já está em utilização!"}, 400

        # valida de ja existe o usuário
        if UsuarioModel.find_by_login(dados["login"]):
            return {"message": "Login {} já existe!".format(dados["login"])}

        usuario = UsuarioModel(**dados)
        usuario.ativado = False
        try:
            usuario.save_usuario()
            usuario.send_confirmation_email()
        except:
            usuario.delete_usuario()
            traceback.print_exc()  # printa o erro no console
            return {"message": "Internal Server Error!"}, 500
        return {"message": "Cadastro realizado com sucesso!"}, 201


class UsuarioLogin(Resource):
    """UsuarioLogin class"""

    @classmethod
    def post(cls):
        """Método responsável pelo login de um usuário"""
        dados = args.parse_args()

        usuario = UsuarioModel.find_by_login(dados["login"])

        if usuario and safe_str_cmp(usuario.senha, dados["senha"]):
            if usuario.ativado:
                token = create_access_token(identity=usuario.usuario_id)
                return {"access_token": token}, 200
            return {"message": "Email não confirmado!"}, 400
        return {"message": "Login ou senha incorreto!"}, 401


class UsuarioLogout(Resource):
    """UsuarioLogout class"""

    @jwt_required()
    def post(self):
        """Método responsável pelo logout de um usuário"""
        jwt_id = get_jwt()["jti"]  # JWT Token Identifier
        BLACKLIST.add(jwt_id)

        return {"message": "Logout realizado com sucesso!"}, 200


class UsuarioConfirmar(Resource):
    """UsuarioConfirmar class"""

    @classmethod
    def get(cls, usuario_id):
        """Método responsável por confirmar um usuário

        Args:
            usuario_id (string): ID do usuário
        """
        usuario = UsuarioModel.find_usuario(usuario_id)
        if not usuario:
            return {"message": "Usuário {} não encontrado!".format(usuario_id)}, 404

        usuario.ativado = True
        usuario.save_usuario()
        return {"message": "Usuário confirmado com sucesso!"}, 200
