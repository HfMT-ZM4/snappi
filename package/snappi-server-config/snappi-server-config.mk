################################################################################
#
# snappi-server-config
#
################################################################################

SNAPPI_SERVER_CONFIG_DEPENDENCIES = host-nodejs host-python
SNAPPI_SERVER_CONFIG_LICENSE = GPL-3.0+
SNAPPI_SERVER_CONFIG_LICENSE_FILES = LICENSE

SNAPPI_SERVER_CONFIG_FRONTEND_INSTALL_DIR = $(TARGET_DIR)/usr/share/snappi-server-config/frontend

define SNAPPI_SERVER_CONFIG_BUILD_CMDS
    cd $(@D)/frontend/ && npm install
    cd $(@D)/frontend/ && npm run build
endef

define SNAPPI_SERVER_CONFIG_INSTALL_TARGET_CMDS
	mkdir -p $(SNAPPI_SERVER_CONFIG_FRONTEND_INSTALL_DIR)
	cp -dpfr $(@D)/frontend/dist/* $(SNAPPI_SERVER_CONFIG_FRONTEND_INSTALL_DIR)

    $(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/backend/snappiserverconfig.py \
		$(TARGET_DIR)/usr/lib/python3.11/site-packages/snappiserverconfig.py
endef

define SNAPPISERVER_CONFIG_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/snappi-server-config-startup.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snappi-server-config-startup.service
	$(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/snappi-server-config.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snappi-server-config.service
endef

$(eval $(generic-package))

