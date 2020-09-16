import socket
from motors import Motors

class Server():
    def __init__(self, host, port):
        self.host = host
        print(host)
        self.port = port
        self.motors = Motors()
        
    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        return self.connection()
        
    def connection(self):
        conn, addr = self.sock.accept()
        print(addr)
        while True:
            data = conn.recv(1024)
            if data.decode("utf-8") == "w":
                print('move forward')
                self.motors.forward()
            elif data.decode("utf-8") == "s":
                print("move back")
                self.motors.back()
            elif data.decode("utf-8") == "a":
                print("move left")
                self.motors.left()
            elif data.decode("utf-8") == "d":
                print("move right")
                self.motors.right()
            elif data.decode("utf-8") == "space":
                print("stopping")
                self.motors.stop()
            elif data.decode("utf-8") == "m":
                print("server OFF")
                break
            elif data.decode("utf-8") == "q":
                print("Program will close...")
                self.sock.close()
                return False
        
        self.sock.close()
        return True
        
    def restart(self):
        self.connection()


if __name__ == "__main__":
    serv = Server('', 9090)    # Вписать адрес хоста в локалке
    serv.start()
