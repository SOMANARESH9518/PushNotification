import json

import requests
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from getGCMIds.models import *
from getGCMIds.serializers import *

API_KEY = 'AIzaSyDyWK0xBOuUi8dPX0n8qvWb4cv-BuEpFWA'


class GCMStoreList(generics.ListCreateAPIView):
    def __init__(self):
        self.queryset = GCMStore.objects.all()
        self.serializer_class = GCMStoreSerializer

    def get(self, request, format=None):
        gcm_id_list = GCMStore.objects.all()
        serializer = GCMStoreSerializer(gcm_id_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GCMStoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GCMStoreDetail(generics.RetrieveUpdateDestroyAPIView):
    def __init__(self):
        self.queryset = GCMStore.objects.all()
        self.serializer_class = GCMStoreSerializer

    def get_object(self, pk):
        try:
            return GCMStore.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        gcm_id = GCMStore.objects.get(pk=pk)
        serializer = GCMStoreSerializer(gcm_id)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        gcm_id = self.get_object(pk)
        serializer = GCMStoreSerializer(gcm_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        gcm_id = self.get_object(pk)
        gcm_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def send_notification(request):
    gcm_id_list = GCMStore.objects.all()
    url = "https://android.googleapis.com/gcm/send"
    headers = {'Content-Type': 'application/json', 'Authorization': 'key=' + API_KEY}
    registration_ids = []
    for each in gcm_id_list:
        registration_ids.append(each.gcmId)
    # registration_ids = gcm_id_list.values_list('gcmId', flat=True)
    data = {"registration_ids": registration_ids,
            'message': 'Welcome to the World of Coding for GCM Notification'}
    requests.post(url, data=json.dumps(data), headers=headers)
    return render(request, '/getGCMIds/notification.html')
