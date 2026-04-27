Project Overview
This project implements a segmented campus network connected to a remote site via a four‑router serial chain (using HWIC‑2T modules). The network features:

VLAN segmentation and inter‑VLAN routing on a Layer‑3 switch.

Static routing between the main campus and the remote site.

An extended ACL that restricts a specific remote PC (PC_C_HR) to only the administrator’s PC and a dedicated web server.

A centralised email server (SMTP/POP3) with user accounts.

IoT automation using an SBC‑PT board and an analog temperature sensor: the SBC‑PT runs a Python script that sends email alerts when the temperature reaches 7 °C (turn ON air conditioners) or drops below 7 °C (turn OFF air conditioners).

All configurations were simulated and verified in Cisco Packet Tracer 8.x.

🏛️ Network Topology
Main Campus (VLANs 10,20,30,60,100)  ←→  Core Router (2911)  ←→  Remote Site (R1–R4 serial chain)
                                                        └─ R4 subinterfaces (10.10.10.1/24, 10.10.20.1/24, 10.10.30.1/24)
                                                              ├─ Switch A (VLANs 10,20,30)
                                                              └─ Switch C (VLANs 10,20,30)
Campus: Core Exchange1 (L3 switch), Access Switches, Admin PC, Mail Server (192.168.20.10), Web Server (192.168.10.200).

Remote Site: Four Cisco 2911 routers with serial DCE links, two Cisco 2960 switches, six remote PCs.

IoT: SBC‑PT (192.168.10.221) with analog temperature sensor connected to D0 pin.

✨ Features
Feature	Description
VLANs	Campus: 10 (IT), 20 (Servers), 30 (Animal Science), 60 (Academic), 100 (Transit). Remote: 10 (Sales), 20 (Engineering), 30 (HR).
Inter‑VLAN Routing	Layer‑3 switch (Core Exchange1) with SVIs.
WAN Connectivity	Serial links (200.200.200.0/24, 201.201.201.0/24, 202.202.202.0/24) and static routing.
Access Control	Extended ACL 101 outbound on R4 – permits PC_C_HR only to Admin PC and web server; denies all other campus destinations.
Email Server	SMTP/POP3 on 192.168.20.10, domain university.edu, users: admin, sbc, etc.
IoT Automation	SBC‑PT reads analog temperature (0‑1023) via analogRead(0), converts to Celsius, and sends email alerts using sendEmail(). Alert thresholds: ≥7 °C → “Turn ON ACs”, <7 °C → “Turn OFF ACs”.
🧰 Technologies Used
Cisco Packet Tracer 8.x – network simulation.

Python (built‑in on SBC‑PT) – temperature reading and email logic.

Cisco IOS – router/switch CLI configurations.

SMTP / POP3 – email services.

📡 IP Addressing (Key Devices)
Device	IP Address	VLAN / Subnet
Core Router G0/2	192.168.0.1/24	Transit VLAN 100
Core Exchange1 VLAN 100	192.168.0.2/24	Transit VLAN 100
Admin PC	192.168.10.10/24	VLAN 10 (IT)
Mail Server	192.168.20.10/24	VLAN 20 (Servers)
Web Server	192.168.10.200/24	VLAN 10 (IT)
SBC‑PT	192.168.10.221/24	VLAN 10 (IT)
R1 – R2 serial	200.200.200.1/30 – 200.200.200.2/30	
R2 – R3 serial	201.201.201.1/30 – 201.201.201.2/30	
R3 – R4 serial	202.202.202.1/30 – 202.202.202.2/30	
R4 – Core Router	203.203.203.1/30 – 203.203.203.2/30	
Remote PCs (Sales)	10.10.10.10/24, 10.10.10.20/24	Remote VLAN 10
Remote PCs (Eng)	10.10.20.10/24, 10.10.20.20/24	Remote VLAN 20
Remote PC (HR)	10.10.30.10/24, 10.10.30.20/24	Remote VLAN 30
⚙️ Configuration Highlights
Core Exchange1 (L3 Switch)
text
ip routing
vlan 10,20,30,60,100
interface vlan10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
...
interface vlan100
 ip address 192.168.0.2 255.255.255.0
 no shutdown
interface GigabitEthernet1/0/1
 switchport mode trunk
 switchport trunk native vlan 100
 switchport trunk allowed vlan 10,20,30,60,100
ip route 0.0.0.0 0.0.0.0 192.168.0.1
Core Router (Static Routes)
text
ip route 192.168.10.0 255.255.255.0 192.168.0.2
ip route 192.168.20.0 255.255.255.0 192.168.0.2
ip route 192.168.30.0 255.255.255.0 192.168.0.2
ip route 192.168.60.0 255.255.255.0 192.168.0.2
ip route 10.10.10.0 255.255.255.0 203.203.203.1
ip route 10.10.20.0 255.255.255.0 203.203.203.1
ip route 10.10.30.0 255.255.255.0 203.203.203.1
R4 (Extended ACL 101)
text
access-list 101 permit ip host 10.10.30.20 host 192.168.10.10
access-list 101 permit ip host 10.10.30.20 host 192.168.10.200
access-list 101 deny ip host 10.10.30.20 192.168.0.0 0.0.255.255
access-list 101 permit ip any any
interface GigabitEthernet0/0
 ip access-group 101 out
SBC‑PT Python Script (for temperature alerts)
python
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
🚀 How to Run in Cisco Packet Tracer
Download the University_Network.pkt file from this repository.

Open it in Cisco Packet Tracer 8.x (or later).

The network is pre‑configured – all devices have static IPs and routing.

To test connectivity:

Open Admin PC → Desktop → Command Prompt → ping 10.10.30.20 (remote PC).

From PC_C_HR → ping 192.168.10.10 (Admin PC) – success.

From PC_C_HR → ping 192.168.20.10 (mail server) – blocked by ACL.

To test IoT email alerts:

Go to Physical → Environment → set ambient temperature to 8 °C.

Watch the SBC‑PT console (Programming tab) – “Email sent” appears.

On Admin PC → Desktop → Email → Send/Receive – you will see the “Turn ON ACs” email.

Lower temperature to 6 °C – the “Turn OFF ACs” email arrives.

Note: The mail server must have SMTP/POP3 enabled and users admin and sbc created.

✅ Verification Results
Test	Expected	Result
Admin PC ↔ PC_A_Sales ping	Success	✅
PC_C_HR → Admin PC ping	Success	✅
PC_C_HR → Web Server (HTTP)	Success	✅
PC_C_HR → Mail Server ping	Fail (ACL)	✅ (Destination unreachable)
Temperature ≥7 °C	“Turn ON ACs” email	✅
Temperature <7 °C	“Turn OFF ACs” email	✅
