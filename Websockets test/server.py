import time
import datetime
from flask import Flask
from flask_socketio import SocketIO, emit, send
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


@socketio.on('message')
def handle_message(message):
	print(message)
	x = str(datetime.datetime.now())
	send(x)


if __name__ == '__main__':
	socketio.run(app)