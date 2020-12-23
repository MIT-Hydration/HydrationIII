# Demo an actuator and sensor end-to-end in the proposed architecture

This project is to demo the following strucutre end-to-end. 

https://docs.google.com/drawings/d/1QRMFYuSZM9tMgI91pgGa5nRd84Z5f_WUibL6J7ogIU0/edit?usp=sharing

Steps that I did (you may need slightly different steps based on OS/hardware):

1. Wrote Ubuntu Desktop 20.10 (RPI 4/400) 64-bit to a 128 Mb flash drive, using RPi Imager for Mac. 
See here: https://www.raspberrypi.org/forums/viewtopic.php?t=269749 , and https://ubuntu.com/download/raspberry-pi

2. Booted Ubuntu, Setup Username and Password

3. `sudo apt-get install net-tools`
4. `gsettings set org.gnome.Vino require-encryption false` was required for VNC connection to work for screensharing when collaborting using a mac
