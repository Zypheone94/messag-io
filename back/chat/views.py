# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .consumers import ChatConsumer

def room(request, room_name):
    # Obtenir le nom de la salle à partir des paramètres de l'URL

    # Créer un nom de groupe de canal pour la salle de chat
    room_group_name = f"chat_{room_name}"

    # Obtenir le canal Layer de Channels
    channel_layer = get_channel_layer()

    # Initialiser le consumer
    consumer = ChatConsumer()

    # Passer le message connecté au consumer
    async_to_sync(channel_layer.group_add)(room_group_name, consumer.channel_name)

    # Retourner une réponse HTTP 200 OK pour indiquer que la connexion WebSocket a été établie
    return HttpResponse(status=200)