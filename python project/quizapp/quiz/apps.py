from django.apps import AppConfig


class QuizConfig(AppConfig):
    """Application configuration for the quiz app.

    This class is intentionally minimal. `default_auto_field` is set to use BigAutoField
    for primary keys and `name` registers the app package.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'
