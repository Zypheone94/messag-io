import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Hérité de asyncWebsocketConsumer contient tout ce qui permet de gérer les connexions,
# ainsi que les échanges de message


class ChatConsumer(AsyncWebsocketConsumer):

    # Méthode appelée lorsqu'un client se connect à la web socket
    async def connect(self):
        # créer un nom de salle au travers de l'url
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Ajoute une personne au groupe
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accepte la personne dans le groupe
        await self.accept()
        print(f"WebSocket CONNECTED to room {self.room_name}")

    # Méthode appelée lorsqu'une personne pars du groupe
    async def disconnect(self, close_code):
        # Retire la personne du groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket DISCONNECTED from room {self.room_name}")

    # Méthode appelée lorsqu'un message est reçu
    async def receive(self, text_data):
        try:
            # Récupère le message et le passe au format JSON
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            print(f"Received message in room {self.room_name}: {message}")
            # Check if the message is not empty before broadcasting
            if message.strip():
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.message',
                        'message': message
                    }
                )
        except json.JSONDecodeError:
            pass  # Ignore invalid JSON messages

    # Méthode appelée lorsqu'un message est reçu
    async def chat_message(self, event):
        message = event['message']
        print(f"Sending message in room {self.room_name}: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
