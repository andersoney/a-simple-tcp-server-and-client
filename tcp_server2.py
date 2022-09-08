import socket
IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
def main():
    print("[STARTING] Server is starting.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening.")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        method = conn.recv(SIZE).decode(FORMAT)
        conn.send("Received Method".encode(FORMAT))
        print(f"Method: {method}")
        if(method=="UPLOAD_FILE"):
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the filename.")
            file = open("dir_path/"+filename, "w")
            conn.send("Filename received.".encode(FORMAT))
            data = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))
            file.close()
        elif(method=="GET_FILE_LIST"):
            pass;
        elif(method=="GET_FILE"):
            pass;
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")
    
if __name__ == "__main__":
    main()