# How to install in a Ubuntu RPi system

We followed the guide here: https://linuxconfig.org/how-to-run-script-on-startup-on-ubuntu-20-04-focal-fossa-server-desktop 

Put the contents of this folder (at least the xr_...ko file, and install_drvr file) in the /usr/local/bin folder.

Also copy the clearpathd.service file to /etc/systemd/system folder. Follow steps 3 and 4 in the above link reproduced below:

```
$ sudo chmod 744 /usr/local/bin/install-clearpath.sh
$ sudo chmod 664 /etc/systemd/system/clearpathd.service

$ sudo systemctl daemon-reload
$ sudo systemctl enable clearpathd.service
```

After rebooting, check that /dev/ttyACM0 is missing, and /dev/ttyX* is present.
