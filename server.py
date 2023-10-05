import socket
import select

HOST = ("192.168.0.106", 7777)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(HOST)
server.listen()
print("Server is ready!")

sockets_list = [server, ]

while True:
    rs, _, es = select.select(sockets_list, [], sockets_list)
    for _socket in rs:
        msg = b""
        try:
            if _socket is server:
                client, addr = server.accept()
                sockets_list.append(client)
                print(f"New connect by {client}")
            else:
                msg = _socket.recv(1024)
        except ConnectionResetError:
            sockets_list.remove(_socket)

        for client in sockets_list:
            if client != server and client != _socket:
                if msg:
                    client.sendall(msg)

    for _socket in es:
        sockets_list.remove(_socket)
