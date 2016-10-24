#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase para un servidor de eco en UDP simple."""

import socketserver as SS
import sys
import time
import json


class SIPRegisterHandler(SS.DatagramRequestHandler):
    """Echo server class SIP."""

    Dicc = {}

    def register2json(self):
        """Rewrite the Dicctionary into a .json file."""
        json_file = open("registered.json", "w")
        json.dump(self.Dicc, json_file, separators=(',', ': '), indent=4)
        json_file.close()

    def json2registered(self):
        """Import json file if it exists."""
        try:
            with open("registered.json") as JsonFile:
                self.Dicc = json.load(JsonFile)
        except FileNotFoundError:
            self.Dicc = {}

    def handle(self):
        """Launch this procedure with each msg received."""
        self.wfile.write(b"Hemos recibido tu peticion")
        self.json2registered()
        msg = self.rfile.read().decode('utf-8')
        print("El cliente nos manda ", msg)

        if msg[:8] == "REGISTER":
            Dir = msg[msg.find("sip:") + 4: msg.rfind(" SIP/2.0")]
            Ip = self.client_address[0]

            Exp = int(msg[msg.find("Expires: ") + 9 : msg.find("\r\n\r\n")])
            time_ex = Exp + int(time.time())
            str_ex = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_ex))

            if Exp == 0:
                del self.Dicc[Dir]
                self.register2json()
            elif Exp > 0:
                self.Dicc[Dir] = {'address': Ip, 'Expires': str_ex}
                self.register2json()

            self.wfile.write(b" SIP/2.0 200 OK\r\n\r\n")


if __name__ == "__main__":
    """
    Main procedure of server.
    """

    try:
        serv = SS.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    except:
        sys.exit("Argument error")

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
