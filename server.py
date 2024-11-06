import socket # importerar modul för att skapar nätverksanslutningar
import threading # importerar modul för att skapar trådar så serven kan köra flera klienter

# servens IP-adress och portnummer
HOST = '127.0.0.1'
PORT = 12345

# lista för alla anslutna klienter
clients_online: list = []

# funktion för en klientanslutning till servern
def handel_client(client_sock, client_addr):
    print(f"Klient ansluten från {client_addr}")
    clients_online.append(client_sock)
    while True:
        try:
            # tar emot klientens meddelande
            message = client_sock.recv(1024).decode('utf-8')
            if not message:
                print(f"klient frånkopplad från {client_addr}")
                clients_online.remove(client_sock) # tar bort klient från listan av anslutna klienter
                break
            
            # skickar meddelande till anslutna klienter
            print(f"meddelande från {client_addr}: {message}")
            for client in clients_online:
                if client != client_sock:
                    client.sendall(f"{client_addr} säger: {message}".encode('utf-8'))
        except:
            # tar bort en klient från listan av anslutna klienter
            print(f"Anslutning förlorad till {client_addr}")
            clients_online.remove(client_sock)
            break

# funktion som kör serven och väntar på att klienter ska ansluta till den 
def chat_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT)) # binder serven till IP-adressen och dess port
        server_sock.listen() # Lyssnar efter anslutningar
        print(f"serven körs på {HOST}: {PORT}")
        print("Väntar på anslutningar så folk kan börja chatta. ")
        while True:
            # accepterar anslutning och skapar en tråd
            client_sock, client_addr = server_sock.accept()
            threading.Thread(target=handel_client,args=(client_sock, client_addr)).start()

# startar servern
chat_server()
