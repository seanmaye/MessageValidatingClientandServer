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
    server_socket.bind(('127.0.0.1', int(listen_port)))
    server_socket.listen(1)

       

    while True:
            key_index=0
            conn, addr = server_socket.accept()
            with conn:
                recieved_data =conn.makefile('r',encoding='ascii', newline='')
                # Read the first line from the client
                print("waiting for first line from client")
                hello_message = recieved_data.readline()
                
                if hello_message != "HELLO\n":
                    
                    conn.close()
                    continue
                conn.send("260 OK\n".encode(encoding='ascii'))
                print("260 OK\n", end='')
                while True:
                    print("waiting for data quit etc")
                    command =recieved_data.readline()
                    print(command)
                    if not command:
                        break

                    if command == "DATA\n":
                        #maybe add while here
                        sha256 = hashlib.sha256()
                        print("waiting for data")
                        data_line = recieved_data.readline().strip
                        print(data_line)
                        if data_line == ".":
                            print("period detected")
                            break
                        escaped_line = data_line.replace("\\n", "\n").replace("\\t", "\t")
                       
                        sha256.update(escaped_line.encode())
                        
                        # Add the key to the hash and finish the hash
                        print(key_index)
                        sha256.update(keys[key_index].encode())
                        signature = sha256.hexdigest()
                        key_index+=1

                        # Send 270 SIG status code back to the client
                        conn.send("270 SIG\n".encode(encoding='ascii'))
                        print("270 SIG\n", end='')
                        

                        # Send the signature on one line
                        conn.send((signature+"\n").encode(encoding='ascii'))
                        print(signature+"\n", end='')
                        print("waiting for pass fail response")
                        response = recieved_data.readline()
                        
                        if response not in ["PASS\n", "FAIL\n"]:
                           
                            conn.close()
                            break
                        conn.send("260 OK\n".encode(encoding='ascii'))
                        print("260 OK\n", end='')
                    elif command == "QUIT\n":
                        conn.close()
                        return

                    else:
                        print("closing connection")
                        conn.close()
                        return

if __name__ == "__main__":
    main()