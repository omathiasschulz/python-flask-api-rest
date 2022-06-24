"""Models
"""
from sql_alchemy import banco


class UsuarioModel(banco.Model):
    """UsuarioModel class
    """
    __tablename__ = 'usuarios'

    usuario_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        """UsuarioModel constructor

        Args:
            login (string): Login do usuário
            senha (float): Senha do usuário
        """
        self.login = login
        self.senha = senha

    def to_json(self):
        """Converte o model usuario para um JSON

        Returns:
            dict: Usuario
        """
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
        }

    @classmethod
    def find_usuario(cls, usuario_id):
        """Método responsável por buscar um usuario no database a partir do ID

        Args:
            usuario (string): ID do usuario
        """
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_by_login(cls, login):
        """Método responsável por buscar um usuario no database a partir do login

        Args:
            usuario (string): ID do usuario
        """
        usuario = cls.query.filter_by(login=login).first()
        if usuario:
            return usuario
        return None

    def save_usuario(self):
        """Método responsável por salvar um usuario
        """
        banco.session.add(self)
        banco.session.commit()

    def delete_usuario(self):
        """Método responsável por remover um usuario
        """
        banco.session.delete(self)
        banco.session.commit()
