################################################################################
#
# snappi cloud init - Support for system config using RPi Imager
#
################################################################################

define SNAPPI_CLOUD_INIT_INSTALL_INIT_SYSV
	$(INSTALL) -m 0755 -D $(SNAPPI_CLOUD_INIT_PKGDIR)/S03snappi-cloud-init $(TARGET_DIR)/etc/init.d/S03snappi-cloud-init
endef

define SNAPPI_CLOUD_INIT_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(SNAPPI_CLOUD_INIT_PKGDIR)/snappi-cloud-init \
		$(TARGET_DIR)/usr/bin/snappi-cloud-init
endef

define SNAPPI_CLOUD_INIT_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(SNAPPI_CLOUD_INIT_PKGDIR)/snappi-cloud-init.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snappi-cloud-init.service
endef

$(eval $(generic-package))
