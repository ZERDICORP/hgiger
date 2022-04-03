import sys
from PyQt5.QtWidgets import QApplication
from core.manager import Manager
from client.builder import Builder

if __name__ == "__main__":
	app = QApplication(sys.argv)
	manager = Manager()
	manager.load()
	builder = Builder(manager=manager)
	builder.show()
	manager.setBuilder(builder)
	sys.exit(app.exec_())