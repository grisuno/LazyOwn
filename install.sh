#!/bin/bash
sudo apt update
sudo apt install ltrace
python3 -m venv env
source env/bin/activate
pip3 install pwn
pip3 install groq
pip3 install PyPDF2
pip3 install docx
pip3 install python-docx
pip3 install olefile
pip3 install exifread
pip3 install pycryptodome
pip3 install impacket
pip3 install pandas
pip3 install colorama
pip3 install tabulate
pip3 install pyarrow
git clone --depth=1 https://github.com/grisuno/LazyOwnInfiniteStorage.git ./modules_ext/ 
