# 🚀 API REST com FastAPI, SQLAlchemy e Alembic

## 📌 Sobre o Projeto

Este projeto consiste no desenvolvimento de uma **API REST utilizando Python e FastAPI**, com integração a um banco de dados relacional utilizando **SQLAlchemy** como ORM e **Alembic** para gerenciamento das migrações do banco de dados.

O objetivo principal foi desenvolver uma aplicação backend aplicando boas práticas de organização de código, separação de responsabilidades e controle da evolução da estrutura do banco através de migrations.

---

## 🛠️ Tecnologias Utilizadas

- **Python** → Linguagem principal utilizada no desenvolvimento.
- **FastAPI** → Framework utilizado para criação dos endpoints da API.
- **SQLAlchemy** → ORM responsável pela comunicação entre a aplicação e o banco de dados.
- **Alembic** → Ferramenta utilizada para criação e controle das migrações do banco.
- **Uvicorn** → Servidor ASGI utilizado para execução da aplicação.
- **SQLite/PostgreSQL** → Banco de dados relacional utilizado para armazenamento das informações.

---

## 📂 Estrutura do Projeto

```
API/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
│
├── routes/
│   ├── auth_routes.py
│   └── order_routes.py
│
├── alembic/
│
├── requirements.txt
│
└── README.md
```

### Descrição dos principais arquivos:

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Inicialização da aplicação FastAPI e registro das rotas |
| `models.py` | Definição das entidades e tabelas do banco |
| `schemas.py` | Modelos de validação e estrutura dos dados recebidos |
| `routes/` | Organização dos endpoints da aplicação |
| `requirements.txt` | Dependências utilizadas no projeto |

---

# 🗄️ Modelagem do Banco de Dados

A criação da estrutura do banco de dados foi realizada utilizando **SQLAlchemy**, através da definição dos modelos presentes no arquivo `models.py`.

Cada modelo representa uma entidade do sistema e define:

- Colunas da tabela;
- Tipos de dados;
- Chaves primárias;
- Relacionamentos;
- Restrições de integridade.

A utilização do SQLAlchemy possibilitou realizar a comunicação entre a aplicação e o banco de dados utilizando uma abordagem orientada a objetos.

---

# 🔄 Controle de Migrações com Alembic

Para gerenciar a evolução da estrutura do banco de dados foi utilizada a biblioteca **Alembic**.

O Alembic permite registrar alterações realizadas nos modelos e aplicá-las ao banco através de arquivos de migração, evitando alterações manuais diretamente no banco de dados.

Fluxo utilizado:

```
Alteração dos modelos (models.py)

          ↓

Criação da migration utilizando Alembic (py -m alembic revision --autogenerate -m "description")

          ↓

Aplicação da migration no banco (py -m alembic upgrade head)

          ↓

Banco de dados atualizado

```

---

# 📚 Conceitos Aplicados

Durante o desenvolvimento deste projeto foram aplicados conhecimentos de:

- Desenvolvimento de APIs REST;
- Arquitetura backend utilizando Python;
- Integração com banco de dados;
- ORM utilizando SQLAlchemy;
- Migrações utilizando Alembic;
- Organização modular de projetos;
- Boas práticas de desenvolvimento.

---
