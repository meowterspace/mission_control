import time
from flask import Flask
from flask_socketio import SocketIO, emit, send
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


count = 0
@socketio.on('message')
def handle_message(message):
	print(message)
	count += 1
	send(count)


if __name__ == '__main__':
	socketio.run(app)



