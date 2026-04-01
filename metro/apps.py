from django.apps import AppConfig

class MetroConfig(AppConfig):
    name = 'metro'

    def ready(self):
        import metro.signals