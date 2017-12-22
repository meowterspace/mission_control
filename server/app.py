import json
import uuid
import datetime
from flask import Flask
from flask_socketio import SocketIO, emit, send
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

data = {
  'time' : '',    #current Time
  'zone' : 'GMT', #timezone
  'serv' : '',    #time the server's been active
  'uuid' : ''     #unique message id
}

start = datetime.datetime.now()

@socketio.on('message')
def handle_message(message):

  if message == str(data['uuid']): print(message)
  else: print('Packet Loss!')

  data['time'] = str(datetime.datetime.now())
  data['serv'] = str(datetime.datetime.now()-start)
  data['uuid'] = str(uuid.uuid4())
  send(data)


if __name__ == '__main__':
  socketio.run(app)