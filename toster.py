import socket
import keyboard

class Client():
    manual_mode = True
    
    def __init__(self, host, port):
        self.host = host
        print(host)
        self.port = port
        
    def move(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        while True:
            #if keyboard.is_pressed("q"):
            #    sock.send(b"q")
            #    break
            if self.manual_mode:
                if keyboard.is_pressed("w"):
                    sock.send(b"w")
                elif keyboard.is_pressed("a"):
                    sock.send(b"a")
                elif keyboard.is_pressed("s"):
                    sock.send(b"s")
                elif keyboard.is_pressed("d"):
                    sock.send(b"d")
                elif keyboard.is_pressed("space"):
                    sock.send(b"space")
                elif keyboard.is_pressed("m"):
                    sock.send(b"m")    
                    break 
                elif keyboard.is_pressed("q"):
                    sock.send(b"q")    
                    break 
        sock.close()
        
if __name__ == "__main__":
    connection = Client('192.168.7.26', 9090)   # Вписать адрес хоста в локалке
    connection.move()