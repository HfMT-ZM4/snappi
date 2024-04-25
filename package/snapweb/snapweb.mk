################################################################################
#
# snapweb
#
################################################################################

SNAPWEB_VERSION = v0.7.0
SNAPWEB_SOURCE = snapweb.zip
SNAPWEB_SITE = https://github.com/badaix/snapweb/releases/download/$(SNAPWEB_VERSION)
SNAPWEB_LICENSE = GPL-3.0+
SNAPWEB_LICENSE_FILES = LICENSE

SNAPWEB_INSTALL_DIR = $(TARGET_DIR)/usr/share/snapserver/snapweb

define SNAPWEB_EXTRACT_CMDS
	$(UNZIP) -d $(@D) $(SNAPWEB_DL_DIR)/$(SNAPWEB_SOURCE)
endef

define SNAPWEB_INSTALL_TARGET_CMDS
	mkdir -p $(SNAPWEB_INSTALL_DIR)
	cp -dpfr $(@D)/* $(SNAPWEB_INSTALL_DIR)
endef

$(eval $(generic-package))
