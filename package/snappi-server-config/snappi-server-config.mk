################################################################################
#
# snappi-server-config
#
################################################################################

SNAPPI_SERVER_CONFIG_LICENSE = GPL-3.0+
SNAPPI_SERVER_CONFIG_SITE = $(SNAPPI_SERVER_CONFIG_PKGDIR)/app
SNAPPI_SERVER_CONFIG_SITE_METHOD = local
SNAPPI_SERVER_CONFIG_SETUP_TYPE = setuptools
SNAPPI_SERVER_CONFIG_DEPENDS = python-websockets python-pyyaml python-fastapi python-uvicorn

define SNAPPI_SERVER_CONFIG_POST_INSTALL_TARGET_CMDS
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

$(eval $(python-package))
