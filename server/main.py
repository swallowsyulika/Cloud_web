import socket
SERVERHOST = '127.0.0.1'
SERVERPORT = 8822
CLIENTHOST = '127.0.0.1'
CLIENTPORT = 9977
KEEP = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVERHOST, SERVERPORT))
server.listen(10)

while KEEP:
    conn, addr = server.accept()
    clientMessage = str(conn.recv(1024), encoding='utf-8')

    print('Client message is:', clientMessage)

    name, account, password = clientMessage.split(',')

    if name == "stop":
        KEEP = False
        clientMessage = "stop"
    else:
        clientMessage = f"0:{name},{account},{password}"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CLIENTHOST, CLIENTPORT))
    client.sendall(clientMessage.encode())

    serverMessage = str(client.recv(1024), encoding='utf-8')
    print('Server:', serverMessage)
    client.close()

    serverMessage = 'stop appaction server.'
    conn.sendall(serverMessage.encode())
    conn.close()

server.close()
