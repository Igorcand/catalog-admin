from src.core._shered.application.handler import Handler
from src.core._shered.events.event import Event
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shered.events.event_dispatcher import EventDispatcher

class PublishAudioVideoMediaUpdatedHandler(Handler):
    def __init__(self, event_dispatcher: EventDispatcher) -> None:
        self.event_dispatcher = event_dispatcher

    def handle(self, event: AudioVideoMediaUpdatedIntegrationEvent) -> None:
        print(f'PublishAudioVideoMediaUpdatedHandler -> Publising event: {event}')
        self.event_dispatcher.dispatch(event)