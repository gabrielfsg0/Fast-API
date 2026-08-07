Banco de Dados

O projeto utiliza SQLAlchemy para modelagem das entidades e interação com o banco de dados. As tabelas são representadas por classes Python definidas no arquivo model.py, seguindo o conceito de ORM (Object-Relational Mapping).

Para controlar a evolução da estrutura do banco, foi utilizado Alembic, responsável pelo versionamento e execução das migrations.

O fluxo utilizado é:

model.py → Alembic migration → banco de dados

As migrations permitem registrar alterações como criação de tabelas, adição ou alteração de colunas e relacionamentos, mantendo o banco sincronizado com a aplicação.

Para criar uma migration:

alembic revision --autogenerate -m "description"

Para aplicar as migrations:

alembic upgrade head

Para reverter a última migration:

alembic downgrade -1
