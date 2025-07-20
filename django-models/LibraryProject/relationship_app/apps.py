from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LibraryProject.relationship_app'

    def ready(self):
        import LibraryProject.relationship_app.signals