import socket 
 
# Configuration 
HOST = input("Enter target IP address: ")  # Target machine's IP address 
PORT = 1111 
 
def send_command(): 
    """Connect to the target and send commands.""" 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    try: 
        client_socket.connect((HOST, PORT)) 
        print(f"[+] Connected to {HOST}:{PORT}") 
 
        # Authenticate 
        password = input("Enter password: ") 
        client_socket.send(password.encode('utf-8')) 
 
        response = client_socket.recv(1024).decode('utf-8') 
        print(f"[*] Server response: {response}")  # Debug statement 
 
        if response == "Authenticated.": 
            print("[+] Authentication successful.") 
            while True: 
                # Send command to target 
                command = input("Enter command (or 'exit' to quit): ") 
                client_socket.send(command.encode('utf-8')) 
 
                if command.lower() == "exit": 
                    print("[!] Exiting...") 
                    break 
 
                # Receive output from target 
                output = client_socket.recv(1024).decode('utf-8') 
                print(f"[!] Output from target:\n{output}") 
        else: 
            print("[-] Authentication failed.") 
    except Exception as e: 
        print(f"[-] Error: {e}") 
    finally: 
        client_socket.close() 
        print("[*] Connection closed.") 
 
if __name__ == "main": 
    send_command()