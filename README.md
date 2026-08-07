🚀 API REST com FastAPI, SQLAlchemy e Alembic
📌 Descrição do Projeto

Este projeto consiste no desenvolvimento de uma API REST utilizando Python e FastAPI, com integração a banco de dados relacional e gerenciamento da estrutura do banco utilizando SQLAlchemy e Alembic.

O objetivo foi desenvolver uma aplicação backend aplicando boas práticas de organização de código, separação de responsabilidades e controle de evolução do banco de dados através de migrations.

🛠️ Tecnologias Utilizadas
🐍 Python
⚡ FastAPI — criação dos endpoints da API
🗄️ SQLAlchemy — ORM para comunicação com o banco de dados
🔄 Alembic — gerenciamento de migrações do banco
🚀 Uvicorn — servidor para execução da aplicação
💾 SQLite/PostgreSQL — armazenamento dos dados
📂 Estrutura do Projeto
API/
│
├── main.py                 # Inicialização da aplicação FastAPI
├── database.py             # Configuração da conexão com o banco
├── models.py               # Modelos e tabelas do banco de dados
├── schemas.py              # Validação e estrutura dos dados
│
├── routes/
│   ├── auth_routes.py      # Endpoints de autenticação
│   └── order_routes.py     # Endpoints relacionados aos pedidos
│
├── alembic/                # Controle das migrations do banco
│
├── requirements.txt        # Dependências do projeto
└── README.md
🗄️ Criação e Gerenciamento do Banco de Dados

A modelagem do banco de dados foi realizada utilizando o SQLAlchemy, onde as entidades do sistema foram definidas através dos modelos presentes no arquivo models.py.

Cada modelo representa uma tabela no banco de dados, contendo:

Definição das colunas;
Tipos de dados;
Chaves primárias;
Relacionamentos entre entidades;
Regras de integridade dos dados.

Para controlar as alterações na estrutura do banco foi utilizada a biblioteca Alembic.

O Alembic permite versionar as mudanças realizadas no banco através de migrations, evitando alterações manuais e garantindo maior organização durante o desenvolvimento.

Fluxo de atualização do banco:

Alteração no models.py
          ↓
Criação da migration com Alembic
          ↓
Aplicação da migration
          ↓
Atualização do banco de dados
