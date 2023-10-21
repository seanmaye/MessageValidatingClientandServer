import socket
import sys

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
            received_data = client_socket.makefile('r',encoding='ascii',newline='')
            # Send a "HELLO" message to the server
            client_socket.send("HELLO\n".encode(encoding='ascii'))
            print("waiting for response after hello")
            response = received_data.readline()
            print(response)
            if response != "260 OK\n":
                print("fuck")
                return

            message_counter = 0

            # Iterate through messages
            for message in messages:
                # Send the DATA command to the server
                client_socket.send("DATA\n".encode(encoding='ascii'))
                client_socket.send(message+"\n".encode(encoding='ascii'))
                print("DATA\n", end='')
                print(message,end='')
                #client_socket.send(".\n".encode(encoding=ascii)) 
                print("."+"\n", end='') 
                print("waiting for response after DATA and message")
                response = received_data.readline()
                print("Response after sending data and message: "+response)
                if response != "270 SIG\n":
                    
                    return "response not sig"

                # Compare the received signature with the stored signature
                print("waiting for signature")
                received_signature = client_socket.recv(1024).decode().strip()
                print("Received signature: "+received_signature)
                print("Our signature: "+ signatures[message_counter])
                if received_signature == signatures[message_counter]:
                    client_socket.send("PASS\n".encode(encoding='ascii'))
                    print("PASS\n", end='')
                else:
                    client_socket.send("FAIL\n".encode(encoding='ascii'))
                    print("FAIL\n",end='')
                print("response after pass or fail")
                response = received_data.readline()
                print(response)

                if response != "260 OK\n":
                    
                    return

                message_counter += 1
                
                  
            
            
            # Send a QUIT message to the server
            client_socket.send(b"QUIT\n"+b"\r")
            print(b"QUIT\n"+b"\r")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()