from django.core.management.base import BaseCommand
from src.core.video.infra.video_converted_rabbitmq_consumer import VideoConvertedRabbitMQConsumer
from src.django_project.video_app.repository import DjangoORMVideoRepository

class Command(BaseCommand):
    help = 'Starts the VideoConverted Consumer'

    def handle(self, *args, **options):
        consumer = VideoConvertedRabbitMQConsumer(video_repository=DjangoORMVideoRepository())
        consumer.start()