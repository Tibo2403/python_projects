# SOCKETS RESEAU : SERVEUR
#
# socket
#  bind (ip, port)
#  listen
#  accept -> socket / (ip, port)
#  close

import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion établie avec {client_address}")

while True:
    texte_envoye = input("Vous: ")
    connection_socket.sendall(texte_envoye.encode())
    data_recues = connection_socket.recv(MAX_DATA_SIZE)
    if not data_recues:
        break
    print("Message :", data_recues.decode())

s.close()
connection_socket.close()