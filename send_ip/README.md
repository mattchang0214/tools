# **Sending your Raspberry Pi's IP address to your email on startup**
Every once in a while the IP address of my Raspberry Pi changes. Trying to SSH or VNC into the Pi when this happens 
is quite inconvenient, as I'm used to running the Pi headless, and I would need to go through the hassle of finding a 
screen and keyboard/mouse just to get the IP address. It's not very easy (if it's even allowed) to set up static IP on 
university network, so I thought the best way to avoid all the trouble is to have the Pi send me its IP on startup.

## "Installation"
Copy `send_ip.py` and `send_ip.sh` to the `/home/pi/` directory. You need to have a SMTP host/server for the Python code to work. 
It's easy to set one up using Gmail, but I used [Mailgun](https://simpleisbetterthancomplex.com/tutorial/2017/05/27/how-to-configure-mailgun-to-send-emails-in-a-django-app.html) 
just because I didn't want to mess with any Gmail settings.

Next, open a service file in the systemd directory using the following line
```
sudo geany /etc/systemd/system/send_ip.service
```
Add in the following and save
```
[Unit]
# By default 'simple' is used
# Type=simple|forking|oneshot|dbus|notify|idle
Description=Send IP Service
## make sure we only start the service after network is up
After=network-online.target

[Service]
## here we can set custom environment variables
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/send_ip.sh

[Install]
WantedBy=multi-user.target
```

Enable and test the service
```
sudo systemctl enable send_ip.service
sudo systemctl start send_ip.service
```
The Python script should have executed. Check the status of the service to make sure everything's ok
```
sudo systemctl status send_ip.service
```
Reboot the Pi and your custom service should run
```
sudo reboot
```

## Sources
* [Sending emails using `smtplib`](https://myhydropi.com/send-email-with-a-raspberry-pi-and-python)
* [Getting IP address of the Pi](https://circuitdigest.com/microcontroller-projects/display-ip-address-of-raspberry-pi)
* [Running a script on startup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)
* [Running a script as a systemd service](https://unix.stackexchange.com/a/401080)
