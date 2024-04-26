################################################################################
#
# snappiserver-config
#
################################################################################

define SNAPPISERVER_CONFIG_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(SNAPPISERVER_CONFIG_PKGDIR)/snappiserver-config.py \
		$(TARGET_DIR)/usr/bin/snappiserver-config.py
endef

define SNAPPISERVER_CONFIG_INSTALL_INIT_SYSV
	$(INSTALL) -D -m 0755 $(SNAPPISERVER_CONFIG_PKGDIR)/S80snappiserver-config \
		$(TARGET_DIR)/etc/init.d/S80snappiserver-config
endef

$(eval $(generic-package))

