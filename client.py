import threading
import socket

# Serverns IP-adress och portnummer
HOST = '127.0.0.1'
PORT = 12345

# Tar emot och skriver ut meddelanden från servern
def recv_messanger(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            # om ett meddelande kommer från servern skrivs det ut
            if message:
                print(message)
        except ConnectionResetError:
            break
        
# skapar en klient-socket som är ansluten till servern        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
    client_sock.connect((HOST, PORT))
    print("Ansluten till serven")
    
    # tråd för att ta emot meddelanden
    threading.Thread(target=recv_messanger,args=(client_sock,)).start()
    while True:
        message = input("Skriv: ") 
        # skickar meddelande till servern
        client_sock.sendall(message.encode('utf-8'))   