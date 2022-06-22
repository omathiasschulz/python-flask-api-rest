"""Resources
"""
from flask_restful import Resource, reqparse
from models.hotel import HotelModel

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

    args = reqparse.RequestParser()
    # argumentos permitidos
    args.add_argument('nome')
    args.add_argument('estrelas')
    args.add_argument('diaria')
    args.add_argument('cidade')

    def find_hotel(self, hotel_id):
        """Método que retorna um hotel pelo ID

        Args:
            hotel_id (string): ID do hotel para retornar

        Returns:
            dict: Hotel encontrado ou None
        """
        for hotel in hoteis:
            if hotel['id'] == hotel_id:
                return hotel

        return None

    def get(self, hotel_id):
        """Método GET que retorna um hotel pelo ID

        Args:
            hotel_id (string): ID do hotel para retornar

        Returns:
            dict: Hotel encontrado
        """
        hotel = self.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {
            'message': 'Hotel não encontrado'
        }, 404  # HTTP Status CODE: Not Found

    def post(self, hotel_id):
        """Método POST que cadastra um novo hotel

        Args:
            hotel_id (string): ID do hotel para cadastrar

        Returns:
            dict: Hotel encontrado
        """
        dados = self.args.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        # é um objeto e converte para json/dict
        novo_hotel = novo_hotel.to_json()
        hoteis.append(novo_hotel)

        return novo_hotel, 201  # HTTP Status CODE: Success

    def put(self, hotel_id):
        """Método PUT para alterar um hotel

        Args:
            hotel_id (string): ID do hotel para cadastrar

        Returns:
            dict: Hotel encontrado
        """
        dados = self.args.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        # é um objeto e converte para json/dict
        novo_hotel = novo_hotel.to_json()

        hotel = self.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200  # HTTP Status CODE: Success

        hoteis.append(novo_hotel)
        return novo_hotel, 201  # HTTP Status CODE: Created

    def delete(self, hotel_id):
        """Método DELETE para deletar um hotel

        Args:
            hotel_id (string): ID do hotel para deletar

        Returns:
            dict: Hotel encontrado
        """
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['id'] != hotel_id]

        return {
            'message': 'Hotel removido'
        }, 200  # HTTP Status CODE: Not Found
