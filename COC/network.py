"""
Network Manager for multiplayer functionality
Handles socket communication between host and client
"""

import socket
import json
import threading
from config import DEFAULT_HOST, DEFAULT_PORT

class NetworkManager:
    def __init__(self):
        self.socket = None
        self.is_host = False
        self.connected = False
        self.client_socket = None
        self.message_queue = []
        self.lock = threading.Lock()
        
    def start_host(self):
        """Start as host (server)"""
        self.is_host = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((DEFAULT_HOST, DEFAULT_PORT))
        self.socket.listen(1)
        self.socket.settimeout(0.1)  # Non-blocking with timeout
        print(f"Server started on {DEFAULT_HOST}:{DEFAULT_PORT}")
        
    def check_connection(self):
        """Check for incoming connections (host only)"""
        if self.is_host and not self.connected:
            try:
                client, addr = self.socket.accept()
                self.client_socket = client
                self.client_socket.settimeout(0.1)
                self.connected = True
                print(f"Client connected from {addr}")
                
                # Start listening thread
                thread = threading.Thread(target=self._listen_thread, daemon=True)
                thread.start()
                return True
            except socket.timeout:
                return False
        return False
        
    def join_game(self, host_ip=DEFAULT_HOST):
        """Join as client"""
        self.is_host = False
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host_ip, DEFAULT_PORT))
            self.socket.settimeout(0.1)
            self.connected = True
            print(f"Connected to {host_ip}:{DEFAULT_PORT}")
            
            # Start listening thread
            thread = threading.Thread(target=self._listen_thread, daemon=True)
            thread.start()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
            
    def _listen_thread(self):
        """Background thread to listen for incoming messages"""
        active_socket = self.client_socket if self.is_host else self.socket
        buffer = ""
        
        while self.connected:
            try:
                data = active_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                buffer += data
                
                # Process complete JSON messages (separated by newlines)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        try:
                            msg = json.loads(line)
                            with self.lock:
                                self.message_queue.append(msg)
                        except json.JSONDecodeError:
                            print(f"Invalid JSON received: {line}")
                            
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Connection error: {e}")
                break
                
        self.connected = False
        
    def send_data(self, data):
        """Send data to the other player"""
        if not self.connected:
            return False
            
        try:
            msg = json.dumps(data) + '\n'
            active_socket = self.client_socket if self.is_host else self.socket
            active_socket.sendall(msg.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
            return False
            
    def receive_data(self):
        """Get next message from queue"""
        with self.lock:
            if self.message_queue:
                return self.message_queue.pop(0)
        return None
        
    def close(self):
        """Close all connections"""
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass