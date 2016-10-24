#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver as SS
import sys
import time
import json

class SIPRegisterHandler(SS.DatagramRequestHandler):
    """
    Echo server class
    """
    Dicc = {}
    def register2json(self):
        '''
        Rewrites the Dicctionary into a .json file
        '''
        json_file = open("registered.json", "w")
        json.dump(self.Dicc, json_file, separators=(',', ': '), indent=4)
        json_file.close()

        
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
                self.register2json()
            elif Exp > 0:
                self.Dicc[Dir] = {'address': Ip, 'Expires': Exp}
                self.register2json()
            
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")


if __name__ == "__main__":
    try:
        serv = SS.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    except:
        sys.exit("Argument error")

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
