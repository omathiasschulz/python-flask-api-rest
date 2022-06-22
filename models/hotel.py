"""Models
"""


class HotelModel:
    """HotelModel class
    """

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
            'id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
        }
