# How to install in a Ubuntu RPi system

We followed the guide here: https://linuxconfig.org/how-to-run-script-on-startup-on-ubuntu-20-04-focal-fossa-server-desktop 

The `ngrok` executable and `start-ngrok.sh` are copied in `/usr/local/bin` folder

Copy the `ngrokcoresensors.service` file to `/etc/systemd/system` folder. Follow steps 3 and 4 in the above link reproduced below:

```
$ sudo chmod 744 /usr/local/bin/start-ngrok.sh
$ sudo chmod 664 /etc/systemd/system/ngrokcoresensors.service

$ sudo systemctl daemon-reload
$ sudo systemctl enable ngrokcoresensors.service
```

## Test
After reboot the following should work from a remote computer

```
ssh hydration@3.tcp.ngrok.io -p23386
```

`3.tcp.ngrok.io:23191` should be available for grpc if grpc server is started at port 50051.