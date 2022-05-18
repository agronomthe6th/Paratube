from django.apps import AppConfig


class YoutubeConfig(AppConfig):
    name = 'main'

def ready(self):
    import main.signals  