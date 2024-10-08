import socket
import threading

host = "127.0.0.1"
port = 12003

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

clients = {}

def broadcast(message, sender_address):
    for client_address in clients:
        if client_address != sender_address:
            server.sendto(message, client_address)

# function handle the connection of clients

def receive():
    while True:
        # might need to make a new port number and socket for new clients?
        try:
            message, address = server.recvfrom(2048)
            if address not in clients:
                nickname = message.decode('utf-8')
                clients[address] = nickname 
                print(f"New connection, {nickname}, from {address}")

                current_participants = ", ".join([name for addr, name in clients.items() if addr != address])
                
                # Send welcome message with current participants
                welcome_message = f"Welcome to the chat, {nickname}! \nTo leave the chat type 'EXIT'..."
                if current_participants:
                    welcome_message += f"\nCurrent participants: {current_participants}"
                else:
                    welcome_message += "\nYou're the first one here!"
                
                server.sendto(welcome_message.encode('utf-8'), address)

                broadcast(f"{nickname} just joined the chat!".encode('utf-8'), address)
            else:
                broadcast(message, address)
        except Exception as e:
            print(f"An error occurred: {e}")

# main function to receive connections from clients


if __name__ == "__main__":
    print("Server is running and listening for connections ...")
    receive()
