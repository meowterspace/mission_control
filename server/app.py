import json
import uuid
import datetime
import os
import io
import errno
from flask import Flask, render_template, send_file, request, session, redirect, render_template_string
from flask_socketio import SocketIO, emit, send
from threading import Thread
import resources

header = '''
<head>
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.8/socket.io.min.js"></script>
</head>
<body>
<script type="text/javascript">
$(document).ready(function() {
  var lobby = io.connect('http://127.0.0.1:5000/lobbu');


  lobby.on('connect', function() {
    lobby.send('hi');


  });

  lobby.on('message', function(msg) {
  	var user_table = '<table style="border: 1px solid #000000">';
  	for (var i=1; i <= msg.USER_LIST.length; i++) {
  		user_table = user_table + '<tr><td>'+msg.USER_LIST[i-1]+'</td></tr>';
  	}
  	user_table = user_table + '</table>';
    document.getElementById('party').innerHTML = user_table;
    lobby.send('hi');
  });
});
</script>
<div id='party'></div>
</body>

'''

CONFIG = {
  'JSON_AS_ASCII': True,
  'USE_X_SENDFILE': False, 
  'SESSION_COOKIE_PATH': None, 
  'SESSION_COOKIE_DOMAIN': None, 
  'SESSION_COOKIE_NAME': 'session', 
  'DEBUG': False, 
  'LOGGER_HANDLER_POLICY': 'always', 
  'LOGGER_NAME': None, 
  'SESSION_COOKIE_SECURE': False, 
  'SECRET_KEY': None, 
  'EXPLAIN_TEMPLATE_LOADING': False, 
  'MAX_CONTENT_LENGTH': None, 
  'PROPAGATE_EXCEPTIONS': None, 
  'APPLICATION_ROOT': None, 
  'SERVER_NAME': None, 
  'PREFERRED_URL_SCHEME': 'http', 
  'JSONIFY_PRETTYPRINT_REGULAR': True, 
  'TESTING': False, 
  'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 
  'TEMPLATES_AUTO_RELOAD': None, 
  'TRAP_BAD_REQUEST_ERRORS': False, 
  'JSON_SORT_KEYS': True, 
  'JSONIFY_MIMETYPE': 'application/json',
  'SESSION_COOKIE_HTTPONLY': True, 
  'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 
  'PRESERVE_CONTEXT_ON_EXCEPTION': None, 
  'SESSION_REFRESH_EACH_REQUEST': True, 
  'TRAP_HTTP_EXCEPTIONS': False
}

GAME = {
  'GAME_NAME': None,
  'DESCRIPTION': None,
  'DIFFICULTY': 0,
  'ONLINE_MODE': True,
  'WHITE_LIST': False,
  'BLACK_LIST': False,
  'CHEATS': False,
  'MAX_GAME_LENGTH': None,
  'BANNED_USERNAMES': False,
  'SCINARIO': False,
  'ACTIVE': False,
  'USER_LIST': []
}

users = []

class User:
  def __init__(self, name):
    self.name = name


# MAKE CONFIG FILE
if os.path.exists('CONFIG.txt') == True:
  with open('CONFIG.txt', 'r') as f:
    for line in f.readlines():
      line_split = line.strip().split("=")
      CONFIG[line_split[0].strip()] = line_split[1].strip()
    f.close()
else:
  with open('CONFIG.txt', 'w') as f:
    for key in CONFIG:
      f.write(key+' = '+str(CONFIG[key])+'\n')
    f.close()

app = Flask(__name__, template_folder='../client')
app.config['SECRET_KEY'] = 'secret'

app.config['DEBUG'] = CONFIG['DEBUG']

#app.config['APPLICATION_ROOT'] = '../client'
for i in app.config: print(i, app.config[i])

socketio = SocketIO(app)


meta = {
  'time' : '',    #current Time
  'zone' : 'GMT', #timezone
  'serv' : '',    #time the server's been active
  'uuid' : ''    #unique message id
}

start = datetime.datetime.now()

#================== APP ROUTES - FLASK =================================

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
  if request.method == "POST":
    session['username'] = request.form['username']
    username = session['username']
    
    exec(str(username)+"=User('"+str(username)+"')")
    
    print(session['username'])
    exec("print("+str(username)+".name)")

    GAME['USER_LIST'].append(username)
    print(session)
    return redirect('/lobby')
  return redirect(url_for('/'))

@app.route('/lobby')
def lobby():
  if session['username'] != None:
    #return render_template_string(header)
    return render_template('lobby.html')

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

#================== APP ROUTES - SOCKETIO ==============================

@socketio.on('message')
def handle_message(message):

  if message == str(meta['uuid']): print(message)
  else: print('Packet Loss!')

  meta['time'] = str(datetime.datetime.now())
  meta['serv'] = str(datetime.datetime.now()-start)
  meta['uuid'] = str(uuid.uuid4())

  to_send = {}
  to_send.update(meta)
  to_send.update(resources.data)
  send(to_send)


@socketio.on('message', namespace='/lobbu')
def handle_lobby_message(message):
  send(GAME)

if __name__ == '__main__':
  socketio.run(app)
