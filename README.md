API REST com FastAPI e Banco de Dados
📌 Sobre o projeto

Este projeto consiste no desenvolvimento de uma API REST utilizando Python e FastAPI, com integração a um banco de dados relacional e gerenciamento das tabelas através do SQLAlchemy e Alembic.

O objetivo da aplicação é demonstrar a criação de uma API estruturada seguindo boas práticas de desenvolvimento, incluindo organização de rotas, modelos de dados, migrações de banco e separação de responsabilidades.

🚀 Tecnologias utilizadas
Python
FastAPI - criação dos endpoints da API
SQLAlchemy - ORM para comunicação com o banco de dados
Alembic - gerenciamento das migrações do banco de dados
Uvicorn - servidor ASGI para execução da aplicação
SQLite/PostgreSQL - banco de dados relacional
📂 Estrutura do projeto
API/
│
├── main.py                 # Arquivo principal da aplicação
├── models.py               # Definição das tabelas e modelos do banco
├── database.py             # Configuração da conexão com o banco
├── schemas.py              # Modelos de validação dos dados
│
├── routes/
│   ├── auth_routes.py      # Rotas relacionadas à autenticação
│   └── order_routes.py     # Rotas relacionadas aos pedidos
│
├── alembic/
│   └── migrations/         # Histórico das alterações do banco
│
├── requirements.txt        # Dependências do projeto
└── README.md
🗄️ Modelagem do banco de dados

A criação do banco de dados foi realizada utilizando o SQLAlchemy, onde as tabelas foram definidas através dos modelos presentes no arquivo models.py.

Cada classe representa uma entidade do sistema e contém:

Nome da tabela no banco de dados;
Colunas e seus respectivos tipos;
Chaves primárias;
Relacionamentos entre entidades;
Restrições necessárias para garantir a integridade dos dados.

Para controlar a evolução da estrutura do banco foi utilizada a biblioteca Alembic.

O Alembic permite criar e aplicar migrações, registrando todas as alterações realizadas no banco de dados sem a necessidade de recriar as tabelas manualmente.

Fluxo utilizado:

models.py
     ↓
Alembic detecta alterações
     ↓
Criação da migration
     ↓
Aplicação no banco de dados
