"""Imports
"""
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


hoteis = [
    {
        'id': 1,
        'nome': 'Schulz Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Ibirama',
    },
    {
        'id': 2,
        'nome': 'Schulz Hotel Filial 01',
        'estrelas': 5,
        'diaria': 480.99,
        'cidade': 'Rio do Sul',
    },
    {
        'id': 3,
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
        """
        return {
            'hoteis': hoteis,
        }


api.add_resource(Hoteis, '/hoteis')

if __name__ == '__main__':
    app.run(debug=True)
