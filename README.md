# CATALOG-ADMIN

## SOBRE

Esse projeto faz parte de uma aplicação robusta chamada CODEFLIX, onde o intuito é construir uma aplicação completa para a administração e consumo de videos. Este projeto se chama CATALOG-ADMIN, pois é responsável por toda a administração de informações dos filmes como: Categoria, Gênero, Membros do Elenco, e o principal, os videos. 

Esse projeto se comunica com um microserviço externo chamado ENCODER atravéz de uma fila do RabbitMQ, onde toda vez que o usuário envia um arquivo de mídia, a aplicação CATALOG-ADMIN adiciona uma mensagem na fila chamada "videos.new", que por sua vez, a aplicação consome essa mensagem, faz o processanto necessário e publica uma mensagem na fila "videos.encoded", que por sua vez, a aplicação CATALOG-ADMIN está consumindo as mensagens para atualizar as informações. Os microserviços acessam os mesmo dados de mídia pois os arquivos estão sendo salvos em um Bucket S3 da AWS.

O cliente dessa aplicação seria um serviço Front-End (que será construido posteriormente) que consultaria as rotas de API para mostrar as informações para o usuário administrador.

Neste pedaço do diagrama C4 abaixo, podemos visualizar a parte que nos importa que é o fluxo desde o FrontEnd consumindo via HTTPS nossa API do CATALOG-ADMIN e a comunicação do CATALOG-ADMIN com o ENCODER via RabbitMQ.

