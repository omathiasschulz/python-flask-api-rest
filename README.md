# python-flask-api-rest

API RESTful para cadastro de Hotéis com login de usuários e autenticação.

Esse projeto utiliza como base para construção o microframework `Flask` e foi realizado com base no curso da Udemy [REST APIs com Python e Flask](https://www.udemy.com/course/rest-apis-com-python-e-flask/)

## Rodar a aplicação

**Obs:** É necessário possui o Python na versão 3.8.10.

Criar um ambiente virtual chamado `venv`:

```bash
virtualenv venv
```

Ativar o ambiente virtual:

```bash
source venv/bin/activate
```

Instalar as dependências da aplicação:

```bash
pip install -r requirements.txt
```

Rodar a aplicação localmente:

```bash
python app.py
```

## Testar a aplicação

Para visualizar todas as rotas existentes nessa API e testar ela você pode importar no Insomnia o arquivo `sample/insomnia.json`.
