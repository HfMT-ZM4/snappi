################################################################################
#
# snappi-server-config-ui
#
################################################################################

SNAPPI_SERVER_CONFIG_UI_DEPENDENCIES = host-nodejs
SNAPPI_SERVER_CONFIG_UI_LICENSE = GPL-3.0+
SNAPPI_SERVER_CONFIG_UI_SITE = $(SNAPPI_SERVER_CONFIG_UI_PKGDIR)/app
SNAPPI_SERVER_CONFIG_UI_SITE_METHOD = local

SNAPPI_SERVER_CONFIG_UI_FRONTEND_INSTALL_DIR = $(TARGET_DIR)/usr/share/snappi-server-config-ui

define SNAPPI_SERVER_CONFIG_UI_BUILD_CMDS
    cd $(@D) && npm ci --no-audit && npm run build
endef

define SNAPPI_SERVER_CONFIG_UI_INSTALL_TARGET_CMDS
	mkdir -p $(SNAPPI_SERVER_CONFIG_UI_FRONTEND_INSTALL_DIR)
	cp -dpfr $(@D)/dist/* $(SNAPPI_SERVER_CONFIG_UI_FRONTEND_INSTALL_DIR)
endef

$(eval $(generic-package))
