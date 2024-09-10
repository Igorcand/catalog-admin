import logging
import json
from uuid import UUID

import pika

from src.core._shered.events.abstract_consumer import AbstractConsumer
from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import MediaType, MediaStatus
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.core.video.domain.video_repository import VideoRepository

logger = logging.getLogger(__name__)

class VideoConvertedRabbitMQConsumer(AbstractConsumer):
    # python manage.py startconsumer
    def __init__(self, video_repository: VideoRepository, host='localhost', queue='videos.converted'):
        self.host = host
        self.queue = queue 
        self.connection = None 
        self.channel = None 
        self.video_repository = video_repository
    
    def on_message(self, message):
        """
        {
            "error": "",
            "video": {
                "resource_id": "24846fe1-6218-46bb-96a8-d6d4534e0885.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video"
            },
            "status": "COMPLETED"
        }
        """

        try:
            #body payload
            message = json.loads(message)

            #tratamento de erro
            error_message = message['error']
            if error_message:
                agregate_id_raw, _ = message['video']['resource_id'].split('.')
                logger.error(f"Error processing video {agregate_id_raw}: {error_message}")
                print(f"Error processing video {agregate_id_raw}: {error_message}")

                return 
            
            #serialização do evento
            agregate_id_raw, media_type_raw = message['video']['resource_id'].split('.')
            agregate_id = UUID(agregate_id_raw)
            media_type = MediaType(media_type_raw)
            encoded_location = message['video']['encoded_video_folder']
            status = MediaStatus(message['status'])

            #execução do use case
            process_audio_video_media_input = ProcessAudioVideoMedia.Input(
                video_id = agregate_id,
                encoded_location=encoded_location,
                media_type=media_type,
                status=status,
            )

            use_case = ProcessAudioVideoMedia(video_repository=self.video_repository)
            use_case.execute(request=process_audio_video_media_input)

        except Exception as e:
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
