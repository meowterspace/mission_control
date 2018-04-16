from threading import Thread, Lock
import sys, os
import subprocess

# This is the server admin panel

# prints title text
print( '''
  __  __          _____          _____         ____     ___     ___     ___    
 |  \/  |        / ____|        / ____|       |___ \   / _ \   / _ \   / _ \   
 | \  / |       | |            | (___           __) | | | | | | | | | | | | |  
 | |\/| |       | |             \___ \         |__ <  | | | | | | | | | | | |  
 | |  | |  _    | |____   _     ____) |  _     ___) | | |_| | | |_| | | |_| |  
 |_|  |_| (_)    \_____| (_)   |_____/  (_)   |____/   \___/   \___/   \___/

 Welcome to the Mission Control Simulator 3000. Type a command below.
 To get help type 'help'
''')

file = open('game_data.txt', 'w') # creates and resets the game_data.txt file
file.write('00000000')
file.close()

server = subprocess # sets up the server as a subprocess so it will run independantly
                    # of this admin panel


# Prints help functions
def help():
    print('''
        start : starts server
         stop : shuts down server
   game_start : starts the simulation.
   game_pause : pauses the simulation
         help : displays list of commands
         exit : closes this window, not the server
    ''')
              
# starts the server on the defined IP and Port                  
def start(ip='127.0.0.1', port='5000'):
    server_thread = Thread(target=server, args=(ip, port))
    server_thread.start()

# Starts the simulation by writing a value of 1 to the game flag in game_data.txt
def game_start():
    bytes = file.read()
    bytes[0] = 1
    file.write(bytes)
    file.close()
    print('Game started')

# pauses the simulation by writing a value of 0 to the game flag.
def game_pause():
    bytes = file.read()
    bytes[0] = 0
    file.write(bytes)
    file.close()
    print('Game paused')

# This function stops the server. It will ask the user if they want to do this first
# as it executes a command to kill subprocesses which they may have running in the 
# background.
def stop():
    print('WARNING: This will kill all running python processes on your computer.')
    while True:
        print('Do you with to continue? Y/N')
        i = input(': ')
        if i == 'Y':
            print('HALT')
            os.system('killall -9 python3')
        elif i == 'N': break

# exits the admin panel
def exit():
    print('bye bye')
    sys.exit()

# This is main function for this script. It continually executes the user input
# in a loop. Once the function requested has been executed it returns to the beginning.
# if the function isn't defined above it prints that it doesn't understand the command.
def admin():
    while True:
        cmd = input('> ')
        try:
            exec(cmd)
        
        except NameError:
            print('Unknown command. Type help for list of commands.')
       
# This defines the server subprocess using the subprocess library. 
def server(ip, port):
    _server = subprocess.Popen(['python3', 'app.pyw', ip, port])    

admin_thread = Thread(target=admin) 
admin_thread.start() # Ths starts this program (admin panel) as a thread that runs along side 
                     # the server subprocess, so that it can continually run in a loop without
                     # interfeering with the server or the simulation.