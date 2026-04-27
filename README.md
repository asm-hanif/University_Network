Smart Campus Network with Remote Site & IoT Alerts

Overview
This project simulates a segmented campus network connected to a remote site via a 4‑router serial chain** (HWIC‑2T). It includes VLANs, static routing, an extended ACL, email server, and IoT temperature alerts using an SBC‑PT.

Key features:
- Campus VLANs: 10 (IT), 20 (Servers), 30 (Animal Science), 60 (Academic), 100 (Transit)
- Remote VLANs: 10 (Sales), 20 (Engineering), 30 (HR)
- Static routes between Core Router and R4
- Extended ACL on R4: `PC_C_HR` (10.10.30.20) → only Admin PC (192.168.10.10) + Web Server (192.168.10.200)
- Mail server: 192.168.20.10 (SMTP/POP3, domain `university.edu`, users `admin`, `sbc`)
- IoT: SBC‑PT reads analog temperature (D0 pin) and sends email alerts at 7°C (ON ACs) / <7°C (OFF ACs)

How to Use
1. Open `University_Network.pkt` in Cisco Packet Tracer 8.x.
2. All devices are pre‑configured.
3. Test connectivity:
   - `Admin PC` → ping `10.10.30.20` (success)
   - `PC_C_HR` → ping `192.168.10.10` (success)
   - `PC_C_HR` → ping `192.168.20.10` (blocked by ACL)
4. Test IoT email alerts:
   - `Physical` → `Environment` → set ambient temperature to 8 °C.
   - Watch `SBC‑PT` console → “Email sent”.
   - `Admin PC` → `Desktop` → `Email` → `Send/Receive` → see “Turn ON ACs” email.
   - Lower temperature to 6 °C → “Turn OFF ACs” email.

Requirements
- Cisco Packet Tracer 8.x or later
- No external hardware needed

Author
- Abu Sayed Muhammed Hanif
LinkedIn: https://www.linkedin.com/in/abu-sayed-muhammed-hanif-15b689374/details/skills/

Course: CSE 3568 – Computer Networks Laboratory  
Institution: Premier University, Chittagong  
