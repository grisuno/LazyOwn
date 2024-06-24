#!/bin/bash
sudo apt update
sudo apt install ltrace
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
git clone --depth=1 https://github.com/grisuno/LazyOwnInfiniteStorage.git ./modules_ext/lazyown_infinitestorage
chmod +x /modules_ext/lazyown_infinitestorage/install.sh
/modules_ext/lazyown_infinitestorage/
./install.sh
