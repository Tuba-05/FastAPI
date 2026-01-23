from fastapi import WebSocket, WebSocketDisconnect
# from services.likes_service import increase_like_in_db

# In-memory storage of active WebSocket connections
# Format:
# {
#   "post_5": [ws1, ws2, ws3],
#   "post_10": [ws4, ws5]
# }
# Each key represents a "room" for one post
rooms = {}


async def post_likes_socket(ws: WebSocket, post_id: int):
    """
    Handles real-time WebSocket communication for a single post.

    Every post has its own room. All users viewing the same post
    are connected to the same room so that like updates are shared
    instantly.
    """

    # Accept the WebSocket connection from the client (browser / app)
    await ws.accept()

    # Create a room name for this post
    room = f"post_{post_id}"

    # If this is the first user for this post, create a new room
    if room not in rooms:
        rooms[room] = []

    # Add this user's WebSocket connection to the room
    rooms[room].append(ws)

    try:
        # Keep listening for messages from this user
        while True:
            # Receive JSON data from client
            # Example:
            # { "action": "like" }
            data = await ws.receive_json()

            # If the user clicked the "Like" button
            if data["action"] == "like":

                # Update the database and get the new like count
                new_likes = "" #  increase_like_in_db(post_id)

                # Broadcast the updated like count to all users
                # who are currently viewing this post
                for client in rooms[room]:
                    await client.send_json({
                        "post_id": post_id,
                        "likes": new_likes
                    })

    # If the user closes the page or loses connection
    except WebSocketDisconnect:

        # Remove their WebSocket from the room
        rooms[room].remove(ws)

        # (Optional but recommended)
        # If the room becomes empty, delete it to free memory
        if len(rooms[room]) == 0:
            del rooms[room]
