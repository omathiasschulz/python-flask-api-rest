"""Models
"""
from sql_alchemy import banco


class HotelModel(banco.Model):
    """HotelModel class
    """
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=2))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        """HotelModel constructor

        Args:
            hotel_id (string): ID do hotel
            nome (string): Nome do hotel
            estrelas (float): Avaliação do hotel
            diaria (float): Diária do hotel
            cidade (string): Cidade do hotel
        """
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def to_json(self):
        """Converte o model hotel para um JSON

        Returns:
            dict: Hotel
        """
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        """Método responsável por buscar um hotel no database a partir do ID

        Args:
            hotel_id (string): ID do hotel
        """
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        """Método responsável por salvar um novo hotel no database
        """
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        """Método responsável por alterar um hotel no database
        """
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        """Método responsável por remover um hotel
        """
        banco.session.delete(self)
        banco.session.commit()
