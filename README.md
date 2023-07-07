# RHManager

Este projeto foi desenvolvido para a disciplina de Projeto Integrador 1 do curso de Engenharia de Computação da Universidade Federal de Santa Catarina - Campus Araranguá. O objetivo do projeto é desenvolver um sistema de gerenciamento de recursos humanos para o setor de Recursos Humanos da Polícia Militar de Santa Catarina. Nesse sentido, usou-se a linguagem de programação Python e o framework Django para desenvolver o sistema. O sistema foi desenvolvido para ser executado em um servidor local, sendo que o banco de dados utilizado é o SQLite.

## Instalação

Para rodar o projeto é necessário ter uma versão do Python 3 instalada. Para instalar as dependências do projeto, execute o seguinte comando:

- Primeiro, instale o virtualenv para criar um ambiente virtual para o projeto:

```bash
pip install virtualenv
```

- A seguir, crie um ambiente virtual para o projeto:

```bash
virtualenv env
```

- Ative o ambiente virtual:

```bash
source env/bin/activate
```

- Instale as dependências do projeto:

```bash
pip install -r requirements/local.txt
```

- A seguir, realize as migrações do banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate
```

- A continução, crie um super usuário para acessar o sistema:

```bash
python manage.py createsuperuser
```

- Por fim, execute o servidor:

```bash
python manage.py runserver
```

## Uso

Para acessar o sistema, abra o navegador e digite o seguinte endereço:

```bash
http://localhost:8000
```

## Contribuição

Para contribuir com o projeto, realize um fork do repositório e crie uma branch com o nome da funcionalidade que deseja implementar. Após implementar a funcionalidade, realize um pull request para a branch master do repositório.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)

## Autor

- [Dennis Paz](https://github.com/DenPaz)