![about](https://github.com/Igorcand/catalog-admin/blob/master/assets/about/c4-part.png)


## Estrutura do repositório

### Arquivos e pastas

```bash

    src
    ├── config.py
    ├── core
    │   ├── cast_member
    │   │   ├── application
    │   │   │   └── use_cases
    │   │   │       ├── create_cast_member.py
    │   │   │       ├── delete_cast_member.py
    │   │   │       ├── exceptions.py
    │   │   │       ├── list_cast_member.py
    │   │   │       └── update_cast_member.py
    │   │   ├── domain
    │   │   │   ├── cast_member.py
    │   │   │   └── cast_member_repository.py
    │   │   ├── infra
    │   │   │   └── in_memory_cast_member_repository.py
    │   │   ├── __init__.py
    │   │   └── tests
    │   │       ├── application
    │   │       │   ├── integration
    │   │       │   │   ├── __init__.py
    │   │       │   │   ├── test_create_cast_member.py
    │   │       │   │   ├── test_delete_cast_member.py
    │   │       │   │   ├── test_list_cast_member.py
    │   │       │   │   └── test_update_cast_member.py
    │   │       │   └── unit
    │   │       │       ├── __init__.py
    │   │       │       ├── test_create_cast_member.py
    │   │       │       ├── test_delete_cast_member.py
    │   │       │       ├── test_list_cast_member.py
    │   │       │       └── test_update_cast_member.py
    │   │       └── domain
    │   │           └── test_cast_member.py
    │   ├── category
    │   │   ├── application
    │   │   │   └── use_cases
    │   │   │       ├── create_category.py
    │   │   │       ├── delete_category.py
    │   │   │       ├── exceptions.py
    │   │   │       ├── get_category.py
    │   │   │       ├── list_category.py
    │   │   │       └── update_category.py
    │   │   ├── domain
    │   │   │   ├── category.py
    │   │   │   └── category_repository.py
    │   │   ├── infra
    │   │   │   └── in_memory_category_repository.py
    │   │   ├── __init__.py
    │   │   └── tests
    │   │       ├── application
    │   │       │   ├── __init__.py
    │   │       │   ├── integration
    │   │       │   │   ├── __init__.py
    │   │       │   │   ├── test_create_category.py
    │   │       │   │   ├── test_delete_category.py
    │   │       │   │   ├── test_get_category.py
    │   │       │   │   ├── test_list_category.py
    │   │       │   │   └── test_update_category.py
    │   │       │   └── unit
    │   │       │       ├── __init__.py
    │   │       │       ├── test_create_category.py
    │   │       │       ├── test_delete_category.py
    │   │       │       ├── test_get_category.py
    │   │       │       ├── test_list_category.py
    │   │       │       └── test_update_category.py
    │   │       ├── domain
    │   │       │   └── test_category.py
    │   │       └── infra
    │   │           └── test_in_memory_category.py
    │   ├── genre
    │   │   ├── application
    │   │   │   └── use_cases
    │   │   │       ├── create_genre.py
    │   │   │       ├── delete_genre.py
    │   │   │       ├── exceptions.py
    │   │   │       ├── get_genre.py
    │   │   │       ├── list_genre.py
    │   │   │       └── update_genre.py
    │   │   ├── domain
    │   │   │   ├── genre.py
    │   │   │   └── genre_repository.py
    │   │   ├── infra
    │   │   │   └── in_memory_genre_repository.py
    │   │   ├── __init__.py
    │   │   └── tests
    │   │       ├── application
    │   │       │   ├── __init__.py
    │   │       │   ├── integration
    │   │       │   │   ├── __init__.py
    │   │       │   │   ├── test_create_genre.py
    │   │       │   │   ├── test_delete_genre.py
    │   │       │   │   ├── test_get_genre.py
    │   │       │   │   ├── test_list_genre.py
    │   │       │   │   └── test_update_genre.py
    │   │       │   └── unit
    │   │       │       ├── __init__.py
    │   │       │       ├── test_create_genre.py
    │   │       │       ├── test_delete_genre.py
    │   │       │       ├── test_get_genre.py
    │   │       │       ├── test_list_genre.py
    │   │       │       └── test_update_genre.py
    │   │       ├── domain
    │   │       │   └── test_genre.py
    │   │       └── __init__.py
    │   ├── _shered
    │   │   ├── application
    │   │   │   └── handler.py
    │   │   ├── domain
    │   │   │   ├── entity.py
    │   │   │   ├── notification.py
    │   │   │   └── pagination.py
    │   │   ├── events
    │   │   │   ├── abstract_consumer.py
    │   │   │   ├── abstract_message_bus.py
    │   │   │   ├── event_dispatcher.py
    │   │   │   ├── event.py
    │   │   │   └── message_bus.py
    │   │   ├── infrastructure
    │   │   │   ├── events
    │   │   │   │   └── rabbitmq_dispatcher.py
    │   │   │   └── storage
    │   │   │       ├── abstract_storage_service.py
    │   │   │       ├── aws_s3_storage.py
    │   │   │       ├── gcs_storage.py
    │   │   │       └── local_storage.py
    │   │   ├── __init__.py
    │   │   └── tests
    │   │       ├── domain
    │   │       │   └── test_entity.py
    │   │       └── events
    │   │           ├── test_event_dispatcher.py
    │   │           └── test_message_bus.py
    │   └── video
    │       ├── application
    │       │   ├── events
    │       │   │   ├── handlers.py
    │       │   │   └── integration_events.py
    │       │   └── use_cases
    │       │       ├── create_video_without_media.py
    │       │       ├── delete_video.py
    │       │       ├── exceptions.py
    │       │       ├── get_video.py
    │       │       ├── list_videos.py
    │       │       ├── process_audio_video_media.py
    │       │       └── upload_video.py
    │       ├── domain
    │       │   ├── events
    │       │   │   └── event.py
    │       │   ├── value_objects.py
    │       │   ├── video.py
    │       │   └── video_repository.py
    │       ├── infra
    │       │   ├── in_memory_video_repository.py
    │       │   └── video_converted_rabbitmq_consumer.py
    │       ├── __init__.py
    │       └── tests
    │           ├── application
    │           │   ├── __init__.py
    │           │   ├── integration
    │           │   │   ├── __init__.py
    │           │   │   ├── test_create_without_media.py
    │           │   │   ├── test_delete_video.py
    │           │   │   ├── test_get_video.py
    │           │   │   ├── test_list_video.py
    │           │   │   ├── test_local_storage.py
    │           │   │   └── test_upload_video.py
    │           │   └── unit
    │           │       ├── __init__.py
    │           │       ├── test_create_video_without_media.py
    │           │       ├── test_delete_video.py
    │           │       ├── test_get_video.py
    │           │       └── test_list_video.py
    │           ├── domain
    │           │   └── test_video.py
    │           ├── infra
    │           │   └── test_consumer.py
    │           └── __init__.py
    ├── django_project
    │   ├── asgi.py
    │   ├── cast_member_app
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── __init__.py
    │   │   ├── migrations
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── repository.py
    │   │   ├── serializers.py
    │   │   ├── tests
    │   │   │   ├── test_repository.py
    │   │   │   ├── test_serializers.py
    │   │   │   └── test_views.py
    │   │   └── views.py
    │   ├── category_app
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── __init__.py
    │   │   ├── migrations
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── repository.py
    │   │   ├── serializers.py
    │   │   ├── tests
    │   │   │   ├── __init__.py
    │   │   │   ├── test_repository.py
    │   │   │   └── test_views.py
    │   │   └── views.py
    │   ├── genre_app
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── __init__.py
    │   │   ├── migrations
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── repository.py
    │   │   ├── serializers.py
    │   │   ├── tests
    │   │   │   ├── __init__.py
    │   │   │   ├── test_repository.py
    │   │   │   └── test_views.py
    │   │   └── views.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── video_app
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── __init__.py
    │   │   ├── management
    │   │   │   └── commands
    │   │   │       └── startconsumer.py
    │   │   ├── migrations
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── repository.py
    │   │   ├── serializers.py
    │   │   ├── tests
    │   │   │   ├── __init__.py
    │   │   │   ├── test_repository.py
    │   │   │   └── test_views.py
    │   │   └── views.py
    │   └── wsgi.py
    ├── __init__.py
    └── tests_e2e
        ├── __init__.py
        ├── test_user_can_create_and_edit_category.py
        ├── test_user_can_create_video_and_update_with_media.py
        └── test_user_can_create_video_without_media.py

```

### Explicação da arquitetura optada

O projeto foi desenvolido utilizando os princípios de Arquitetura Limpa e Arquitetura Hexagonal, onde separamos os nossos domínios, regras de negócio, casos de uso, e aplicação web em pastas seraradas. E também foi utilizado o máximo de proveitamento do conceito de POO, pois foi criado Classes Principais, e Classes Abstratas para facilitar a implementação de futuras tecnologias, como por exemplo, o repositório para salvar as informações do núcleo da aplicação foi feito em memória, e a aplicação web feita em django apenas implementa a classe de repositório para poder salvar em um banco de dados.

A pasta "core" é responsável por separar todas as regras de negócio e de aplicação, onde cada pasta interna (category, genre, cast_member, videos) representa um núcleo separado, onde declaramos nosso domínio com as entidades principais, e também geramos nossos caso de uso da aplicação (cadastrar, listar, atualizar e deletar). Perceba que criado um CRUD sem a necessidade de um serviço web, pois como é apresentado na Arquitetura Hexagonal, a aplicação web chega para agregar no isstema e não para ter dentro das regras de negócio.

Portanto, a pasta "django_project" representa toda a aplicação web gerada, com os endpoints para cada caso de uso criado no núcleo da nossa aplicação. Por padrão, o django cria apps na mesma raiz do projeto django, e essa arquitetura foi alterada para seguir os conceitos de Arquitetura Hexagonal e por isso os apps foramm adicionado dentro do projeto django.

Nessa imagem abaixo podemos entender como os agregados possuem casos de uso e a aplicação Web acessa esses casos de uso para poder gerar os endpoints.

![about](https://github.com/Igorcand/catalog-admin/blob/master/assets/about/agregados.png)

## Como rodar esse projeto

```bash
# clone este repositorio
git clone https://github.com/Igorcand/catalog-admin

# Entre na pasta
cd catalog-admin

# Rode os serviços
docker-compose up --build

```

## Testes
Esse projeto foi desenvolvido todo baseado em testes, possuindo mais de 200 testes, dentre eles unitários, integração e end-to-end. 

![tests](https://github.com/Igorcand/catalog-admin/blob/master/assets/tests/tests.png)

Nos testes unitários, sua intenção é testar a menor unidade do sistema, o código. E para isso é bem importante que teste a maior parte de problemas técnicos de implementação possíveis, buscando mitigar ao máximo a possibilidade de um erro de codificação

Testes de integração, nessa camada, você deve buscar executar testes que garantam a integridade com outros componentes como tabelas, arquivos e filas

Já os testes End to End devem buscar testar sua aplicação de ponta a ponta, com um resultado funcional observável. Neste momento a ideia é testar o sistema da forma mais próxima do ambiente produtivo.

![tests](https://github.com/Igorcand/catalog-admin/blob/master/assets/tests/piramide.png)

### Como rodar os testes

```bash
# Com os containeres rodando, rode o comando
docker exec -it app bash

# Rode os testes
pytest

```

## API
Para acessar os endpoints presentes e visualizar os inputs e outputs de cada rota, acesse o link <a href="https://documenter.getpostman.com/view/2763594/2s9Ykt5yuR" target="_blank">link</a>

Para melhor visualização das rotas, acesse o endpoint http://127.0.0.1:8000/ para visualizar o swagger do django rest framework
![api](https://github.com/Igorcand/catalog-admin/blob/master/assets/api/swagger.png)

## RabbitMQ
Acesse o dashboard do RabbitMQ no endpoint "http://127.0.0.1:15672" e faça login com as credenciais: Username = guest | Password = guest

![rabbitmq](https://github.com/Igorcand/catalog-admin/blob/master/assets/rabbitmq/login.png)

Para visualizar as filas vá na aba "Queues and Stream"
![rabbitmq](https://github.com/Igorcand/catalog-admin/blob/master/assets/rabbitmq/queues.png)

OBS: Caso não esteja visualizando a fila "videos.new", é necessário que faça uma requisição para a rota http://localhost:8000/api/videos/{video_id}/ no método http PATCH, com o input de midia_type = "VIDEO" ou "TRAILER", porque essa rota irá disparar uma mensagem na fila e caso não exista irá criar


## Autenticação
### Configuração
Acesse o dashboard do keycloak no endpoint "http://127.0.0.1:8080" e faça login com as credenciais: Username = admin | Password = Admin

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/login.png)

Crie um realm para o projeto com o nome "codeflix"

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/realm.png)

Vá na aba "Clients" e clique no boão "Create client"
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/create_client.png)

Crie um client chamado "codeflix-frontend" e aperte "Next" 2 vezes
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/client_frontend.png)

Crie um usuário para você

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/create_user.png)

Para fins de aprendizagem, pode criar com valores padrão.

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/user_admin.png)

Vá na aba "Credentials" e clique no botão "Set password"
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/user_password.png)

