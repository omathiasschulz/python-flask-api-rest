"""SQL
"""
import sqlite3

connection = sqlite3.connect('banco.database')
cursor = connection.cursor()

cria_tabela = 'create table if not exists hoteis (\
    id text primary key,\
    nome text,\
    estrelas real,\
    diaria real,\
    cidade text\
)'
cursor.execute(cria_tabela)

cria_hotel = "insert into hoteis values (\
    '5', 'Schulz Filial 06', 4.3, 350.99, 'Lontras'\
)"
cursor.execute(cria_hotel)

connection.commit()
connection.close()
