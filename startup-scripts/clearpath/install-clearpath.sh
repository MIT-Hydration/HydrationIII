#!/bin/bash

date > /root/disk_space_report.txt
du -sh /home/ >> /root/disk_space_report.txt

rmmod cdc-acm
insmod /usr/local/bin/xr_usb_serial_common.ko
