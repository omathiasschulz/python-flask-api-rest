"""Resources
"""
from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel


class Usuario(Resource):
    """Usuario class
    """

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
        return {
            'message': 'Usuário não encontrado'
        }, 404  # HTTP Status CODE: Not Found

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
                return {'message': 'Falha ao deletar usuário!'}, 500
            return {
                'message': 'Usuário removido'
            }, 200

        return {
            'message': 'Usuário não encontrado'
        }, 404


class UsuarioRegistro(Resource):
    """UsuarioRegistro class
    """

    def post(self):
        """Método responsável por cadastrar um novo usuário
        """
        args = reqparse.RequestParser()
        args.add_argument('login', type=str, required=True, help="Campo login obrigatório!")
        args.add_argument('senha', type=str, required=True, help="Campo senha obrigatório!")
        dados = args.parse_args()

        # valida de ja existe o usuário
        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'Login {} já existe!'.format(dados['login'])}

        usuario = UsuarioModel(**dados)
        usuario.save_usuario()
        return {'message': 'Cadastro realizado com sucesso!'}, 201
