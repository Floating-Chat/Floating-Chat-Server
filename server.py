import asyncio
import websockets
import json
from utils import load_json_safe, debug_log
from db.models.user import User
from db.models.message import Message


async def get_info(client):
    user_info = None
    while user_info is None:
        connect_msg = await client.recv()
        connect_json = load_json_safe(connect_msg)
        if connect_json.get('type') == 'send_info':
            user_name = connect_json.get('user_name')
            user_color = connect_json.get('user_color', '#FFF')
            if user_name:
                user_info = user_name, user_color
    return user_info


class Server:
    def __init__(self, server_name='localhost', port=8765):
        self.__loop = asyncio.get_event_loop()
        self.__server_name = server_name
        self.__port = port
        self.__connected = set()

    async def send_to_all_clients(self, message: dict):
        message_to_send = json.dumps(message)
        for client_object in self.__connected:
            client = client_object[0]
            await client.send(message_to_send)

    async def unregister_client(self, client_obj: tuple):
        self.__connected.remove(client_obj)
        user = client_obj[1]
        disconnect_message = {
            'type': 'user_disconnected',
            'info': user.serialize()
        }
        debug_log(disconnect_message)
        await self.send_to_all_clients(disconnect_message)

    async def register_client(self, client_obj: tuple):
        self.__connected.add(client_obj)
        user = client_obj[1]
        connect_message = {
            'type': 'user_connected',
            'info': user.serialize()
        }
        debug_log(connect_message)
        await self.send_to_all_clients(connect_message)

    async def message_handler(self, message: str, user: 'User'):
        message_obj = Message.create(user, message)
        serialized_message = message_obj.serialize()
        message_to_send = {
            'type': 'receive_message',
            'message': serialized_message
        }
        debug_log(message_to_send)
        await self.send_to_all_clients(message_to_send)

    async def on_connect(self, client, path):
        greetings_msg = json.dumps({
            'type': 'connection_open',
        })
        await client.send(greetings_msg)
        user_name, user_color = await get_info(client)

        user = User.get_by_name(user_name)
        if not user:
            user = User.create(user_name, user_color)
        if user.color != user_color:
            user.update(color=user_color)
        information_msg = json.dumps({
            'type': 'user_information',
            'info': user.serialize()
        })
        await client.send(information_msg)
        client_object = (client, user)
        await self.register_client(client_object)
        try:
            async for message in client:
                message_json = load_json_safe(message)
                message_type = message_json.get('type', '')
                if message_type == 'send_message':
                    text_message = message_json.get('message', '<mensagem vazia>')
                    await self.message_handler(text_message, user)
                elif message_type == 'change_color':
                    color_code = message_json.get('user_color', '#FFF')
                    user.update(color=color_code)
                elif message_type == 'change_name':
                    new_name = message_json.get('user_name', user.name)
                    user.update(name=new_name)
                elif message_type == 'close_connection':
                    break
        finally:
            await self.unregister_client(client_object)

    def stop(self):
        self.__loop.stop()

    def start(self):
        ws_server = websockets.serve(self.on_connect, self.__server_name, self.__port)
        self.__loop.run_until_complete(ws_server)
        self.__loop.run_forever()
