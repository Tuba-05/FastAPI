from fastapi import WebSocket, WebSocketDisconnect, Depends
from models.models import GroupMembers, Group
from utils.security import get_user_from_token
from sqlalchemy.orm import Session
from databases.session import get_db

class ClassroomManager:
    def __init__(self):
        # { "classroom_1": [ws1, ws2] }
        self.rooms: dict[str, list[WebSocket]] = {}
        self.usernames: dict[WebSocket, str] = {}
        self.room_stats: dict[str, dict] = {}  # ← track stats per room

    async def connect(self, ws: WebSocket, room: str, username: str):
        await ws.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        if room not in self.room_stats:
            self.room_stats[room] = {"total_joined": 0, "total_left": 0}  # init stats

        self.rooms[room].append(ws)
        self.usernames[ws] = username
        self.room_stats[room]["total_joined"] += 1 # update stats on new connection

    async def disconnect(self, ws: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].remove(ws)
            # Clean up the room key if no one is left
            if not self.rooms[room]:
                del self.rooms[room]
        self.usernames.pop(ws, None)

        if room in self.room_stats:
            self.room_stats[room]["total_left"] += 1 # update stats on disconnect

    async def broadcast(self, room: str, message: dict):
        if room in self.rooms:
            for connection in self.rooms[room]:
                await connection.send_json(message)


    def get_stats(self, room: str) -> dict:
        stats = self.room_stats.get(room, {"total_joined": 0, "total_left": 0})
        return {
            "online": len(self.rooms.get(room, [])),
            "total_joined": stats["total_joined"],
            "total_left": stats["total_left"],
        }
    
    # Add helper methods to manager
    def get_member_count(self, room: str) -> int:
        return len(self.rooms.get(room, []))

    def get_member_names(self, room: str) -> list:
        return [self.usernames[ws] for ws in self.rooms.get(room, [])]            


# Global manager instance
manager = ClassroomManager()

async def classroom_room_socket(ws: WebSocket, classroom_code: str, db: Session = Depends(get_db)):
    # Get token from query params or function argument
    from urllib.parse import unquote
    token = unquote(ws.query_params.get("token", ""))
    
    name_of_room = db.query(Group).filter(Group.class_code == classroom_code).first()
    # Manual DB Session handling for WebSockets
    room_name = f"classroom_{name_of_room.group_name}_{name_of_room.id}"  # unique room name based on classroom id and name
    try:
        user = get_user_from_token(token, db)
        if not user:
            await ws.close(code=1008)
            return
        
        # checking enrollement status of the user in the classroom
        is_member = db.query(GroupMembers).filter(GroupMembers.user_id == user.id, GroupMembers.group_id == name_of_room.id).first()

        if not is_member:
            await ws.close(code=1008)
            return

        # ✅ Mark user as online
        is_member.is_online = True
        db.commit()    

        await manager.connect(ws, room_name, user.name)

        # Join Event
        await manager.broadcast(room_name, {
            "type": "event",
            "message": f"{user.name} joined",
            "stats": manager.get_stats(room_name)
        })

        while True:
            data = await ws.receive_json()
            if data["action"] == "count_students":
                await manager.broadcast(room_name, {
                    "type": "count",
                    "active_students": manager.get_member_count(room_name),
                    "tapped_by": user.name  # ✅ who tapped
                })    
            
    except WebSocketDisconnect:
        # ✅ Mark user as offline on disconnect
        is_member = db.query(GroupMembers).filter(
            GroupMembers.user_id == user.id,
            GroupMembers.group_id == name_of_room.id
        ).first()
        if is_member:
            is_member.is_online = False
            db.commit()

        await manager.disconnect(ws, room_name)
        await manager.broadcast(room_name, {   # notifying others
        "type": "event",
        "message": f"{user.name} left",
        "stats": manager.get_stats(room_name)
    })
    finally:
        db.close() # CRITICAL: Always close the DB connection
