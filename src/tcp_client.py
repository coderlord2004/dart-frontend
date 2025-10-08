import socket
import threading
import json

class TCPClient:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.fp = None
        self.is_connected = False
        self.listener_thread = None
        self.on_message = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.fp = self.socket.makefile(mode="rw", encoding="utf-8")
            self.is_connected = True
            print(f"[CLIENT] Connected to {self.host}:{self.port}")

            self.listener_thread = threading.Thread(target=self.listen, daemon=True)
            self.listener_thread.start()

        except Exception as e:
            print(f"[CLIENT] Connection failed: {e}")

    def listen(self):
        """Liên tục nhận dữ liệu JSON từ server"""
        try:
            while self.is_connected:
                line = self.fp.readline()
                if not line:
                    break

                try:
                    data = json.loads(line)
                    print(f"[SERVER] {data}")
                    if self.on_message:
                        self.on_message(data)
                except json.JSONDecodeError:
                    print(f"[CLIENT] Invalid JSON: {line.strip()}")

        except Exception as e:
            print(f"[CLIENT] Error while listening: {e}")

        finally:
            self.disconnect()

    def send_object(self, obj):
        """Gửi object Python dưới dạng JSON"""
        if not self.is_connected:
            print("[CLIENT] Not connected")
            return

        try:
            json.dump(obj, self.fp)
            self.fp.write("\n")
            self.fp.flush()
            print(f"[CLIENT] Sent: {obj}")
        except Exception as e:
            print(f"[CLIENT] Send failed: {e}")

    def disconnect(self):
        """Đóng kết nối an toàn"""
        self.is_connected = False
        try:
            if self.fp and not self.fp.closed:
                self.fp.close()
            if self.socket:
                self.socket.close()
        finally:
            self.fp = self.socket = None
        print("[CLIENT] Disconnected")

