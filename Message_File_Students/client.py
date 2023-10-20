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

            # Send a "HELLO" message to the server
            client_socket.send(b"HELLO\n"+b"\r")
            print("waiting for response after hello")
            response = client_socket.recv(1024).decode().strip()
            print(response)
            if response != "260 OK":
                
                return

            message_counter = 0

            # Iterate through messages
            for message in messages:
                # Send the DATA command to the server
                client_socket.send(b"DATA\n"+b"\r")
                client_socket.send(message+b"\r")
                print(b"DATA\n"+b"\r")
                print(message+b"\r")
                client_socket.send(b"."+b"\r") 
                print(b"."+b"\r") 
                print("waiting for response after DATA and message")
                response = client_socket.recv(1024).decode().strip()
                print(response)
                if response != "270 SIG":
                    
                    return "response not sig"

                # Compare the received signature with the stored signature
                print("waiting for signature")
                received_signature = client_socket.recv(1024).decode().strip()
                print(received_signature)
                print(signatures[message_counter])
                if received_signature == signatures[message_counter]:
                    client_socket.send(b"PASS\n"+b"\r")
                    print(b"PASS\n"+b"\r")
                else:
                    client_socket.send(b"FAIL\n"+b"\r")
                    print(b"Fail\n"+b"\r")
                print("response after pass or fail")
                response = client_socket.recv(1024).decode().strip()
                print(response)

                if response != "260 OK":
                    
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