from django.apps import AppConfig


class BankpageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bankPage"
    
    
    #need to be created use signal and receiver in django
    def ready(self) -> None:
        
        import bankPage.signal
        return super().ready()
