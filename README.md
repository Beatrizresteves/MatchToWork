# MatchToWork

## Requisitos

- Python 3.8+
- Flask
- psycopg2
- PostgreSQL

## Configuração

### Instalação das Dependências

Primeiro, crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate
```
Instale as dependências:

```bash
pip install Flask psycopg2-binary
```

Inicialização do Banco de Dados
Crie as tabelas necessárias executando o script de inicialização:
```bash
python db.py
```

Executando a Aplicação
```bash
python app.py
```
