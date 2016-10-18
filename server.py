#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        Dicc = {}
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'))
            msg = line.decode('utf-8')
            print(msg)
            if msg[0:8] == "REGISTER":
                Dicc = {self.client_address[0] : self.client_address[1]}
                self.wfile.write(b"200 OK")
                
                

if __name__ == "__main__":
    try:
        serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    except:
        sys.exit("Argument error")

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
