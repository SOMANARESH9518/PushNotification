from rest_framework import serializers

from getGCMIds import models


# from django.core import serializers

class GCMStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GCMStore
        fields = ('id', 'gcmId')
