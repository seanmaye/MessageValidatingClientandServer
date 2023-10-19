import socket
import sys
import hashlib

def main():

    listen_port = int(sys.argv[1])
    key_file = sys.argv[2]

    # Read keys from the key file
    with open(key_file, 'r') as key_file:
        keys = [line.strip() for line in key_file]
    print(keys)
    # Create a socket and bind it to the specified port
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(('127.0.0.1', int(listen_port)))
    server_socket.listen(1)

       

    while True:
            key_index=0
            conn, addr = server_socket.accept()
            with conn:
                

                # Read the first line from the client
                hello_message = conn.recv(1024).decode().strip()
                
                if hello_message != "HELLO":
                    
                    conn.close()
                    continue
                conn.send(b"260 OK\n"+b"\r")
                while True:
                    
                    command = conn.recv(1024).decode().strip()
                    print(command)
                    if not command:
                        break

                    if command == "DATA":
                        # Start a new SHA-256 hash
                    
                        

                        sha256 = hashlib.sha256()
                        data_line = conn.recv(1024).decode().strip()
                        print(data_line)
                        if data_line == ".":
                            break
                        escaped_line = data_line.replace("\\n", "\n").replace("\\t", "\t")
                       
                        sha256.update(escaped_line.encode())
                        
                        # Add the key to the hash and finish the hash
                        print(key_index)
                        sha256.update(keys[key_index].encode())
                        signature = sha256.hexdigest()
                        key_index+=1

                        # Send 270 SIG status code back to the client
                        conn.send(b"270 SIG\n"+b"\r")
                        print(b"270 SIG\n"+b"\r")

                        # Send the signature on one line
                        conn.send(signature.encode() + b"\n"+b"\r")
                        print(signature.encode() + b"\n" +b"\r")
                        response = conn.recv(1024).decode().strip()
                        
                        if response not in ["PASS", "FAIL"]:
                           
                            conn.close()
                            break
                        conn.send(b"260 OK\n"+b"\r")
                        print(b"260 OK\n"+b"\r")
                    elif command == ".":
                        conn.send(b"260 OK\n"+b"\r")
                        print(b"260 OK\n"+b"\r")
                    elif command == "QUIT":
                        conn.close()
                        return

                    else:
                        conn.close()
                        return

if __name__ == "__main__":
    main()