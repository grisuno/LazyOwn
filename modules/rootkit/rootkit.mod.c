#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

#ifdef CONFIG_UNWINDER_ORC
#include <asm/orc_header.h>
ORC_HEADER;
#endif

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_MITIGATION_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x65487097, "__x86_indirect_thunk_rax" },
	{ 0x1e6d26a8, "strstr" },
	{ 0x6b10bee1, "_copy_to_user" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x92997ed8, "_printk" },
	{ 0x18e95b73, "sock_create" },
	{ 0x1b6314fd, "in_aton" },
	{ 0x82830afa, "sock_release" },
	{ 0x7c55a176, "filp_open" },
	{ 0x81865bb, "filp_close" },
	{ 0xa7eedcc4, "call_usermodehelper" },
	{ 0xe2d5255a, "strcmp" },
	{ 0xb0e602eb, "memmove" },
	{ 0xbb10e61d, "unregister_kprobe" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0x3f66a26e, "register_kprobe" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0x29fff2aa, "module_layout" },
};

MODULE_INFO(depends, "");

