from unittest.mock import create_autospec, MagicMock, patch
from src.core._shered.application.handler import Handler
from src.core._shered.events.message_bus import MessageBus
from src.core._shered.events.event import Event
from src.core._shered.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher


class DummyEvent(Event):
    pass 

class TestEventDispatcher:
    def test_dispatch_event(self):
        # Simula a conexão utilizando o contexto do patch
        with patch('src.core._shered.infrastructure.events.rabbitmq_dispatcher.pika.BlockingConnection') as mock_blocking_connection:
            # Configura o mock para a conexão e canal
            mock_connection = MagicMock()
            mock_channel = MagicMock()
            mock_blocking_connection.return_value = mock_connection
            mock_connection.channel.return_value = mock_channel

            # Instancia o dispatcher
            dispatcher = RabbitMQDispatcher()

            # Chama o método dispatch
            dispatcher.dispatch(DummyEvent())

            # Verifica se o channel foi inicializado corretamente
            mock_connection.channel.assert_called_once()
            mock_channel.queue_declare.assert_called_once_with(queue="videos.new")
            mock_channel.basic_publish.assert_called_once()

            print("Teste de RabbitMQDispatcher foi executado com sucesso.")