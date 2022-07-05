"""Resources
"""
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    """Sites class
    """

    def get(self):
        """Método GET que retorna todos os sites existentes

        Returns:
            dict: Todos os sites cadastrados
        """

        return {
            'sites': [site.to_json() for site in SiteModel.query.all()],
        }


class Site(Resource):
    """Site class
    """

    def get(self, url):
        """Método GET que retorna um site

        Args:
            url (string): URL do site

        Returns:
            dict: Site encontrado
        """
        site = SiteModel.find_site(url)
        if site:
            return site.to_json()
        return {
            'message': 'Site não encontrado'
        }, 404  # HTTP Status CODE: Not Found

    @jwt_required()
    def post(self, url):
        """Método POST que cadastra um novo site

        Args:
            url (string): URL do site

        Returns:
            dict: Site encontrado
        """
        if SiteModel.find_site(url):
            return {'message': "Site {} já existe".format(url)}, 400

        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'Falha ao salvar site!'}, 500
        return site.to_json(), 201  # HTTP Status CODE: Success

    @jwt_required()
    def delete(self, url):
        """Método DELETE para deletar um site

        Args:
            url (string): URL do site

        Returns:
            dict: Site encontrado
        """
        site = SiteModel.find_site(url)
        if site:
            try:
                site.delete_site()
            except:
                return {'message': 'Falha ao deletar site!'}, 500
            return {
                'message': 'Site removido'
            }, 200

        return {
            'message': 'Site não encontrado'
        }, 404
