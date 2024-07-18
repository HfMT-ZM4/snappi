################################################################################
#
# snappi-server-ui
#
################################################################################

SNAPPI_SERVER_UI_DEPENDENCIES = host-nodejs host-python
SNAPPI_SERVER_UI_LICENSE = GPL-3.0+
SNAPPI_SERVER_UI_LICENSE_FILES = LICENSE

SNAPPI_SERVER_UI_FRONTEND_INSTALL_DIR = $(TARGET_DIR)/usr/share/snappi-server-ui/frontend

define SNAPPI_SERVER_UI_BUILD_CMDS
    cd $(@D)/frontend/ && npm install
    cd $(@D)/frontend/ && npm run build
endef

define SNAPPI_SERVER_UI_INSTALL_TARGET_CMDS
	mkdir -p $(SNAPPI_SERVER_UI_FRONTEND_INSTALL_DIR)
	cp -dpfr $(@D)/frontend/dist/* $(SNAPPI_SERVER_UI_FRONTEND_INSTALL_DIR)
endef

$(eval $(generic-package))

