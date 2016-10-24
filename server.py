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
    Dicc = {}
    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        
        msg = self.rfile.read().decode('utf-8')
        print("El cliente nos manda ", msg)

        if msg[:8] == "REGISTER":
            Dir = msg[msg.find("sip:") + 4 : msg.rfind(" SIP/2.0")]
            Exp = int(msg[msg.find("Expires: ") + 9 : msg.find("\r\n\r\n")])
            Ip = self.client_address[0]
            if Exp == 0:
                del self.Dicc[Dir]
            elif Exp > 0:
                self.Dicc[Dir] = {'address': Ip, 'Expires': Exp}
            
            self.wfile.write(b"200 OK")
        print(self.Dicc)


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
