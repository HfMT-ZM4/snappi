################################################################################
#
# snapweb
#
################################################################################

#SNAPWEB_VERSION = v0.7.0
#SNAPWEB_SOURCE = snapweb.zip
#SNAPWEB_SITE = https://github.com/badaix/snapweb/releases/download/$(SNAPWEB_VERSION)
SNAPWEB_VERSION = show-system-info
SNAPWEB_SITE = $(call github,mawe42,snapweb,$(SNAPWEB_VERSION))
SNAPWEB_SOURCE = snapweb-$(SNAPWEB_VERSION).tar.gz
SNAPWEB_DEPENDENCIES = host-nodejs
SNAPWEB_LICENSE = GPL-3.0+
SNAPWEB_LICENSE_FILES = LICENSE

SNAPWEB_INSTALL_DIR = $(TARGET_DIR)/usr/share/snapserver/snapweb

SNAPWEB_BUILD_ENV = npm_config_nodedir=/build/server/host/include/node/

define SNAPWEB_BUILD_CMDS
    cd $(@D) && npm install
    cd $(@D) && npm run build
endef

define SNAPWEB_INSTALL_TARGET_CMDS
	mkdir -p $(SNAPWEB_INSTALL_DIR)
	cp -dpfr $(@D)/dist/* $(SNAPWEB_INSTALL_DIR)
endef

$(eval $(generic-package))
