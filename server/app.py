import json
import uuid
import datetime
import os
import io
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit, send
from threading import Thread

app = Flask(__name__, template_folder='../client')
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
#app.config['APPLICATION_ROOT'] = '../client'
for i in app.config: print(i, app.config[i])

socketio = SocketIO(app)

data = {
  'time' : '',    #current Time
  'zone' : 'GMT', #timezone
  'serv' : '',    #time the server's been active
  'uuid' : '',    #unique message id
  'angle' : [0,0,0]
}

start = datetime.datetime.now()
@app.route('/')
def index():
  return render_template('ui.html')

@app.route('/resources/img/<path:path>')
def img_route(path):
  ext = os.path.splitext(path[-1].lower())
  if ext == '.jpg' or '.png' or '.gif':
    with open('../client/resources/img/'+str(path), 'rb') as bites:
      return send_file(
        io.BytesIO(bites.read()),
        #attatchment_filename=str(path),
        mimetype='image/'+str(ext)
      )

@app.route('/<path:path>')
def route(path):
  if os.path.exists('../client/'+str(path)) == True:
    return render_template('/'+str(path))
  else:
    return "ERROR 404: "+str(path)+" doesn't exist"


@socketio.on('message')
def handle_message(message):

  if message == str(data['uuid']): print(message)
  else: print('Packet Loss!')

  data['time'] = str(datetime.datetime.now())
  data['serv'] = str(datetime.datetime.now()-start)
  data['uuid'] = str(uuid.uuid4())
  data['angle'][0] = data['angle'][0]+0.01
  send(data)


if __name__ == '__main__':
  socketio.run(app)
