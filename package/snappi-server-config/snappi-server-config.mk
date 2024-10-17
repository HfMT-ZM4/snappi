################################################################################
#
# snappi-server-config
#
################################################################################

SNAPPI_SERVER_CONFIG_DEPENDENCIES = host-nodejs
SNAPPI_SERVER_CONFIG_LICENSE = GPL-3.0+
SNAPPI_SERVER_CONFIG_LICENSE_FILES = LICENSE

SNAPPI_SERVER_CONFIG_FRONTEND_INSTALL_DIR = $(TARGET_DIR)/usr/share/snappi-server-config/frontend

define SNAPPI_SERVER_CONFIG_BUILD_CMDS
	cp -dpfr $(SNAPPI_SERVER_CONFIG_PKGDIR)/frontend $(@D)
    cd $(@D)/frontend/ && npm install
    cd $(@D)/frontend/ && npm run build
endef

define SNAPPI_SERVER_CONFIG_INSTALL_TARGET_CMDS
	mkdir -p $(SNAPPI_SERVER_CONFIG_FRONTEND_INSTALL_DIR)
	cp -dpfr $(@D)/frontend/dist/* $(SNAPPI_SERVER_CONFIG_FRONTEND_INSTALL_DIR)

    $(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/backend/snappiserverconfig.py \
		$(TARGET_DIR)/usr/lib/python$(PYTHON3_VERSION_MAJOR)/site-packages/snappiserverconfig.py

    $(INSTALL) -D -m 0755 $(SNAPPI_SERVER_CONFIG_PKGDIR)/uac2.sh \
		$(TARGET_DIR)/usr/bin/uac2.sh
endef

define SNAPPI_SERVER_CONFIG_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/snappi-server-config-startup.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snappi-server-config-startup.service
	$(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/snappi-server-config.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snappi-server-config.service
	$(INSTALL) -D -m 0644 $(SNAPPI_SERVER_CONFIG_PKGDIR)/uac2.service \
		$(TARGET_DIR)/usr/lib/systemd/system/uac2.service
endef

$(eval $(generic-package))