Para fins de aprendizagem, crie a senha como "admin" e desmarque a opção "Temporary"
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/set_password.png)

Crie role para seu usuário

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/roles.png)

Crie a role "admin"

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/role_admin.png)

Vá na aba "Users" e clique no seu usuário

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/tab_user.png)

Vá na aba "Role mapping" e clique em "Assign role"
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/assign_role.png)

Filtre por "Filter by realm roles" e selecione a role "admin"
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/admin_role_assigned.png)

### Comunicação entre Keycloak e Aplicação principal
Vá na aba "Realm settings" -> clique no ícone "Keys" -> Clique no botão "Public key" do item "RS256" e copie a chave
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/public_key.png)

Crie um arquivo .env 
```
AUTH_PUBLIC_KEY='sua_public_key'
```

### Gerar token JWT
Para gerar o token você precisa chamar a rota "http://127.0.0.1:8080/realms/codeflix/protocol/openid-connect/token" com o método http POST, enviando no formato Form Url Encoded passando as informações 

![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/input_token.png)

Copie e cole o token gerado nas rotas da aplicação "catalog-admin"
![keycloak](https://github.com/Igorcand/catalog-admin/blob/master/assets/keycloak/output_token.png)


# Tecnologias Usadas

## Back end
- Python
- Django
- Pytest
- Docker

## Database
- SQLite
  
## Infra
- RabbitMQ

# Author

Igor Cândido Rodrigues

https://www.linkedin.com/in/igorc%C3%A2ndido/

