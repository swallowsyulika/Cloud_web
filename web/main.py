from flask import Flask, request, render_template
import socket

HOST = '127.0.0.1'
PORT = 8822

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods =["GET", "POST"])
def get_data():
    if request.method == "POST":
        # get data
        name = request.form.get("name")
        account = request.form.get("account")
        password = request.form.get("password")
        # simple check data
        if len(name) == 0 or len(account) == 0 or len(password) == 0:
            return render_template("index.html")

        # send data to other server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        clientMessage = f"{name},{account},{password}"
        client.sendall(clientMessage.encode())

        serverMessage = str(client.recv(1024), encoding='utf-8')
        print('Server:', serverMessage)
        client.close()
    else:
        return render_template("index.html")

    return f"<h1>Succeeded! Welcome, {name}, u are criminal now! (laugh.</h1>"
    
if __name__ == "__main__":
    print("a")
    app.run(debug=True)