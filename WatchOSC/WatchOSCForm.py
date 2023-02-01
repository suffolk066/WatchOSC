import JsonConfigFileManager
from PySide2.QtWidgets import *

conf = JsonConfigFileManager.JsonConfigFileManager('./config.json')

IP = conf.values.IPADRESS
PORT = conf.values.PORT
HOURS = conf.values.AvatarParameterWatchHours
MINUTES = conf.values.AvatarParameterWatchMinutes
SECONDS = conf.values.AvatarParameterWatchSeconds
SENDCYCLE = conf.values.SENDCYCLE

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()


        self.form = QFormLayout()
        self.setLayout(self.form)
        self.setWindowTitle("Watch OSC")
        self.setFixedSize(400, 200)

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
        self.form.addRow("Cycle(per second)", self.ln_cycle)
        self.form.addRow(self.vb_button)

app = QApplication([])
form = Form()
form.show()
app.exec_()