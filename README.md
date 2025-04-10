# api-despesas-python-03

# 1. Introdução:

## Descrição geral do projeto

Este projeto de gerenciamento de gastos tem como objetivo ser uma ferramenta personalizada para controle financeiro pessoal. O usuário pode registrar receitas e despesas, e categorizá-las a fim de acompanhar o fluxo de caixa.

## Funcionalidades do sistema:

- **Registro de transações**: inserção de dados como data, valor, descrição e categoria.
- **Categorização**: classificação de despesas em categorias como alimentação, transporte, lazer, etc.

## Tecnologias utilizadas:

- **Python**
- **PostgreSQL**

## Objetivo da API:

- Controle de gastos pessoais.

# 2. Arquitetura do Sistema:

Diagrama de Classes:
![Diagrama de Classes](imagens/Diagrama_de_Classes_API.png)

Diagrama de Caso de Uso:
![Diagrama de Caso de Uso](imagens/Caso1-Novo_Usuario.png)
![Diagrama de Caso de Uso](imagens/Caso2-Usuario_Existente.png)

# 3. Estrutura de Banco de Dados:

Diagrama de Relacionamento de Entidades:
![Diagrama de Relacionamento](imagens/Relacionamento.png)

# 4. EndPoints da API:

Documentação dos principais endpoints (incluindo método HTTP, URL, parâmetros, e exemplo de resposta).

| Método | URL                           | Descrição          |
| ------ | ----------------------------- | ------------------ |
| POST   | http://localhost:8081/usuario | Cadastra o usuário |
| GET    | http://localhost:8081/usuario | Lista o usuário    |
| PUT    |                               | Atualiza o usuário |
| DELETE |                               | Remove o usuário   |

POST /usuario: Cria um usuario.

GET /usuario: Lista usuarios existentes.

# 5. Autenticação:

# 6. Validação de Dados:

# 7. Como rodar o projeto:

1- Inicia o ambiente virtual (venv)\
`python3 -m venv venv`

2- Ativa o ambiente virtual\
Linux:\
`source venv/bin/activate`\
Windows:\
`venv/Scripts/activate`

3- Instala as dependências para o projeto\
`pip install -r requirements.txt`

4- Define a variável de ambiente FLASK_APP com o valor app.py\
`export FLASK_APP=app.py`
ou `set FLASK_APP=app.py`

5- Executa o flask\
`flask run`

6- acesse o link pelo navegador\
http://127.0.0.1:5000/usuario

# 8. Testes:
