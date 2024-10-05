from django.apps import AppConfig


class SiedlungsmanagerConfig(AppConfig):
    # by default, any models in this app that don't explicitly specify a primary key
    # will use a BigAutoField as their primary key.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'siedlungsmanager'
