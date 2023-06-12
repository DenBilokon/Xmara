from django.apps import AppConfig




class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'

    def ready(self):
        from scheduler import views
        views.start()

