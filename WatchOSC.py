import JsonConfigFileManager
import time
import sys
from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox
from PySide2.QtCore import QTimer
from pythonosc.udp_client import SimpleUDPClient

conf = JsonConfigFileManager.JsonConfigFileManager('./config.json')

IP = conf.values.IPADRESS
PORT = conf.values.PORT
HOURS = conf.values.AvatarParameterWatchHours
MINUTES = conf.values.AvatarParameterWatchMinutes
SECONDS = conf.values.AvatarParameterWatchSeconds
SENDCYCLE = conf.values.SENDCYCLE

set_thread = ""
send_hours = ["", True]
send_minutes = ["", True]
send_seconds = ["", True]

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.setWindowTitle("Watch OSC")
        self.setFixedSize(450, 200)

        self.ln_ip = QLineEdit(IP)
        self.ln_port = QLineEdit(str(PORT))
        self.ln_hours = QLineEdit(str(HOURS))
        self.ln_minutes = QLineEdit(str(MINUTES))
        self.ln_seconds = QLineEdit(str(SECONDS))
        self.ln_cycle = QLineEdit(str(SENDCYCLE))

        self.vb_button = QHBoxLayout()
        self.btn_send = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.vb_button.addWidget(self.btn_send)
        self.vb_button.addWidget(self.btn_stop)

        self.form.addRow("IP", self.ln_ip)
        self.form.addRow("Send Port", self.ln_port)
        self.form.addRow("Parameter(Hours)", self.ln_hours)
        self.form.addRow("Parameter(Minutes)", self.ln_minutes)
        self.form.addRow("Parameter(Seconds)", self.ln_seconds)
        self.form.addRow("Cycle(per milliseconds)", self.ln_cycle)
        self.form.addRow(self.vb_button)

        self.btn_send.clicked.connect(self.start_message)
        self.btn_stop.clicked.connect(self.stop_message)

        self.isPushButtonClicked = False
        self.pushButtonTimer = QTimer(self)
        self.pushButtonTimer.setInterval(SENDCYCLE)
        self.pushButtonTimer.timeout.connect(self.send_message)

    def send_message(self):
        hours = time.strftime("%I")
        minutes = time.strftime("%M")
        seconds = time.strftime("%S")

        send_hours[0] = f"{hours}"
        send_minutes[0] = f"{minutes}"
        send_seconds[0] = f"{seconds}"

        CLIENT.send_message(HOURS, send_hours)
        CLIENT.send_message(MINUTES, send_minutes)
        CLIENT.send_message(SECONDS, send_seconds)

    def start_message(self):
        if not self.isPushButtonClicked:
            self.isPushButtonClicked = True
            self.btn_send.setEnabled(False)
            self.pushButtonTimer.start()

    def stop_message(self):
        self.isPushButtonClicked = False
        self.btn_send.setEnabled(True)
        self.pushButtonTimer.stop()
    
    def alert(self):
        button = QMessageBox.question(self, "Error", "Check IPAddress or click 'yes' to set 127.0.0.1", QMessageBox.Yes | QMessageBox.Ignore)
        if button == QMessageBox.Yes:
                self.ln_ip.setText('127.0.0.1')
        else:
            pass

    def closeEvent(self, event):
        global IP, PORT, HOURS, MINUTES, SECONDS, SENDCYCLE
        IP = self.ln_ip.text()
        PORT = int(self.ln_port.text())
        HOURS = self.ln_hours.text()
        MINUTES = self.ln_minutes.text()
        SECONDS = self.ln_seconds.text()
        SENDCYCLE = int(self.ln_cycle.text())
        conf.update({'IPADRESS':IP,'PORT':PORT,'AvatarParameterWatchHours':HOURS,'AvatarParameterWatchMinutes':MINUTES,'AvatarParameterWatchSeconds':SECONDS,'SENDCYCLE':SENDCYCLE})
        conf.export('./config.json')
CLIENT = ""

app = QApplication([])
form = Form()
form.show()

try:
    CLIENT = SimpleUDPClient(IP, PORT)
except:
    form.alert()
    pass

sys.exit(app.exec_())