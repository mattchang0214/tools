#! /usr/bin/env python3.6

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import socket
import time


def get_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # try connecting every 10 seconds for a minute
    for _ in range(6):
        try:
            # connect to Google's public DNS
            s.connect(("8.8.8.8",80))
        except OSError:
            print("Failed to connect...")
            time.sleep(10)
        else:
            print("Success!")
            break
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr    


from_addr = "[SMTP HOST USER]"
to_addr = "[CLIENT EMAIL ADDRESS]"

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = "Raspberry Pi's IP"
body = "IP Address: {}".format(get_ip_addr())
msg.attach(MIMEText(body, 'plain'))


server = smtplib.SMTP('[SMTP HOST]', 587)
server.starttls()
server.login(from_addr, "[SMTP HOST PASSWORD]")
text = msg.as_string()
server.sendmail(from_addr, to_addr, text)
server.quit()
