
from flask import Flask
from flask_socketio import SocketIO
import eventlet
import time
import math

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def data_generation(count) -> tuple:
    return ('sin_wave', {'x': count, 'y': math.sin(count)})


def background_thread():
    count = 0
    while True:
        socketio.sleep(0.001)  # Emit at 1ms intervals
        count += 0.1
        data_name,data_json = data_generation(count)
        socketio.emit(data_name, data_json)

if __name__ == '__main__':
    # Start background thread only once, not per client connect
    if not hasattr(app, 'thread_started'):
        app.thread_started = True
        eventlet.spawn(background_thread)
    socketio.run(app, debug=True)
