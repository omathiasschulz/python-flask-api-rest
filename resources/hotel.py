"""Resources
"""
import sqlite3
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


def normalize_path_params(
    cidade=None,
    estrelas_min=0,
    estrelas_max=5,
    diaria_min=0,
    diaria_max=10000,
    limit=50,
    offset=0,
    **dados
):
    """Normaliza os parametros enviados no request
    """
    if cidade:
        return {
            'cidade': cidade,
            'estrelas_max': estrelas_max,
            'estrelas_min': estrelas_min,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset,
        }
    return {
        'estrelas_max': estrelas_max,
        'estrelas_min': estrelas_min,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset,
    }


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    """Hoteis class
    """

    def get(self):
        """Método GET que retorna todos os hotéis existentes

        Returns:
            dict: Todos os hoteis cadastrados
        """
        connection = sqlite3.connect('banco.database')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}

        parametros = normalize_path_params(**dados_validos)

        print('parametros')
        print(parametros)

        if not parametros.get('cidade'):
            consulta = 'select * from hoteis \
                where (estrelas > ? and estrelas < ?) \
                and (diaria > ? and diaria < ?) \
                limit ? offset ?'
        else:
            consulta = 'select * from hoteis \
                where (estrelas > ? and estrelas < ?) \
                and (diaria > ? and diaria < ?) \
                and cidade = ? \
                limit ? offset ?'

        # pega os valores sem chave
        data = tuple([parametros[chave] for chave in parametros])
        resultado = cursor.execute(consulta, data)

        print('resultado')
        print(resultado)

        hoteis = []
        for linha in resultado:
            print('linha')
            print(linha)
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
            })

        return {
            'hoteis': hoteis,
        }


class Hotel(Resource):
    """Hotel class
    """

    args = reqparse.RequestParser()
    # argumentos permitidos
    args.add_argument('nome', type=str, required=True,
                      help="Campo nome obrigatório!")
    args.add_argument('estrelas', type=float, required=True,
                      help="Campo estrelas obrigatório!")
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

    @jwt_required()
    def post(self, hotel_id):
        """Método POST que cadastra um novo hotel

        Args:
            hotel_id (string): ID do hotel para cadastrar

        Returns:
            dict: Hotel encontrado
        """
        if HotelModel.find_hotel(hotel_id):
            return {'message': "Hotel ID {} já existe".format(hotel_id)}, 400

        dados = self.args.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Falha ao salvar hotel!'}, 500
        return hotel.to_json(), 201  # HTTP Status CODE: Success

    @jwt_required()
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
            return {'message': 'Falha ao salvar hotel!'}, 500
        return hotel.to_json(), 201  # HTTP Status CODE: Created

    @jwt_required()
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
                return {'message': 'Falha ao deletar hotel!'}, 500
            return {
                'message': 'Hotel removido'
            }, 200

        return {
            'message': 'Hotel não encontrado'
        }, 404
