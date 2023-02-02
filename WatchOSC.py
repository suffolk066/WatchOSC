import JsonConfigFileManager
import time
import sys
from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox
from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon
from pythonosc.udp_client import SimpleUDPClient

try:
    conf = JsonConfigFileManager.JsonConfigFileManager('./config.json')
except:
    with open('./config.json', 'w') as f:
        JsonConfigFileManager.json.dump(dict(IPADRESS='127.0.0.1',PORT=9000,
        AvatarParameterWatchMonth='SFS_WatchMonth',AvatarParameterWatchWday='SFS_WatchWday',
        AvatarParameterWatchDay='SFS_WatchDay',AvatarParameterWatchHours='SFS_WatchHours',
        AvatarParameterWatchMinutes='SFS_WatchMinutes',SENDCYCLE=3000), f, indent=4)
    conf = JsonConfigFileManager.JsonConfigFileManager('./config.json')

IP = conf.values.IPADRESS
PORT = conf.values.PORT
MONTH = conf.values.AvatarParameterWatchMonth
WDAY = conf.values.AvatarParameterWatchWday
DAY = conf.values.AvatarParameterWatchDay
HOURS = conf.values.AvatarParameterWatchHours
MINUTES = conf.values.AvatarParameterWatchMinutes
SENDCYCLE = conf.values.SENDCYCLE
PARAMETER = "/avatar/parameters/"

send_month = 0
send_wday = 0
send_day = 0
send_hours = 0
send_minutes = 0

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.setWindowTitle("Watch OSC")
        self.setFixedSize(450, 250)
        appIcon = QIcon("suffolk.ico")
        self.setWindowIcon(appIcon)

        self.ln_ip = QLineEdit(IP)
        self.ln_port = QLineEdit(str(PORT))
        self.ln_month = QLineEdit(str(MONTH))
        self.ln_wday = QLineEdit(str(WDAY))
        self.ln_day = QLineEdit(str(DAY))
        self.ln_hours = QLineEdit(str(HOURS))
        self.ln_minutes = QLineEdit(str(MINUTES))
        self.ln_cycle = QLineEdit(str(SENDCYCLE))

        self.vb_button = QHBoxLayout()
        self.btn_send = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.vb_button.addWidget(self.btn_send)
        self.vb_button.addWidget(self.btn_stop)

        self.form.addRow("IP", self.ln_ip)
        self.form.addRow("Send Port", self.ln_port)
        self.form.addRow("Parameter(Month) " + PARAMETER, self.ln_month)
        self.form.addRow("Parameter(Wday) " + PARAMETER, self.ln_wday)
        self.form.addRow("Parameter(Day) " + PARAMETER, self.ln_day)
        self.form.addRow("Parameter(Hours) " + PARAMETER, self.ln_hours)
        self.form.addRow("Parameter(Minutes) " + PARAMETER, self.ln_minutes)
        self.form.addRow("Cycle(per milliseconds)", self.ln_cycle)
        self.form.addRow(self.vb_button)

        self.btn_send.clicked.connect(self.start_message)
        self.btn_stop.clicked.connect(self.stop_message)

        self.isPushButtonClicked = False
        self.pushButtonTimer = QTimer(self)
        self.pushButtonTimer.setInterval(SENDCYCLE)
        self.pushButtonTimer.timeout.connect(self.send_message)

    def send_message(self):
        month = time.strftime("%m")
        wday = time.strftime("%w")
        day = time.strftime("%d")
        hours = time.strftime("%H")
        minutes = time.strftime("%M")

        send_month = int(month)
        send_wday = int(wday)
        send_day = int(day)
        send_hours = int(hours)
        send_minutes = int(minutes)

        CLIENT.send_message(PARAMETER + MONTH, send_month)
        CLIENT.send_message(PARAMETER + WDAY, send_wday)
        CLIENT.send_message(PARAMETER + DAY, send_day)
        CLIENT.send_message(PARAMETER + HOURS, send_hours)
        CLIENT.send_message(PARAMETER + MINUTES, send_minutes)

    def start_message(self):
        if not self.isPushButtonClicked:
            self.isPushButtonClicked = True
            self.btn_send.setEnabled(False)
            self.pushButtonTimer.start()
            self.setWindowTitle("Watch OSC Started...")

    def stop_message(self):
        self.isPushButtonClicked = False
        self.btn_send.setEnabled(True)
        self.pushButtonTimer.stop()
        self.setWindowTitle("Watch OSC")
    
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
        MONTH = self.ln_month.text()
        WDAY = self.ln_wday.text()
        DAY = self.ln_day.text()
        HOURS = self.ln_hours.text()
        MINUTES = self.ln_minutes.text()
        SENDCYCLE = int(self.ln_cycle.text())
        conf.update({'IPADRESS':IP,'PORT':PORT,'AvatarParameterWatchMonth':MONTH,'AvatarParameterWatchWday':WDAY,'AvatarParameterWatchDay':DAY,'AvatarParameterWatchHours':HOURS,'AvatarParameterWatchMinutes':MINUTES,'SENDCYCLE':SENDCYCLE})
        conf.export('./config.json')

app = QApplication([])
form = Form()
form.show()

try:
    CLIENT = SimpleUDPClient(IP, PORT)
except:
    form.alert()
    pass

sys.exit(app.exec_())