# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import UploadedFace


class UploadedFaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFace
        fields = ('uuid', 'image', )


class SearchFaceUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFace
        fields = ('image',)
