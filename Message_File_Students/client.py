import socket
import sys
import time

def main():
    message_file = sys.argv[3]
    port = sys.argv[2]
    signature_file = sys.argv[4]
    server_address = sys.argv[1]

    # Read messages from the message file
    messages = []
    with open(message_file, 'r') as message_file:
        for line in message_file:
            num_bytes = int(line)
            message_data = message_file.read(num_bytes)
            messages.append(message_data.encode())
   
    # Read signatures from the signature file
    signatures = []
    with open(signature_file, 'r') as signature_file:
        for line in signature_file:
            signatures.append(line.strip())
    
    try:
        # Open a TCP socket to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, int(port)))

            # Send a "HELLO" message to the server
            client_socket.send(b"HELLO\n")
            print("waiting for response after hello")
            response = client_socket.recv(1024).decode()
            print(response)
            if response != "260 OK\n":
                
                return

            message_counter = 0

            # Iterate through messages
            for message in messages:
                # Send the DATA command to the server
                client_socket.send(b"DATA\n")
                
                client_socket.send(message+b"\n")
                
                
                client_socket.send(b".\n") 
               
                print(".\n") 
                
                response = client_socket.recv(8).decode()
                print(response, end='')
                if response != "270 SIG\n":
                    
                    return "response not sig"

                # Compare the received signature with the stored signature
                
                received_signature = client_socket.recv(1024).decode().strip()
                print(received_signature+"\n",end='')
                if received_signature == signatures[message_counter]:
                    client_socket.send(b"PASS\n")
                    
                else:
                    client_socket.send(b"FAIL\n")
                
                response = client_socket.recv(1024).decode()
    
                print(response, end='')

                if response != "260 OK\n":
                    
                    return

                message_counter += 1
                
                  
            
            
            # Send a QUIT message to the server
            client_socket.send(b"QUIT\n")
            

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()