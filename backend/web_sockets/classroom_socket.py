from fastapi import WebSocket, WebSocketDisconnect, Depends
from models.models import GroupMembers, Group
from utils.security import get_user_from_token
from sqlalchemy.orm import Session
from databases.session import get_db

class ClassroomManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}
        self.usernames: dict[WebSocket, str] = {}
        self.room_stats: dict[str, dict] = {}

    async def connect(self, ws: WebSocket, room: str, username: str):
        await ws.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        if room not in self.room_stats:
            self.room_stats[room] = {"total_joined": 0, "total_left": 0, "tap_count": 0}  # ✅ added tap_count

        self.rooms[room].append(ws)
        self.usernames[ws] = username
        self.room_stats[room]["total_joined"] += 1

    async def disconnect(self, ws: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].remove(ws)
            if not self.rooms[room]:
                del self.rooms[room]
        self.usernames.pop(ws, None)

        if room in self.room_stats:
            self.room_stats[room]["total_left"] += 1

    async def broadcast(self, room: str, message: dict):
        if room in self.rooms:
            for connection in self.rooms[room]:
                await connection.send_json(message)

    async def get_stats(self, room: str) -> dict:
        stats = self.room_stats.get(room, {"total_joined": 0, "total_left": 0, "tap_count": 0})
        return {
            "online": len(self.rooms.get(room, [])),
            "total_joined": stats["total_joined"],
            "total_left": stats["total_left"],
        }

    async def get_member_count(self, room: str) -> int:
        return len(self.rooms.get(room, []))

    async def get_member_names(self, room: str) -> list:
        return [self.usernames[ws] for ws in self.rooms.get(room, [])]

    
    async def increment_tap(self, room: str) -> int:
        if room not in self.room_stats:
            self.room_stats[room] = {"total_joined": 0, "total_left": 0, "tap_count": 0}
        self.room_stats[room]["tap_count"] += 1
        return self.room_stats[room]["tap_count"]
    
# Global manager instance
manager = ClassroomManager()

async def classroom_room_socket(ws: WebSocket, classroom_code: str, db: Session = Depends(get_db)):
    from urllib.parse import unquote
    token = unquote(ws.query_params.get("token", ""))

    # ✅ Normalize classroom_code to avoid casing/whitespace issues
    classroom_code = classroom_code.strip().upper()

    # ✅ Guard: check if classroom exists
    classroom = db.query(Group).filter(Group.class_code == classroom_code).first()
    if not classroom:
        await ws.accept()
        await ws.close(code=1008)
        return

    # ✅ Consistent room key using classroom_code directly
    room_name = f"classroom_{classroom_code}"

    try:
        user = get_user_from_token(token, db)
        if not user:
            await ws.accept()
            await ws.close(code=1008)
            return

        # Check enrollment
        is_member = db.query(GroupMembers).filter(
            GroupMembers.user_id == user.id,
            GroupMembers.group_id == classroom.id
        ).first()

        if not is_member:
            await ws.accept()
            await ws.close(code=1008)
            return

        # ✅ Mark user as online
        is_member.is_online = True
        db.commit()

        await manager.connect(ws, room_name, user.name)

        # Broadcast join event
        await manager.broadcast(room_name, {
            "type": "event",
            "message": f"{user.name} joined",
            "stats": manager.get_stats(room_name),      
            "active_students": manager.get_member_count(room_name),  # ✅
            "total_taps": manager.room_stats.get(room_name, {}).get("tap_count", 0)  # ✅
        })

        while True:
            data = await ws.receive_json()
            if data["action"] == "count_students":
                total_taps = manager.increment_tap(room_name)  # ✅ global tap count
                await manager.broadcast(room_name, {
                    "type": "count", # ✅ changed from "stats" to "count"
                    "active_students": manager.get_member_count(room_name),
                    "tapped_by": user.name,
                    "total_taps": total_taps  # ✅ send global tap count
                })

    except WebSocketDisconnect:
        # ✅ Mark user as offline
        is_member = db.query(GroupMembers).filter(
            GroupMembers.user_id == user.id,
            GroupMembers.group_id == classroom.id
        ).first()
        if is_member:
            is_member.is_online = False
            db.commit()

        await manager.disconnect(ws, room_name)
        await manager.broadcast(room_name, {
            "type": "event",
            "message": f"{user.name} left",
            "stats": manager.get_stats(room_name),
            "active_students": manager.get_member_count(room_name),  # ✅
            "total_taps": manager.room_stats.get(room_name, {}).get("tap_count", 0)  # ✅
        })

    finally:
        db.close()