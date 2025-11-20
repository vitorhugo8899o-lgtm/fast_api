# API RESTful de E-commerce

Esta é uma API RESTful completa desenvolvida em **Python** utilizando o framework **FastAPI**. O projeto simula a estrutura básica de um backend de **E-commerce**, gerenciando produtos, usuários e pedidos. O deploy está ativo no **Render**.

[![Status do Deploy](https://img.shields.io/badge/Deploy-Online-success?style=for-the-badge)](https://fast-api-k9as.onrender.com)


Tecnologias Utilizadas:
* **Linguagem:** Python
* **Framework:** FastAPI (para desenvolvimento rápido da API)
* **Banco de Dados:** PostgreSQL (com integração via SQLAlchemy)
* **Gerenciamento de Dependências:** Poetry
* **Deploy/Hospedagem:** Render
* **Containers:** Docker (Dockerfile e docker-compose.yml)

Funcionalidades da API:
* **Autenticação** (`/auth`):
    * Implementação de rotas de login e geração de tokens JWT.
 
* **Usuários (`/user`)**:
    * `GET /useres`: Listar todos os usuários.
    * `POST /Create_Account`: Cadastrar um novo usuário.
    * `PUT /alter`: Altera as informações do usuário.
    * `DELETE /Delete user`: Deleta a conta do usuário.
* **Produtos (`/master`)**:
    * `POST /produtos`: Adicionar um novo produto (funcionalidade exclusiva dos usuários adiministrativos).
    * `DELETE /`: deletar um produto específico (funcionalidade exclusiva dos usuários adiministrativos).
    * `GET /get_product`: Listar todos os produtos (Não é necessario está logado para ver a lista).


