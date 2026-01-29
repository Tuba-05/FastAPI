from fastapi import WebSocket, WebSocketDisconnect, Depends

from sqlalchemy.orm import Session
from databases.session import get_db

from utils.security import get_user_from_token

# { "exam_42": [ws1, ws2, ws3] }
exam_rooms = {} # dictionary is server memory.
connected_users = {}  # ws -> username

async def exam_room_socket(ws: WebSocket, exam_id: int, db: Session = Depends(get_db)):
    token = ws.query_params.get("token")
    user = get_user_from_token(token, db)

    username = user.name

    await ws.accept() # completes the handshake

    room = f"exam_{exam_id}"

    if room not in exam_rooms:
        exam_rooms[room] = []

    exam_rooms[room].append(ws) # student is officially inside the exam room.
    connected_users[ws] = username

     # JOIN EVENT
    await broadcast_message(room, {
        "type": "event",
        "message": f"{username}t joined the exam"
    })

    # Send updated/live count when someone joins
    await broadcast_count(room)

    try:
        while True:
            # user's submission response here 
            data = await ws.receive_json()

            if data["action"] == "submit_exam":
                # you could save submission to DB here
                await broadcast_message(room, {
                    "type": "submission",
                    "message": f"{username} submitted the exam"
                })

    # when user closes the page from frontend
    except WebSocketDisconnect:
        exam_rooms[room].remove(ws)
        connected_users.pop(ws, None)

        # LEAVE EVENT
        await broadcast_message(room, {
            "type": "event",
            "message": f"{username} left the exam"
        })
    
        await broadcast_count(room) 


async def broadcast_count(room):
    count = len(exam_rooms[room])
    for client in exam_rooms[room]:
        await client.send_json({
            "type": "count",
            "active_students": count
        })


async def broadcast_message(room, payload):
    for client in exam_rooms[room]:
        await client.send_json(payload)
