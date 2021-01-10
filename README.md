# Floating-Chat-Server
Server-side for Floating Chat


## Message Documentation

## Client-side:

#### Send info:
**Params**:
- type = send_info: Sends your info for allow you to send messages;
- user_name: Your name;
- user_color: Your color (hexadecimal). Pattern: #RRGGBBAA (alpha is optional);
```json
{
  "type": "send_info",
  "user_name": "HidekiHrk",
  "user_color": "#99FFBB"
}
```

#### Send message:
**Params**:
- type = send_message: Sends a message to all clients connected;
- message: The message that you want to send;
```json
{
  "type": "send_message",
  "message": "Hello everyone!!!"
}
```

#### Change color:
**Params**:
- type = change_color: Changes your color;
- user_color: Your new color (hexadecimal). Pattern: #RRGGBBAA (alpha is optional);
```json
{
  "type": "change_color",
  "user_color": "#99FFBB"
}
```

#### Change name:
**Params**:
- type = change_name: Changes your name;
- user_name: Your new name;
```json
{
  "type": "change_name",
  "user_name": "HidekiHrk"
}
```

#### Close connection:
**Params**:
- type = close_connection: Closes the connection between the server and you;
```json
{
  "type": "close_connection"
}
```

## Server-side:

#### Connection open:
**Params**:
- type = connection_open: Means that you opened a connection and the server is waiting for your info;
```json
{
  "type": "connection_open"
}
```

#### User information:
**Params**:
- type = user_information: Sends your info to you to confirm that you're now connected into chat;
- info: Your serialized info
    - name: Your name;
    - color: Your color (hexadecimal). Pattern: #RRGGBBAA (alpha is optional);
```json
{
  "type": "user_information", 
  "info": {
    "name": "HidekiHrk",
    "color": "#99ffbb"
  }
}
```

#### User connected:
**Params**:
- type = user_connected: Means that another user (or you) have connected in the chat;
- info: User serialized info
    - name: User name;
    - color: User color (hexadecimal). Pattern: #RRGGBBAA (alpha is optional);
```json
{
  "type": "user_connected", 
  "info": {
    "name": "HidekiHrk",
    "color": "#99ffbb"
  }
}
```

#### User disconnected:
**Params**:
- type = user_disconnected: Means that another user (or you) have disconnected to the chat;
- info: User serialized info
    - name: User name;
    - color: User color (hexadecimal). Pattern: #RRGGBBAA (alpha is optional);
```json
{
  "type": "user_disconnected", 
  "info": {
    "name": "HidekiHrk",
    "color": "#99ffbb"
  }
}
```

#### Receive message:
**Params**:
- type = receive_message: Means that you're receiving a message from other user;
- message: Message information;
    - id: Message id;
    - content: Message content (text);
    - time: When the message was processed in the server;
    - user: The user that sent the message;
        - name: User name;
        - color: User color (hexadecimal). Pattern: #RRGGBBAA (alpha is optional);
```json
{
  "type": "receive_message",
  "message": {
    "id": 2,
    "user": {
      "name": "HidekiHrk",
      "color": "#99ffbb"
      },
      "content": "Test message",
      "time": 1610237745259
  }
}
```
