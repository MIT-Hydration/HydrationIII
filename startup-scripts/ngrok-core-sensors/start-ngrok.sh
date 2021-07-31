#!/bin/bash

ngrok tcp --remote-addr=3.tcp.ngrok.io:23386 1337
ngrok tcp --remote-addr=3.tcp.ngrok.io:23191 50051
