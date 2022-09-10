## Project description

In this project. In first moment i make am api, but this is a error of interpretation, end, in this moment, begin.

In first make a conection, with listiner in a port. This aplication only listiner all time, wait a mensage to begin the process. 

after received the conection, a method is receive, with this, change the sequential process to upload, list all file in folder or download file. 

After create earch feat, is necessary the thread funcion, this is simple, only receive the conection and send this to thread to manager the message. After this. Have a problem. The application can use cache. The cache is a dict with if a file have in process. Can restore the bits from send. If not have, i can get the file from disk, but if the cache is full? I need remove the last file to enter in cache. From this i have a list ordened, i get the fist element, remove and remove by key from dict. 

With cache finished, i go to problem of lock. In test i can see with the application have error from get a file with not exist in cache. But, using lock this problem can be solved ease. 

## decisions.
I use dict in cache but this is equivalent to use a hashmap in java. The file is intuitive the key to get values.

Use thread to process all flow after begin conect for simplicity.

I use message with 1MB because with this i can send more data. and can fill the cache fast.
