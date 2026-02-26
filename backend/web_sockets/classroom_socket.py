from fastapi import WebSocket, WebSocketDisconnect, Depends
from utils.security import get_user_from_token
from sqlalchemy.orm import Session
from databases.session import get_db

class ClassroomManager:
    def __init__(self):
        # { "classroom_1": [ws1, ws2] }
        self.rooms: dict[str, list[WebSocket]] = {}
        self.usernames: dict[WebSocket, str] = {}

    async def connect(self, ws: WebSocket, room: str, username: str):
        await ws.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(ws)
        self.usernames[ws] = username

    async def disconnect(self, ws: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].remove(ws)
            # Clean up the room key if no one is left
            if not self.rooms[room]:
                del self.rooms[room]
        self.usernames.pop(ws, None)

    async def broadcast(self, room: str, message: dict):
        if room in self.rooms:
            for connection in self.rooms[room]:
                await connection.send_json(message)

# Global manager instance
manager = ClassroomManager()

async def classroom_room_socket(ws: WebSocket, classroom_id: int, db: Session = Depends(get_db)):
    token = ws.query_params.get("token")
    
    # Manual DB Session handling for WebSockets
    try:
        user = get_user_from_token(token, db)
        if not user:
            await ws.close(code=1008)
            return

        room_name = f"classroom_{classroom_id}"
        await manager.connect(ws, room_name, user.name)

        # Join Event
        await manager.broadcast(room_name, {
            "type": "event",
            "message": f"{user.name} joined"
        })

        while True:
            data = await ws.receive_json()
            if data["action"] == "some_action":
                # you could save submission to DB here
                await manager.broadcast(room_name, {
                    "type": "some_type",
                    "username" : user.name,
                    "message": f"{user.name} did some action"
                })
            
    except WebSocketDisconnect:
        await manager.disconnect(ws, room_name)
    finally:
        db.close() # CRITICAL: Always close the DB connection
