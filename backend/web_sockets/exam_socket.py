from fastapi import WebSocket, WebSocketDisconnect

# { "exam_42": [ws1, ws2, ws3] }
exam_rooms = {} # dictionary is server memory.

async def exam_room_socket(ws: WebSocket, exam_id: int):
    await ws.accept() # completes the handshake

    room = f"exam_{exam_id}"

    if room not in exam_rooms:
        exam_rooms[room] = []

    exam_rooms[room].append(ws) # student is officially inside the exam room.

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
                    "student": data["student"]
                })

    # when user closes the page from frontend
    except WebSocketDisconnect:
        exam_rooms[room].remove(ws)
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
