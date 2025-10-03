import socket
import threading

class TCPClient:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.is_connected = False
        self.listener_thread = None
        self.on_message = None  # callback khi nhận data

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            print(f"[CLIENT] Connected to {self.host}:{self.port}")

            # bắt đầu luồng nhận dữ liệu
            self.listener_thread = threading.Thread(target=self.listen, daemon=True)
            self.listener_thread.start()
        except Exception as e:
            print(f"[CLIENT] Connection failed: {e}")

    def listen(self):
        try:
            while self.is_connected:
                data = self.socket.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8")
                print(f"[SERVER] {msg}")

                if self.on_message:
                    self.on_message(msg)
        except Exception as e:
            print(f"[CLIENT] Error while listening: {e}")
        finally:
            self.disconnect()

    def send(self, message: str):
        if self.is_connected:
            try:
                self.socket.sendall(message.encode("utf-8"))
                print(f"[CLIENT] Sent: {message}")
            except Exception as e:
                print(f"[CLIENT] Send failed: {e}")

    def disconnect(self):
        self.is_connected = False
        if self.socket:
            self.socket.close()
        print("[CLIENT] Disconnected")
