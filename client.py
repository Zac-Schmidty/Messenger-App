import socket
import threading

host = "127.0.0.1"
port = 12003
address = (host, port)
nickname = input('Choose name >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(nickname.encode('utf-8'), address)  # send nickname to server one time

running = True

# receiving msgs from client
def exit():
    global runnning 
    running = False
    print("Exiting the chat...")
    client.close()
    sys.exit()

def receive():
    while running:
        try:
            message, server_addy = client.recvfrom(2048)
            print(message.decode('utf-8'))
            
        except:
            print("Error!")
            break

# sending msgs to client


def send():
    while running:
        msg = input("")
        if msg == 'EXIT':
            exit()
        full_msg = f'{nickname}: {msg}'
        client.sendto(full_msg.encode('utf-8'), address)

# thread to receive inputs from other clients or the server


receiveThread = threading.Thread(target=receive)
receiveThread.start()


# thread to send inputs to other clients through the server


sendThread = threading.Thread(target=send)
sendThread.start()
