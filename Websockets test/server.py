import time
from flask import Flask
from flask_socketio import SocketIO, emit, send
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


def bg_emit(count):
	send(count)	

@socketio.on('message')
def handle_message(message):
	print(message)
	
	for i in range(10):
		bg_emit(i)
		print(i)
		time.sleep(1)


if __name__ == '__main__':
	socketio.run(app)


