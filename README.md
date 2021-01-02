# Demo an actuator and sensor end-to-end in the proposed architecture

This project is to demo the following strucutre end-to-end. 

https://docs.google.com/drawings/d/1QRMFYuSZM9tMgI91pgGa5nRd84Z5f_WUibL6J7ogIU0/edit?usp=sharing

# Running

## Client

### Main QT GUI Client
`make run-qt-client`

### Hello World Test
Test to make sure that the server is accesible and running without GUI complications
`make run-echo-client`

## Server

### Mission Control Server

`make run-mc-server`

# Installation

Steps that I did (you may need slightly different steps based on OS/hardware):

## Prepare OS
1. Wrote Ubuntu Desktop 20.10 (RPI 4/400) 64-bit to a 128 Mb flash drive, using RPi Imager for Mac. 
See here: https://www.raspberrypi.org/forums/viewtopic.php?t=269749 , and https://ubuntu.com/download/raspberry-pi

2. Booted Ubuntu, Setup Username and Password

3. `sudo apt-get install net-tools`
4. `gsettings set org.gnome.Vino require-encryption false` was required for VNC connection to work for screensharing when collaborting using a mac

## Install GRPC in MAC
Following guide here: https://grpc.io/docs/languages/python/quickstart/

1. `sudo apt install python3-pip` to get pip
2. `pip install grpcio`
3. `pip install grpcio-tools`

## Versions 
I get the following versions in my mac

`protoc --version`
`libprotoc 3.14.0`

`python3 -m grpc_tools.protoc --version`
`libprotoc 3.13.0`

## Firewall setting in the Raspberry Pi

I needed to have the following settings to allow port 50051 on the raspberry pi.

```
hydration@mit-hydration-prakash-rpi-00:~/github/demo-end-to-end-2021$ sudo ufw status verbose
[sudo] password for hydration: 
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere                  
50051                      ALLOW IN    Anywhere                  
50051/tcp                  ALLOW IN    Anywhere                  
22/tcp (v6)                ALLOW IN    Anywhere (v6)             
50051 (v6)                 ALLOW IN    Anywhere (v6)             
50051/tcp (v6)             ALLOW IN    Anywhere (v6)             

50051                      ALLOW OUT   Anywhere                  
50051/tcp                  ALLOW OUT   Anywhere                  
50051/udp                  ALLOW OUT   Anywhere                  
50051 (v6)                 ALLOW OUT   Anywhere (v6)             
50051/tcp (v6)             ALLOW OUT   Anywhere (v6)             
50051/udp (v6)             ALLOW OUT   Anywhere (v6)
```

### Commands

`sudo ufw allow in 50051/tcp`
`sudo ufw allow out 50051/tcp`


### Relevant documentation

`https://grpc.github.io/grpc/python/grpc.html`
`http://manpages.ubuntu.com/manpages/xenial/en/man8/ufw.8.html`

### Starting with Qt5

Starting from example code here: 
`https://stackoverflow.com/questions/9957195/updating-gui-elements-in-multithreaded-pyqt`

Needed to install the following modules and small code modifications:
`python3 -m pip install pyqt5`

### Starting a more "mission control" like UI

Installing LED component: `https://github.com/jazzycamel/QLed`
`python3 -m pip install QLed`
