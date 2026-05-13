# Comunidade Postify

## Sobre o Projeto

O Comunidade Postify é uma aplicação web full-stack desenvolvida com Python e Flask, funcionando como uma plataforma de comunidade no estilo blog.

Os usuários podem criar contas, editar perfil, publicar, editar e excluir posts e interagir com conteúdos de outros usuários.

Este projeto foi desenvolvido como parte de um exercício prático para consolidar conhecimentos em desenvolvimento web, backend, banco de dados, autenticação e deploy.

## Demonstração

https://postify.up.railway.app

## Funcionalidades
- Autenticação de usuários com registro e login seguro utilizando hash de senhas
- Gerenciamento de perfil, permitindo edição de nome de usuário, email e foto de perfil
- Sistema de habilidades/cursos exibidos no perfil do usuário
- Sistema completo de posts (criar, visualizar, editar e excluir)
- Upload de imagens de perfil utilizando Cloudinary para armazenamento
- Visualização de perfis de outros usuários e seus respectivos posts

## Tecnologias 

**Backend** 
- Python 
- Flask

**Database** 
- SQLAlchemy 
- PostgreSQL / SQLite

**Autenticação** 
- Flask-Login
- Flask-Bcrypt

**Formulários** 
- Flask-WTF

**Manipulação de Imagens** 
- Pillow
- Cloudinary

**Frontend** 
- HTML 
- CSS 
- Bootstrap 5

**Deploy** 
- Railway

## Aviso!

Por ser um projeto acadêmico, algumas funcionalidades como verificação de e-mail foram simplificadas.
Por esse motivo, não é necessário utilizar um e-mail real para cadastro, porém não há recuperação de senha caso ela seja esquecida.
