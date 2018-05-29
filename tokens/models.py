# Stdlib imports

# Core Django imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Third-party app imports
from rest_framework.authtoken.models import Token

# Imports from your apps


# Create extra token when create a new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    every time a new user is saved in your database,
    this function will run and a new Token will be created for that user
    """
    if created:
        Token.objects.create(user=instance)
