#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    MSG_TYPE = sys.argv[3]
    DIRECCTION = sys.argv[4]
    EXPIRES = sys.argv[5]

except:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    if MSG_TYPE == "register":
        Message = ("REGISTER sip:" + DIRECCTION + " SIP/2.0\r\n")
        Message += ("Expires: " + EXPIRES + "\r\n\r\n")
        print("Enviando:", Message)
        my_socket.send(bytes(Message, 'utf-8'))

    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
