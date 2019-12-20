import socket,os
import threading
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QTextEdit,QLabel,QDesktopWidget
from PyQt5.QtCore import pyqtSlot


def restart():
	print("restarting")
	os.execl(sys.executable, sys.executable, *sys.argv)


class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'Messenger'
		self.left = 10
		self.top = 10
		self.width = 400
		self.height = 400
		self.initUI()

	def centerOnScreen(self):
		resolution = QDesktopWidget().screenGeometry()
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),(resolution.height() / 2) - (self.frameSize().height() / 2))

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.centerOnScreen()
		# create label for ip and name
		self.ip_label = QLabel(self)
		self.ip_label.setText('Enter IP ')
		self.ip_label.move(20, 20)
		# Create textbox for ip
		self.ip_textbox = QLineEdit(self)
		self.ip_textbox.move(100, 20)
		self.ip_textbox.resize(280,30)

		# create label for message
		self.ip_label = QLabel(self)
		self.ip_label.setText('Enter Message')
		self.ip_label.move(20, 80)
		# Create textbox for message
		self.textbox = QLineEdit(self)
		self.textbox.move(100, 80)
		self.textbox.resize(280,30)

		# Create a button in the window
		self.button = QPushButton('Send', self)
		self.button.move(20,150)
		# connect button to send message
		self.button.clicked.connect(self.on_click)

		# Button to restart chatbot
		self.stop_button = QPushButton('Restart', self)
		self.stop_button.move(130,150)
		self.stop_button.clicked.connect(restart)

		# hidden button to update textbox from thread
		self.hidden_button = QPushButton('set value', self)
		self.hidden_button.hide()
		self.hidden_button.clicked.connect(self.set_text)

		# Create textbox for received message
		self.received_textbox = QTextEdit(self)
		self.received_textbox.move(20, 200)
		self.received_textbox.resize(280,150)
		self.received_textbox.setReadOnly(True)

		# Command to show chatbot
		self.show()

	def client(self,message):
		socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		port = 54321
		host_ip = self.ip_textbox.text()
		socket_client.connect((host_ip,port))

		byt=message.encode()
		socket_client.sendall(byt)
		self.received_textbox.append("You : {0}".format(message))

	def set_text(self):
		self.received_textbox.append("{0} : {1}".format(addr[0], message_from_client))

	def server(self):
		global message_from_client,addr
		socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		port = 54321
		socket_server.bind(('',port))
		print("listening.....")
		socket_server.listen(5)
		while True:
			conn,addr = socket_server.accept()
			print("got connection from ",conn)
			message_from_client = conn.recv(1024).decode('utf-8')
			print(message_from_client)
			self.hidden_button.click()
			conn.close()

	@pyqtSlot()
	def on_click(self):
		textboxValue = self.textbox.text()
		# QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
		self.textbox.setText("")
		self.client(textboxValue)

	def start_server(self):	
		server_app = threading.Thread(target=self.server)
		server_app.daemon = True
		server_app.start()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.start_server()
	sys.exit(app.exec_())
