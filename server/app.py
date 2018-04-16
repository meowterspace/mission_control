# Import all external libraries
import json 
import datetime
import time
import os
import io
import errno
from flask import Flask, render_template, send_file, request, session, redirect, render_template_string
from flask_socketio import SocketIO, emit, send
from threading import Thread, Lock
import resources
import sys

print(sys.argv)


# This is a dictionary of all the settings Flask has. Since I have a complex setup it is best to have the 
# config ready at all times so I can quickly change server settings. This dictionary is a default dictionary
# and will be overwritten when the server starts with the settings specified in CONFIX.txt
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

# This library contains game data, such as the name, and whether or not the game is active. A lot of this isn't
# currently implimented however it outlines a plan of future development. Some elements like USER_LIST and 
# ACTIVE are used throughout the program.
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

users = [] # A list of all the current users in the game.

# This defines the user class.
class User:
  def __init__(self, name):
    self.name = name


#The code below is responsible for loading in the server settings from CONFIG.txt
if os.path.exists('CONFIG.txt') == True: # checks if CONFIG.txt exists yet
  with open('CONFIG.txt', 'r') as f: # if it does exist, open the file
    for line in f.readlines(): 
      line_split = line.strip().split("=") # For every line, split the left and right half at the = sign
      CONFIG[line_split[0].strip()] = line_split[1].strip() # Update CONFIG dictionary
    f.close() # close CONFIG.txt
else: # if it doesn't exit
  with open('CONFIG.txt', 'w') as f:  # Open CONFIG.txt (generates file) 
    for key in CONFIG:
      f.write(key+' = '+str(CONFIG[key])+'\n')   # write the default config to the file 
    f.close() # Close new file


# Flask server setup
app = Flask(__name__, template_folder='../client')  # Defines the Flask Server. The template_folder is set to 
                                                    # ../client (the client folder) which means the browser has
                                                    # no access to the server at all as it is in a different
                                                    # directory.
app.config['SECRET_KEY'] = 'secret' # Sets the server encryption key

app.config['DEBUG'] = CONFIG['DEBUG']  # Sets the server settings to equal CONFIG


for i in app.config: print(i, app.config[i])  # prints the new server CONFIG to the terminal

socketio = SocketIO(app) # Defines SOCKETIO app

# Below is a meta data dictionary that is to updated and sent with each websocket message 
# to the client so the message can be verified for debugging / tracking purposes, or 
# can be used to measure information loss in the websocket stream
meta = {
  'time' : '',    #current Time
  'zone' : 'GMT', #timezone
  'serv' : '',    #time the server's been active
  'uuid' : ''    #unique message id
}

start = datetime.datetime.now() # This represents the time the server started

#================== RUN =================================
player = resources.setup() # Calls the setup function in resources that returns a player object

#================== APP ROUTES - FLASK =================================


# This is the index route. If a user navigates to {ip}:{port}/ then this route will be run.
# It is set to render the index.html page when the GET request is recieved.
@app.route('/')
def index():
  return render_template('index.html')

# This is the login route. When a user submits their name in /index.html, before joining
# it is directed to /login. This route takes the data POSTed to it and assigns is to the 
# client specific session variable. The session is now indentifiable with that username.
@app.route('/login', methods=['POST'])
def login():
  if request.method == "POST":
    session['username'] = request.form['username']
    username = session['username']
    
    exec(str(username)+"=User('"+str(username)+"')") # this creates a new user class in the name of 
                                                     # the user POSTed to the server.
    print(session['username'])
    exec("print("+str(username)+".name)")

    GAME['USER_LIST'].append(username) # Adds the name to the list of current users
    print(session)
    return redirect('/lobby')          # redirects the client's page to /lobby
  return redirect(url_for('/')) # If nothing is posted to /login, send back to the index.

@app.route('/lobby')
def lobby():
  if session['username'] != None:  # If the user has logged in, this will render the lobby.html 
                                   # webpage.
    return render_template('lobby.html')

# This route is required if an image is requested from the server. Since the server can't send
# images or files over HTTP normally it has to encode it into byte data first and send it as a 
# string where the browser will automatically decode it at the other end because it knows the 
# mimetype to be image.
@app.route('/resources/img/<path:path>')
def img_route(path):
  ext = os.path.splitext(path[-1].lower())
  if ext == '.jpg' or '.png' or '.gif':
    with open('../client/resources/img/'+str(path), 'rb') as bites:
      return send_file(
        io.BytesIO(bites.read()),
        mimetype='image/'+str(ext)
      )

# This route is for anything else that hasn't been listed above. E.g Javascript/css files in
# the client folder. It takes the path and if the path exists, it will return what ever is 
# at that path location within /client folder. If there is nothing there it returns 404
@app.route('/<path:path>')
def route(path):
  if os.path.exists('../client/'+str(path)) == True:
    return render_template('/'+str(path))
  else:
    return "ERROR 404: "+str(path)+" doesn't exist"

#================== APP ROUTES - SOCKETIO ==============================

lock = Lock() # defines multithreading lock

# This socketIO decorator defines what happens when a websocket message is recieved on the
# open websocket channel ('/')
@socketio.on('message')
def handle_message(message):

  meta['time'] = str(datetime.datetime.now()) # updates the meta time
  meta['serv'] = str(datetime.datetime.now()-start) # updates the meta server time
  meta['uuid'] = str(uuid.uuid4()) # gives the meta a Unique ID

  to_send = {} 
  to_send.update(meta)
  # The below packages the meta data with the data from the server so it can all be
  # sent in one message rather than many different confusing messages that could 
  # get lost or fall out of time. The multithreading Lock is needed because the 
  # calculation thread is running seperate and both threads are unable to access
  # the same information at the same time, so the calculation thread is very 
  # quickly locked while the latest data is pulled and then unlocked.
  with lock:
    to_send.update(resources.data) 

  send(to_send) # send data via websockets to whoever sent the origional message


# This socketIO decorator defines what happens when a websocket message is recieved on the
# /update namespace channel. This channel is used for user input, so it runs the update
# function in resources.py with the message (new updated data) as the parameter
# so the data can be updated. Again this requires a Thread Lock.
@socketio.on('message', namespace='/update')
def handle_incoming_data(message):
  print('Incoming Data: '+str(message))
  with lock:
    resources.update(player, message)
  print(resources.data)
  print('Data updated')

# This socketIo decorator defines what happens when a websocket message is recieved
# on the /lobbu channel (from lobby.html). All it needs to do is simply send 
# the game information back to the client that requested it
@socketio.on('message', namespace='/lobbu')
def handle_lobby_message(message):
  send(GAME)

#================== THREADS ==============================

# This defines the compute thread. This runs seperately from everything else
# in this script so that it can run in real time and wont be interruped by any 
# other processes.
def compute(time):
  while True:
    for i in resources.OBJECTS: # This is for gravity purposes. It runs the calculation against
      if (i[1] == 'planet'): resources.run(i[0], player, time) # every object in the game (bar the player)
      global resources.data
    time.sleep(time) # waits interval before running calculations again.


if __name__ == '__main__':
  compute_thread = Thread(target=compute, args=(0.1)) # Here the thread is actually set up with the parameter 0.1 second delay
  compute_thread.start() # Starts the thread
  socketio.run(app) # Starts the server app
