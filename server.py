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
        
        msg = self.rfile.read().decode('utf-8')
        print("El cliente nos manda ", msg)

        if msg[:8] == "REGISTER":

            Dir = msg[msg.find("sip:"): msg.rfind(" SIP/2.0")]
            Dicc = {Dir : self.client_address[0]}
            self.wfile.write(b"200 OK")
        print(Dicc)


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
