# Python 3 server example
from functools import cache
from http.server import SimpleHTTPRequestHandler, HTTPServer
import io
import cgi
import os
import json
import socketserver
from urllib.parse import quote
from socketserver import ThreadingMixIn

hostName = "localhost"
serverPort = 8080
dirPath="./dir_path/"
cacheSize=1024*1024*64
cacheSize= 1370660
class  Cache:
    def __init__(self) -> None:
        self.cache = {}
        self.fileNames=[];
        pass
    def exists(self, fileName) ->bool:
        return fileName in self.cache;
    def add(self,fileName,fileData):
        newSize=self.size()+len(fileName)+len(fileData);
        # print(f"newSize -> {newSize}")
        while(newSize>cacheSize):
            self.removeLast();
            newSize=self.size()+len(fileName)+len(fileData);
            # print(f"newSize -> {newSize}")
            pass;
        self.cache[fileName]=fileData
        self.fileNames.append(fileName)
    def removeLast(self):
        # print(f"Removing from caches -> {self.fileNames}")
        key=self.fileNames[0];
        self.fileNames = self.fileNames[1:];
        # print(f"Removing from cache -> {key}")
        self.cache.pop(key)
        pass;
    def size(self):
        size=0;
        for key in self.cache:
            size=size+len(self.cache[key]);
        return size;
            
    def get(self, fileName):
        return self.cache[fileName];
        

myCache=Cache();
class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if(self.path=="/files/"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(os.listdir(dirPath)), "utf-8"))
            return;
        elif(self.path.startswith("/files/") and self.path != "/files/"):
            fileName=self.path[len("/files/"):]
            fileName=fileName.replace(" ", "%20")
            clientAddress=self.client_address[0]
            print(f"Client {clientAddress} is requesting file {fileName}")
            fileBytes='';
            if(myCache.exists(fileName)):
                print(f"Cache hit. {fileName} sent to the client");
                fileBytes=myCache.get(fileName);
                pass;
            else:
                print(f"Cache miss. {fileName} sent to the client");
                with open(f"{dirPath}{fileName}", 'rb') as file:
                    fileBytes=file.read();
                    myCache.add(fileName,fileBytes);
            self.send_response(200)
            self.send_header("Content-Length", str(len(fileBytes)))
            self.send_header("Content-Type", 'application/octet-stream')
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(fileName))
            self.end_headers()
            self.wfile.write(fileBytes)
    def do_POST(self):
        r, info = self.deal_post_data()
        # print(r, info, "by: ", self.client_address)
        response = io.BytesIO()
        if r:
            response.write(b"Success\n")
        else:
            response.write(b"Failed\n")
        length = response.tell()
        response.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if response:
            self.copyfile(response, self.wfile)
            response.close()      

    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        open(f"{dirPath}{record.filename}", "wb").write(record.file.read())
                else:
                    fileName=form["file"].filename;
                    open(f"{dirPath}{fileName}", "wb").write(form["file"].file.read())
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded")
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":        
    webServer = ThreadingSimpleServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")