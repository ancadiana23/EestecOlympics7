import socket
import threading
import time

HOST = "localhost"
PORT = 10000
SERVER_STATE_UPDATE_FREQUENCY_SECONDS = 0.01

MOUSE_UP = 1
MOUSE_DOWN = 2

class ClientState:
	def __init__(self, x, y, s):
		self.lock = threading.Lock()
		self.setState(x, y, s)
		self.lastReceivedPacketTime = 0.0

	def getState(self):
		with self.lock:
			return self.x, self.y, self.s

	def setState(self, x, y, s):
	    if x < 0 or x > 640 or y < 0 or y > 480:
	      print("ERROR: trying to set out of bounds values for x, y: {}, {}".format(x, y))
	      return
	    with self.lock:
	      self.x, self.y, self.s = x, y, s

	def sendTeamName(self, conn, name):
		toSend = name.encode() + b'\x00'
		print(toSend)
		conn.sendall(toSend)

	def send(self, conn):
		with self.lock:
			result = bytes([self.x >> 8, self.x & 0xff, self.y >> 8, self.y & 0xff, self.s])
		print(result)
		conn.sendall(result)

class Client(threading.Thread):
	def __init__(self):
		global HOST, PORT
		super(Client, self).__init__()
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conn.connect((HOST, PORT))
		self.state = ClientState(0, 0, MOUSE_UP)

	def run(self):
		global SERVER_STATE_UPDATE_FREQUENCY_SECONDS
		self.state.sendTeamName(self.conn, "ADA")
		while True:
			time.sleep(SERVER_STATE_UPDATE_FREQUENCY_SECONDS)
			self.state.send(self.conn)

	def update_state(self, event):
		self.state.setState(int(x),
							int(y),
							MOUSE_DOWN if event.state else MOUSE_UP)

def main():
	client = Client()
	client.start()


if __name__ == "__main__":
  main()
