from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}  # store chat history for each room

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']

    join_room(room)

    if room not in rooms:
        rooms[room] = []

    # Send previous messages to new user
    emit('chat_history', rooms[room], room=request.sid)

    # Broadcast join message
    msg = f"{username} has joined the room."
    rooms[room].append(msg)
    emit('message', msg, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    msg = f"{username}: {data['msg']}"

    rooms[room].append(msg)
    emit('message', msg, room=room)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
