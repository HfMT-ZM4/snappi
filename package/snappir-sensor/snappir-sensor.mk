################################################################################
#
# snappi PIR sensor client
#
################################################################################

define SNAPPIR_SENSOR_INSTALL_INIT_SYSV
	$(INSTALL) -m 0755 -D $(SNAPPIR_SENSOR_PKGDIR)/S99snappir-sensor $(TARGET_DIR)/etc/init.d/S99snappir-sensor
endef

define SNAPPIR_SENSOR_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(SNAPPIR_SENSOR_PKGDIR)/snappir-sensor \
		$(TARGET_DIR)/usr/bin/snappir-sensor
endef

$(eval $(generic-package))

