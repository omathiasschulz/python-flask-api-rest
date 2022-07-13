from flask import request, url_for
from sql_alchemy import banco
from requests import post

MAILGUN_DOMAIN = "sandboxad628da248a0490fafb8580524fb3c8e.mailgun.org"
MAILGUN_API_KEY = "5d222a0eb063b1af857d4ebd6d918f9b-62916a6c-6cf37cd3"
FROM_TITLE = "NO-REPLY"
FROM_EMAIL = "no-reply@schulz.net.br"


class UsuarioModel(banco.Model):
    """UsuarioModel class"""

    __tablename__ = "usuarios"

    usuario_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(40), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        """UsuarioModel constructor

        Args:
            login (string): Login do usuário
            senha (float): Senha do usuário
            email (string): Email do usuário
            ativado (float): Determina se o usuário está ativado ou não
        """
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def to_json(self):
        """Converte o model usuario para um JSON

        Returns:
            dict: Usuario
        """
        return {
            "usuario_id": self.usuario_id,
            "login": self.login,
            "email": self.email,
            "ativado": self.ativado,
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

    @classmethod
    def find_by_email(cls, email):
        """Método responsável por buscar um usuario no database a partir do email

        Args:
            email (string): Wmail do usuario
        """
        usuario = cls.query.filter_by(email=email).first()
        if usuario:
            return usuario
        return None

    def save_usuario(self):
        """Método responsável por salvar um usuario"""
        banco.session.add(self)
        banco.session.commit()

    def delete_usuario(self):
        """Método responsável por remover um usuario"""
        banco.session.delete(self)
        banco.session.commit()

    def send_confirmation_email(self):
        """Método responsável por enviar um email para confirmação do email"""
        # remove a última / para quando concatenar URL não apresentar duas /
        link = request.url_root[:-1] + url_for(
            "usuarioconfirmar", usuario_id=self.usuario_id
        )
        return post(
            "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": "{} <{}>".format(FROM_TITLE, FROM_EMAIL),
                "to": self.email,
                "subject": "Confirmação de Cadastro",
                "text": "Confirme seu cadastro clicando no seguinte link: {}".format(
                    link
                ),
                "html": '<html><p>\
                Confirme seu cadastro clicando no seguinte link: <a href="{}">\
                CONFIRMAR EMAIL</a>\
                </p></html>'.format(
                    link
                ),
            },
        )
