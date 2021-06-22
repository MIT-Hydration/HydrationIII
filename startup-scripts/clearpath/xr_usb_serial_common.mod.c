#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(.gnu.linkonce.this_module) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section(__versions) = {
	{ 0xe65d2cb5, "module_layout" },
	{ 0x5fa42981, "usb_deregister" },
	{ 0xc5850110, "printk" },
	{ 0x2ef85089, "put_tty_driver" },
	{ 0xd980ac88, "tty_unregister_driver" },
	{ 0x29020e0a, "usb_register_driver" },
	{ 0xef519a06, "tty_register_driver" },
	{ 0xe28bdea0, "tty_set_operations" },
	{ 0x67b27ec1, "tty_std_termios" },
	{ 0x28319534, "__tty_alloc_driver" },
	{ 0xfd5314a4, "tty_port_register_device" },
	{ 0xf4b3201a, "usb_get_intf" },
	{ 0xddad7e8a, "usb_driver_claim_interface" },
	{ 0x7054ea62, "_dev_info" },
	{ 0xeb233a45, "__kmalloc" },
	{ 0xd0e2fa28, "_dev_warn" },
	{ 0x1d01db1c, "device_create_file" },
	{ 0x290dea32, "usb_alloc_urb" },
	{ 0xffde232c, "usb_alloc_coherent" },
	{ 0x2c4fdfe1, "tty_port_init" },
	{ 0x977f511b, "__mutex_init" },
	{ 0xaff98eb8, "usb_ifnum_to_if" },
	{ 0x6cbbfc54, "__arch_copy_to_user" },
	{ 0x9484df36, "kmem_cache_alloc_trace" },
	{ 0x6e724670, "kmalloc_caches" },
	{ 0xc6cbbc89, "capable" },
	{ 0x12a4e128, "__arch_copy_from_user" },
	{ 0x409873e3, "tty_termios_baud_rate" },
	{ 0x90967791, "tty_port_open" },
	{ 0x17390c14, "usb_autopm_put_interface" },
	{ 0x36033f03, "usb_autopm_get_interface" },
	{ 0x9f49dcc4, "__stack_chk_fail" },
	{ 0x5af2dc10, "cpu_hwcaps" },
	{ 0xd697e69a, "trace_hardirqs_on" },
	{ 0xb788fb30, "gic_pmr_sync" },
	{ 0xec3d2e1b, "trace_hardirqs_off" },
	{ 0x296695f, "refcount_warn_saturate" },
	{ 0x2fe5c019, "tty_standard_install" },
	{ 0x7d3c13ca, "tty_flip_buffer_push" },
	{ 0x9f7635f1, "tty_insert_flip_string_fixed_flag" },
	{ 0x845a3a1c, "cpu_hwcap_keys" },
	{ 0x14b89635, "arm64_const_caps_ready" },
	{ 0xceb1566a, "usb_driver_release_interface" },
	{ 0xdec88b39, "usb_free_coherent" },
	{ 0x80b137f0, "usb_free_urb" },
	{ 0xb0697d39, "tty_unregister_device" },
	{ 0xff5d88c9, "tty_kref_put" },
	{ 0x920c2952, "tty_vhangup" },
	{ 0x71bb41cc, "tty_port_tty_get" },
	{ 0x67120fd2, "device_remove_file" },
	{ 0x37a0cba, "kfree" },
	{ 0x8874c72f, "usb_put_intf" },
	{ 0x409bcb62, "mutex_unlock" },
	{ 0x2ab7989d, "mutex_lock" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x2d3385d3, "system_wq" },
	{ 0x82fe8495, "tty_port_close" },
	{ 0xbfad288a, "usb_autopm_get_interface_async" },
	{ 0x7a678c0b, "tty_port_hangup" },
	{ 0x42d9bdf5, "tty_port_tty_wakeup" },
	{ 0xf9cb8214, "tty_port_tty_hangup" },
	{ 0x6ebe366f, "ktime_get_mono_fast_ns" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x9a93e2fe, "tty_port_put" },
	{ 0x301fa007, "_raw_spin_unlock" },
	{ 0xdbf17652, "_raw_spin_lock" },
	{ 0x3c12dfe, "cancel_work_sync" },
	{ 0x1cdc8acd, "usb_kill_urb" },
	{ 0xe1e6eced, "usb_autopm_put_interface_async" },
	{ 0xae723d7b, "_dev_err" },
	{ 0x50961c7f, "usb_submit_urb" },
	{ 0x4829a47e, "memcpy" },
	{ 0x70cae077, "__dynamic_dev_dbg" },
	{ 0x51784403, "usb_control_msg" },
	{ 0xc5664491, "_raw_spin_unlock_irq" },
	{ 0x47941711, "_raw_spin_lock_irq" },
	{ 0x3812050a, "_raw_spin_unlock_irqrestore" },
	{ 0x51760917, "_raw_spin_lock_irqsave" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("usb:v04E2p1410d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1411d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1412d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1414d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1420d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1421d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1422d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1424d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1400d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1401d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1402d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1403d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v2890p0213d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "B2542D718D56BDE08DB7088");
