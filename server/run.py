from threading import Thread, Lock
import sys, os
import subprocess

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

file = open('game_data.txt', 'w')
file.write('00000000')
file.close()

server = subprocess

def help():
    print('''
start : starts server
 stop : shuts down server
 halt : stops the server instantly
 help : displays list of commands
 exit : closes this window, not the server
    ''')
                  
def start(ip='127.0.0.1', port='5000'):
    server_thread = Thread(target=server, args=(ip, port))
    server_thread.start()

def game_start():
    bytes = file.read()
    bytes[0] = 1
    file.write(bytes)
    file.close()
    print('Game started')


def game_pause():
    bytes = file.read()
    bytes[0] = 0
    file.write(bytes)
    file.close()
    print('Game paused')


def stop():
    print('WARNING: This will kill all running python processes on your computer.')
    while True:
        print('Do you with to continue? Y/N')
        i = input(': ')
        if i == 'Y':
            print('HALT')
            os.system('killall -9 python3')
        elif i == 'N': break
def exit():

    print('bye bye')
    sys.exit()
  
def admin():
    while True:
        cmd = input('> ')
        try:
            exec(cmd)
        
        except NameError:
            print('Unknown command. Type help for list of commands.')
        
def server(ip, port):
    _server = subprocess.Popen(['python3', 'app.pyw', ip, port])    

admin_thread = Thread(target=admin)
admin_thread.start()