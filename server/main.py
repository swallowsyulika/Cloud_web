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
    clientMessageFromWeb = str(conn.recv(1024), encoding='utf-8')

    print('Client message is:', clientMessageFromWeb)

    worktype, data = clientMessageFromWeb.split(":")
    worktype = int(worktype)

    if worktype == 0:
        # stop server
        KEEP = False
        clientMessageToDB = "0:"
    elif worktype == 1:
        # create account
        name, account, password = data.split(',')
        clientMessageToDB = f"1:{name},{account},{password}"


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CLIENTHOST, CLIENTPORT))
    client.sendall(clientMessageToDB.encode())

    serverMessageFromDB = str(client.recv(1024), encoding='utf-8')
    print('Server:', serverMessageFromDB)
    client.close()

    serverMessageToWeb = 'GOT'
    conn.sendall(serverMessageToWeb.encode())
    conn.close()

server.close()
