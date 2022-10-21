from flask import Flask, request, render_template
import socket

HOSTTOSERVER = '10.0.2.30'
PORTTOSERVER = 8822

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods =["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # get data
        account = request.form.get("account")
        password = request.form.get("password")
        # simple check data
        if len(account) == 0 or len(password) == 0:
            return render_template("index.html")

        # send data to other server

        # --------------- block 1 ----------------- #
        print("block 1")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOSTTOSERVER, PORTTOSERVER))

        clientMessage = f"1:{account},{password}"
        client.sendall(clientMessage.encode())
        print("wait")
        serverMessage = str(client.recv(1024), encoding='utf-8')
        print('Server:', serverMessage)



        client.close()
        # --------------- block 2 ----------------- #
        print("block 2")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOSTTOSERVER, PORTTOSERVER))

        clientMessage = f"2:{account},{password}"
        client.sendall(clientMessage.encode())

        serverMessage = str(client.recv(1024), encoding='utf-8')
        print('Server:', serverMessage)
        money = serverMessage
        client.close()

        # --------------- block 3 ----------------- #
        print("block 3")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOSTTOSERVER, PORTTOSERVER))

        clientMessage = f"3:{account},{password}"
        client.sendall(clientMessage.encode())

        serverMessage = str(client.recv(1024), encoding='utf-8')
        print('Server:', serverMessage)
        money = serverMessage
        client.close()
 
    else:
        return render_template("index.html")

    return render_template("signup.html", name=account, money=money)


    
if __name__ == "__main__":
    app.run(host="0,0,0,0", port="5000", debug=True)