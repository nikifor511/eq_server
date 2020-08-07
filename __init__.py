from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from time import sleep

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 58583
BUFSIZ = 1024
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SOCK.accept()
        print("%s:%s has connected." % client_address)
        client.send("Greetings from the ChatRoom! ".encode("utf8"))
        # client.send("Now type your name and press enter!".encode("utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(conn, addr):

    conn.send(bytes("Welcome", "utf8"))
    clients[conn] = addr
    while True:
        msg = conn.recv(BUFSIZ)
        if msg != bytes("#quit", "utf8"):
            broadcast(msg, str(addr[0]) + ": ")
        else:
            # conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            # broadcast(bytes("%s has left the chat." % addr, "utf8"), "cc")
            print("User disconnected")
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SOCK.listen(5)  # Listens for 5 connections at max.
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()