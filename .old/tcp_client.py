from fileinput import filename
import requests
import json
url = "http://localhost:8080/files/"

payload={}
files={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)
filesList=list(json.loads(response.text));
import sys
host=sys.argv[1]
port=sys.argv[2]
fileName=sys.argv[3]
url = f"http://{host}:{port}/files/{fileName}"
if(fileName in filesList):
    print(url)
    payload={}
    files={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    open(sys.argv[3], 'wb').write(response.content)
    print(f"{fileName} saved")
else:
    print(f"File {fileName} does not exist in the server")
