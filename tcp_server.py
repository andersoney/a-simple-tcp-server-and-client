import os
import socket
import threading
import sys


IP = socket.gethostbyname(socket.gethostname())
# PORT = 4455
PORT = int(sys.argv[1])
# print(f"PORT -> {PORT}")
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
dirPath=sys.argv[2]
# print(f"dirPath -> {dirPath}")
cacheSize= 1024*1024*64
lock = threading.Lock()
class  Cache:
    def __init__(self) -> None:
        self.cache = {}
        self.fileNames=[];
        pass
    def exists(self, fileName) ->bool:
        # print(self.cache);
        return fileName in self.cache;
    def add(self,fileName,fileData):
        newSize=self.size()+len(fileName)+len(fileData);
        # print(f"newSize -> {newSize} -{cacheSize}");
        while(newSize>cacheSize):
            self.removeLast();
            newSize=self.size()+len(fileName)+len(fileData);
            pass;
        self.cache[fileName]=fileData
        # print(self.cache);
        self.fileNames.append(fileName)
        
        
    def removeLast(self):
        # print(f"AA->{self.fileNames}")
        key=self.fileNames[0];
        self.fileNames = self.fileNames[1:];
        self.cache.pop(key)
        # print(f"REMOVING -> {key}")
        pass;
    def size(self):
        size=0;
        for key in self.cache:
            size=size+len(self.cache[key]);
        return size;
            
    def get(self, fileName):
        return self.cache[fileName];

myCache=Cache();

class ThreadProcess (threading.Thread):
    def __init__(self, threadID, name, counter,conn,addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.conn=conn;
        self.addr=addr;
        
    def run(self):
        conn=self.conn
        addr=self.addr
        # print(f"[NEW CONNECTION] {addr} connected.")
        method = conn.recv(SIZE).decode(FORMAT)
        conn.send("Received Method".encode(FORMAT))
        if(method=="UPLOAD_FILE"):
            self.uploadFile(conn)
        elif(method=="GET_FILE_LIST"):
            self.getFileList(conn);
        elif(method=="GET_FILE"):
            self.downloadFile(conn);
            
        conn.close()
        # print(f"[DISCONNECTED] {str(addr)} disconnected.")
        
    def getFileList(self,conn):
        start = conn.recv(SIZE).decode(FORMAT)
        if(start=="BEGIN_LIST"):
            conn.send("BEGIN_LIST".encode(FORMAT))
            start = conn.recv(SIZE).decode(FORMAT)
            listFile=os.listdir(dirPath)
            for file in listFile:
                conn.send(file.encode(FORMAT))
                msg = conn.recv(SIZE).decode(FORMAT)
                pass;
            conn.send("END".encode(FORMAT))
            msg = conn.recv(SIZE).decode(FORMAT)
        pass;
    def downloadFile(self,conn):
        msg = conn.recv(SIZE).decode(FORMAT)
        fileName=msg
        print(f"Client {self.addr} is requesting file {fileName}")
        lock.acquire();
        if(myCache.exists(fileName)):
            print(f"Cache hit. {fileName} sent to the client")
            data=myCache.get(fileName);
            pass;
        else:
            print(f"Cache miss. {fileName} sent to the client")
            filePath=f"{dirPath}/{fileName}"
            file = open(filePath, "r")
            data = file.read()
            myCache.add(fileName,data);
            file.close();
            pass;
        lock.release();
        conn.send(data.encode(FORMAT))
        pass;
    def uploadFile(self,conn):
        msg = conn.recv(SIZE).decode(FORMAT)
        file = open(f"./{dirPath}/{msg}", "w")
        conn.send("Filename received.".encode(FORMAT))
        data = conn.recv(SIZE).decode(FORMAT)
        file.write(data)
        conn.send("File data received".encode(FORMAT))
        file.close()
        pass;

def main():
    # print("[STARTING] Server is starting.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    # print("[LISTENING] Server is listening.")
    while True:
        conn, addr = server.accept()
        thread1 = ThreadProcess(1, "Thread-1", 1,conn,addr)
        thread1.start();
        
    
if __name__ == "__main__":
    main()
    