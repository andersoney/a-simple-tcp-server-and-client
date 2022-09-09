import socket
import threading
IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
def uploadFile(fileName):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    file = open(fileName, "r")
    data = file.read()
    client.send("UPLOAD_FILE".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    # print(f"[SERVER]: {msg}")
    client.send(fileName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    # print(f"[SERVER]: {msg}")
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    # print(f"[SERVER]: {msg}")
    """ Closing the file. """
    file.close()
    client.close()
    
def downloadFileList():
    listFiles=[]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send("GET_FILE_LIST".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    client.send("BEGIN_LIST".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    client.send("START".encode(FORMAT))
    while(True):
        if(msg=='END'):
            client.send("END_CONECTION".encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            client.close()
            break;
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            if(msg=='END'):
                continue;
            listFiles.append(msg);
            client.send("MORE".encode(FORMAT))
    print(f"Files In Servidor {listFiles}");
def downloadFile(fileName):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send("GET_FILE".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    client.send(fileName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    file = open("./dir_path_received/"+fileName, "w")
    file.write(msg)
    file.close()
    client.close()
    pass;


class ThreadProcess (threading.Thread):
    def __init__(self, threadID, name, counter,fileName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.fileName=fileName
    def run(self):
        # uploadFile(self.fileName);
        downloadFileList();
        downloadFile(self.fileName);
        pass;

def main():
    threadM = ThreadProcess(1, "Thread-1", 1,"makefile")
    thread1 = ThreadProcess(2, "Thread-2", 2,"1.log")
    thread2 = ThreadProcess(2, "Thread-2", 2,"2.log")
    thread3 = ThreadProcess(2, "Thread-2", 2,"3.log")
    thread4 = ThreadProcess(2, "Thread-2", 2,"4.log")
    threadM.start()
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    fileName="makefile"
    uploadFile(fileName);
    downloadFileList();
    downloadFile(fileName);
    
if __name__ == "__main__":
    main()