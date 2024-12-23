#!/bin/bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get -yq install wine32
wget -q https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe -O /tmp/python-3.12.8-amd64.exe
wine /tmp/python-3.12.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
wine C:/Python312/Scripts/pip.exe install -r requirements.txt
rm /tmp/python-3.12.8-amd64.exe