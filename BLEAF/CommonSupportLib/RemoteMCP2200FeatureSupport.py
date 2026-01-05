#!/usr/bin/env python
import threading
import time
from websocket_server import WebsocketServer  # pip install websocket-server
import websockets.sync.client as ws_client

class WebSocketManager:
    def __init__(self, host="127.0.0.1", port=8111):
        self.host = host
        self.port = port
        self.server = None
        self.server_thread = None
        self.websocket = None  # Client websocket instance
        self.client_thread = None
        self._connected = threading.Event()
        print("WebSocketManager init")

    def new_client(self, client, peer):
        print(f"New client connected: {peer}")

    def client_left(self, client, peer):
        print(f"Client disconnected: {peer}")

    def message_received(self, client, peer, message):
        print(f"Server Received from {peer}: {message}")
        #if message.lower() == "stop":
        #    print("Stop received; shutting down.")
        #    self.shutdown()
        #    return
        print(f"[Server Echo]: {message}")
        self.server.send_message(client, message)

    def start_server(self):
        #self.server = WebsocketServer(self.port, host=self.host)
        self.server = WebsocketServer(port=self.port)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        print(f"Threaded Server running on ws://{self.host}:{self.port}")
        self.server.run_forever(threaded=True)

    def client_loop(self):
        """Persistent client loop: stays connected until stop."""
        uri = f"ws://{self.host}:{self.port}"
        retries = 0
        while retries < 3:  # Reconnect logic
            try:
                self.websocket = ws_client.connect(uri)
                print("Client connected and persistent.")
                self._connected.set()
                while self.websocket.keepalive():
                    time.sleep(1)  # Low CPU; check open state
                print("Client disconnected.")
            except Exception as e:
                retries += 1
                print(f"Client reconnect attempt {retries}: {e}")
                time.sleep(2)
        print("Client failed after retries.")

    def send_to_server(self, message):
        """Send data; 'stop' closes connection."""
        if self.websocket and self.websocket.keepalive:
            try:
                self.websocket.send(message)
                print(f"Sent: {message}")
                response = self.websocket.recv()
                print(f"[Client Recv]: {response}")
                if response.lower() == "stop":
                    print(f"Stop response: {response}")
                    #self.websocket.close()
                    self.shutdown()
                return response
            except Exception as e:
                print(f"Send error: {e}")
        print("Not connected.")
        return None

    def run(self):
        """Modified: Non-blocking daemon threads for persistent connection."""
        print("Starting persistent WebSocket connection...")
        # Server daemon thread
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)
        # Client daemon thread
        self.client_thread = threading.Thread(target=self.client_loop, daemon=True)
        self.client_thread.start()
        self._connected.wait(timeout=10)  # Wait for connection
        print("Connection established and kept alive.")

    def shutdown(self):
        """Graceful shutdown."""
        print("WebSocketManager shutting down...")
        if self.websocket.keepalive:
            try:
                self.websocket.close()
            except:
                pass
        if self.server:
            self.server.shutdown()
        print("complete.")

if __name__ == "__main__":
    manager = WebSocketManager("127.0.0.1", 8101)
    manager.run()  # Establishes and keeps connection

    # Keep main thread alive for external access
    try:
        for i in range(5):
            time.sleep(3)
            manager.send_to_server("Keepalive.")
        time.sleep(3)
        manager.shutdown()
    except KeyboardInterrupt:
        manager.shutdown()
