import logging
import json
from uuid import UUID

import pika

from src.core._shered.events.abstract_consumer import AbstractConsumer
from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import MediaType, MediaStatus
from src.django_project.video_app.repository import DjangoORMVideoRepository

logger = logging.getLogger(__name__)

class VideoConvertedRabbitMQConsumer(AbstractConsumer):
    # python manage.py startconsumer
    def __init__(self, host='localhost', queue='videos.converted'):
        self.host = host
        self.queue = queue 
        self.connection = None 
        self.channel = None 
    
    def on_message(self, message):
        """
        {
            'error': '',
            'video': {
                'resource_id': 'dd57b20c-b6a0-4525-ba05-5bdcaf6baad9.VIDEO',
                'encoded_video_folder': '/path/to/encoded/video'
            },
            'status': 'COMPLETED'
        }
        """
        print(f'Received message consuming queue: {message}') 

        try:
            #body payload
            message = json.loads(message)

            #tratamento de erro
            error_message = message['error']
            if error_message:
                agregate_id_raw, _ = message['message']['resource_id'].split('.')
                logger.error(f"Error processing video {agregate_id_raw}: {error_message}")
            
            #serialização do evento
            agregate_id_raw, media_type_raw = message['message']['resource_id'].split('.')
            agregate_id = UUID(agregate_id_raw)
            media_type = MediaType(media_type_raw)
            encoded_location = message['video']['encoded_video_folder']
            status = MediaStatus(message['status'])

            #execução do use case
            process_audio_video_media_input = ProcessAudioVideoMedia.Input(
                video_id = agregate_id,
                encoded_location=encoded_location,
                media_type=media_type,
                status=status
            )

            print(f'Calling use case with input: {process_audio_video_media_input}')
            use_case = ProcessAudioVideoMedia(video_repository=DjangoORMVideoRepository())
            use_case.execute(request=process_audio_video_media_input)

        except:
            logger.error(f"Error processing payload {message}", exc_info=True)
            return  

    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(
            queue=self.queue, 
            on_message_callback=self.on_message_callback
        )

        print(f'Consumer started. Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    def on_message_callback(self, ch, method, properties, body):
        self.on_message(body)
    
    def stop(self):
        self.connection.close()
