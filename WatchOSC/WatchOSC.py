import time
import JsonConfigFileManager
from pythonosc.udp_client import SimpleUDPClient

conf = JsonConfigFileManager('./config.json')

IP = conf.values.IPADRESS
PORT = conf.values.PORT
HOURS = conf.values.AvatarParameterWatchHours
MINUTES = conf.values.AvatarParameterWatchMinutes
SECONDS = conf.values.AvatarParameterWatchSeconds
SENDCYCLE = conf.values.SENDCYCLE
CLIENT = SimpleUDPClient(IP, PORT)

send_hours = ["", True]
send_minutes = ["", True]
send_seconds = ["", True]

def send_message():
    hours = time.strftime("%I")
    minutes = time.strftime("%M")
    seconds = time.strftime("%S")
    print(hours)
    print(minutes)
    print(seconds)

    send_hours[0] = f"{hours}"
    send_minutes[0] = f"{minutes}"
    send_seconds[0] = f"{seconds}"

    CLIENT.send_message(HOURS, send_hours)
    CLIENT.send_message(MINUTES, send_minutes)
    CLIENT.send_message(SECONDS, send_seconds)
    time.sleep(SENDCYCLE)
    send_message()

if __name__ == "__main__":
    send_message()