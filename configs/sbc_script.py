from time import *
from gpio import *
from email import *

MAIL_SERVER = "192.168.20.10"
SENDER_EMAIL = "sbc@university.edu"
SENDER_USER = "sbc"
SENDER_PASS = "password"
RECIPIENT = "admin@university.edu"

TEMP_ON = 7  
TEMP_OFF = 7 

alert_on_sent = False
alert_off_sent = False

def get_temperature():
    raw = analogRead(0)  
    celsius = (raw / 1023.0) * 100.0 - 50.0
    return celsius

def send_alert(to, subject, body):
    sendEmail(to, subject, body, SENDER_EMAIL)
    print("Email sent to:", to)

while True:
    temp = get_temperature()
    print("Temperature: {:.1f}°C".format(temp))
    if temp >= TEMP_ON and not alert_on_sent:
        send_alert(RECIPIENT,
                   "Temperature Alert: Turn ON ACs",
                   "Temperature reached {:.1f}°C. Turn ON ACs.".format(temp))
        alert_on_sent = True
        alert_off_sent = False
    elif temp < TEMP_OFF and not alert_off_sent:
        send_alert(RECIPIENT,
                   "Temperature Alert: Turn OFF ACs",
                   "Temperature dropped to {:.1f}°C. Turn OFF ACs.".format(temp))
        alert_off_sent = True
        alert_on_sent = False
    sleep(30)
