"""Imports
"""
from flask_restful import Resource


hoteis = [
    {
        'id': '1',
        'nome': 'Schulz Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Ibirama',
    },
    {
        'id': '2',
        'nome': 'Schulz Hotel Filial 01',
        'estrelas': 5,
        'diaria': 480.99,
        'cidade': 'Rio do Sul',
    },
    {
        'id': '3',
        'nome': 'Schulz Hotel Filial 02',
        'estrelas': 4.3,
        'diaria': 320.34,
        'cidade': 'Ituporanga',
    },
]


class Hoteis(Resource):
    """Hoteis class
    """

    def get(self):
        """Método GET que retorna todos os hotéis existentes

        Returns:
            dict: Todos os hoteis cadastrados
        """
        return {
            'hoteis': hoteis,
        }


class Hotel(Resource):
    """Hotel class
    """

    def get(self, hotel_id):
        """Método GET que retorna um hotel pelo ID

        Args:
            hotel_id (string): ID do hotel para retornar

        Returns:
            dict: Hotel encontrado
        """
        for hotel in hoteis:
            if hotel['id'] == hotel_id:
                return hotel

        return {
            'message': 'Hotel não encontrado'
        }, 404  # HTTP Status CODE: Not Found
