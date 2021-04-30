# Running

## Generate ProtoBuf Interface Files
`make grpc-gen`

## Client

### Main QT GUI Client
`make run-qt-client`

### Hello World Test
Test to make sure that the server is accesible and running without GUI complications
`make run-echo-client`

## Server (Raspberry Pi 4 B)

### Mission Control Server

`make run-mc-server`

### Connecting through ssh

`ssh hydration@96.237.232.240 -p1337`
`ssh hydration@192.168.1.196 -p1337`

# Installation

Steps that I did (you may need slightly different steps based on OS/hardware):

## Prepare OS
1. Wrote Ubuntu Desktop 20.10 (RPI 4/400) 64-bit to a 128 Mb flash drive, using RPi Imager for Mac. 
See here: https://www.raspberrypi.org/forums/viewtopic.php?t=269749 , and https://ubuntu.com/download/raspberry-pi

2. Booted Ubuntu, Setup Username and Password

3. `sudo apt-get install net-tools`
4. `gsettings set org.gnome.Vino require-encryption false` was required for VNC connection to work for screensharing when collaborting using a mac
5. Follow steps here to get `sshserver`: https://thishosting.rocks/how-to-enable-ssh-on-ubuntu/ for remote login

## Python C++ Bindings in RPi (Ubuntu)

1. `sudo apt-get install python3-dev`
2. `sudo apt install libpython3.9-dev`

## Running ClearPath Servo Test in RPi

See `Makefile` in `ClearPathTestCode` folder. 

1. `make test-run` for a completely C++ program to test the servo connection
2. `make hydration-servo` for compiling C++ to Python bindings
3. `make hydration-servo-test` to physically test the bindings

## For connecting to INA-219 current sensor from AdaFruit

1. `python3 -m pip install pi-ina219`

See example here: https://pypi.org/project/pi-ina219/

## For GPIO in RPi

We are using gpiozero: https://gpiozero.readthedocs.io/en/stable/


## Install GRPC in MAC
Following guide here: https://grpc.io/docs/languages/python/quickstart/

1. `sudo apt install python3-pip` to get pip
2. `pip install grpcio`
3. `pip install grpcio-tools`

In addition you may need to add the user to the `dialout` group and restart to access gpio without sudo:

`sudo adduser [username] dialout`

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

# Initial demo

This project is to demo the following strucutre end-to-end. 

https://docs.google.com/drawings/d/1QRMFYuSZM9tMgI91pgGa5nRd84Z5f_WUibL6J7ogIU0/edit?usp=sharing

See tag V0.3: https://github.com/MIT-Hydration/HydrationIII/tree/V0.3


# Process for GitHub + JIRA

1. Have a ticket to do the work
2. Review requirements with team lead of the subsystem
3. Set the ticket to In Progress
4. Create a branch in GitHub (e.g. use *git checkout -b _branch-name_* command). Use the Jira ticket number as branch name (e.g. *SOFT-2*)
5. Start working on the ticket, commit, and push as many times as you want 
6. When ready, create a *Pull Request* using the GitHub interface
7. Put the ticket in *Review and Commit* column in Jira
8. Review together with the team lead and accept commit (or back to in progress if team lead is not satisfied)
