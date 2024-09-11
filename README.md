# CATALOG-ADMIN

## SOBRE

Esse projeto faz parte de uma aplicação robusta chamada CODEFLIX, onde o intuito é construir uma aplicação completa para a administração e consumo de videos. Este projeto se chama CATALOG-ADMIN, pois é responsável por toda a administração de informações dos filmes como: Categoria, Gênero, Membros do Elenco, e o principal, os videos. 

Esse projeto se comunica com um microserviço externo chamado ENCODER atravéz de uma fila do RabbitMQ, onde toda vez que o usuário envia um arquivo de mídia, a aplicação CATALOG-ADMIN adiciona uma mensagem na fila chamada "videos.new", que por sua vez, a aplicação consome essa mensagem, faz o processanto necessário e publica uma mensagem na fila "videos.encoded", que por sua vez, a aplicação CATALOG-ADMIN está consumindo as mensagens para atualizar as informações. Os microserviços acessam os mesmo dados de mídia pois os arquivos estão sendo salvos em um Bucket S3 da AWS.

O cliente dessa aplicação seria um serviço Front-End (que será construido posteriormente) que consultaria as rotas de API para mostrar as informações para o usuário administrador.

Neste pedaço do diagrama C4 abaixo, podemos visualizar a parte que nos importa que é o fluxo desde o FrontEnd consumindo via HTTPS nossa API do CATALOG-ADMIN e a comunicação do CATALOG-ADMIN com o ENCODER via RabbitMQ.

![c4-part](https://github.com/Igorcand/catalog-admin/blob/master/assets/c4-part.png)


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

![agregados](https://github.com/Igorcand/catalog-admin/blob/master/assets/agregados.png)








tree -I "__pycache__" src

python manage.py startapp genre_app ./src/django_project/genre_app