################################################################################
#
# LADSPA SDK
#
################################################################################

LADSPA_VERSION = 1.15
LADSPA_SOURCE = ladspa_sdk_$(LADSPA_VERSION).tgz
LADSPA_SITE = http://www.ladspa.org/download
LADSPA_INSTALL_STAGING = YES
LADSPA_INSTALL_TARGET = YES
LADSPA_AUTORECONF = NO
LADSPA_DEPENDENCIES = 

define LADSPA_BUILD_CMDS
    $(MAKE) CC=$(TARGET_CC) LD=$(TARGET_LD) \
		INSTALL_PLUGINS_DIR=$(@D)/usr/lib/ladspa/ \
		INSTALL_BINARY_DIR=$(@D)/usr/local/bin/ \
		INSTALL_INCLUDE_DIR=$(@D)/usr/include/ \
		-C $(@D)/src ../bin/listplugins ../bin/analyseplugin ../plugins/filter.so ../plugins/amp.so
endef

define LADSPA_INSTALL_TARGET_CMDS
    mkdir -p $(TARGET_DIR)/usr/lib/ladspa
    $(INSTALL) -D -m 0755 $(@D)/plugins/*.so $(TARGET_DIR)/usr/lib/ladspa
    $(INSTALL) -D -m 0755 $(@D)/bin/analyseplugin $(TARGET_DIR)/usr/local/bin
    $(INSTALL) -D -m 0755 $(@D)/bin/listplugins $(TARGET_DIR)/usr/local/bin
endef

define LADSPA_INSTALL_STAGING_CMDS
    $(INSTALL) -D -m 0644 $(@D)/src/ladspa.h $(STAGING_DIR)/usr/include
endef

$(eval $(generic-package))
