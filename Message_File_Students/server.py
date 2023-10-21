import socket
import sys
import hashlib
import time
def main():

    listen_port = int(sys.argv[1])
    key_file = sys.argv[2]

    # Read keys from the key file
    with open(key_file, 'r') as key_file:
        keys = [line.strip() for line in key_file]
    
    # Create a socket and bind it to the specified port
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(('localhost', int(listen_port)))
    server_socket.listen(1)

       

    while True:
            key_index=0
            conn, addr = server_socket.accept()
            with conn:
                

                # Read the first line from the client
                print("waiting for first line from client")
                hello_message = conn.recv(1024).decode()
                
                if hello_message != "HELLO\n":
                    print("not hello")
                    conn.close()
                    continue
                conn.send(b"260 OK\n")
                while True:
                    print("waiting for data quit etc")
                    command = conn.recv(5).decode()
                    print("data quit etc " +command)
                    if not command:
                        break

                    if command == "DATA\n":
                        sha256 = hashlib.sha256()
                        print("waiting for data")
                        recieved = conn.recv(1).decode()
                        data_line = ""
                        print("Dataline: "+data_line)

                        while(recieved!="."):
                            data_line = data_line+ recieved
                            recieved=conn.recv(1).decode()
                            #print(data_line)
                        
                        
                            
                        escaped_line = data_line.replace("\\n", "\n").replace("\\t", "\t")
                       
                        sha256.update(escaped_line.encode())
                        
                        # Add the key to the hash and finish the hash
                        print(key_index)
                        sha256.update(keys[key_index].encode())
                        signature = sha256.hexdigest()
                        key_index+=1

                        # Send 270 SIG status code back to the client
                        conn.send(b"270 SIG\n")
                           
                        print("270 SIG\n", end='')

                        # Send the signature on one line
                        conn.send(signature.encode() + b"\n")
                            
                        print(signature+"\n",end='')
                        print("waiting for pass fail response\n",end='')
                        response = conn.recv(1024).decode()
                        response = conn.recv(1024).decode()
                        print("response: "+response+"after",end='')
                        if response not in ["PASS\n", "FAIL\n"]:
                           
                            conn.close()
                            break
                        conn.send(b"260 OK\n")
                           
                        print("260 OK\n",end='')
                    elif command == "QUIT\n":
                        conn.close()
                        return
                    elif command==".\n":
                        print("period")
                    else:
                        print("closing connection")
                        conn.close()
                        return

if __name__ == "__main__":
    main()