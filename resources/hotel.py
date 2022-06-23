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
            'hoteis': [hotel.to_json() for hotel in HotelModel.query.all()],
        }


class Hotel(Resource):
    """Hotel class
    """

    args = reqparse.RequestParser()
    # argumentos permitidos
    args.add_argument('nome', type=str, required=True, help="Campo nome obrigatório!")
    args.add_argument('estrelas', type=float, required=True, help="Campo estrelas obrigatório!")
    args.add_argument('diaria')
    args.add_argument('cidade')

    def get(self, hotel_id):
        """Método GET que retorna um hotel pelo ID

        Args:
            hotel_id (string): ID do hotel para retornar

        Returns:
            dict: Hotel encontrado
        """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.to_json()
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
        if HotelModel.find_hotel(hotel_id):
            return { 'message': "Hotel ID {} já existe".format(hotel_id) }, 400

        dados = self.args.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return { 'message': 'Falha ao salvar hotel!' }, 500
        return hotel.to_json(), 201  # HTTP Status CODE: Success

    def put(self, hotel_id):
        """Método PUT para alterar um hotel

        Args:
            hotel_id (string): ID do hotel para cadastrar

        Returns:
            dict: Hotel encontrado
        """
        dados = self.args.parse_args()

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return hotel.to_json(), 200  # HTTP Status CODE: Success

        # se não foi encontrado, cria o hotel
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return { 'message': 'Falha ao salvar hotel!' }, 500
        return hotel.to_json(), 201  # HTTP Status CODE: Created

    def delete(self, hotel_id):
        """Método DELETE para deletar um hotel

        Args:
            hotel_id (string): ID do hotel para deletar

        Returns:
            dict: Hotel encontrado
        """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return { 'message': 'Falha ao deletar hotel!' }, 500
            return {
                'message': 'Hotel removido'
            }, 200

        return {
            'message': 'Hotel não encontrato'
        }, 404
