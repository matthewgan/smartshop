# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import EntranceLog


class EntranceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceLog
        fields = ('who', 'where', )
