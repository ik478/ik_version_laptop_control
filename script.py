from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from pynput.keyboard import Controller, Key  # Import for keyboard control

# Server configuration
host_name = "0.0.0.0"  # Listen on all available network interfaces
port_number = 9090     # Port number

# Initialize keyboard controller
keyboard = Controller()

class CommandHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/get_ip":
            system_ip = self.get_system_ip()  # Get the server's IP address
            self.respond(system_ip)
        elif self.path.startswith("/control?cmd="):
            command = self.path.split("=")[-1]
            if command == "right_arrow":
                keyboard.press(Key.right)  # Simulate pressing the right arrow key
                keyboard.release(Key.right)  # Release the key
                self.respond("Right arrow pressed.")
            elif command == "left_arrow":
                keyboard.press(Key.left)  # Simulate pressing the left arrow key
                keyboard.release(Key.left)  # Release the key
                self.respond("Left arrow pressed.")
            else:
                self.respond("Unknown command.")
        else:
            self.respond("Invalid endpoint.")

    def get_system_ip(self):
        """Return the server's IP address"""
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def respond(self, message):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

if __name__ == "__main__":
    server = HTTPServer((host_name, port_number), CommandHandler)
    print(f"Server started on {host_name}:{port_number}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
