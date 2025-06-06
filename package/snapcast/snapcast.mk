################################################################################
#
# snapcast
#
################################################################################

#SNAPCAST_VERSION = v0.28.0
#SNAPCAST_SITE = $(call github,badaix,snapcast,$(SNAPCAST_VERSION))
SNAPCAST_VERSION = snappi-pw-0.1.0
SNAPCAST_SITE = $(call github,mawe42,snapcast,$(SNAPCAST_VERSION))
SNAPCAST_SOURCE = snapcast-$(SNAPCAST_VERSION).tar.gz
SNAPCAST_DEPENDENCIES = libogg alsa-lib avahi boost 
SNAPCAST_LICENSE = GPL-3.0+
SNAPCAST_LICENSE_FILES = LICENSE

define SNAPCLIENT_INSTALL_CONFIG
endef

define SNAPSERVER_INSTALL_CONFIG
	$(INSTALL) -m 0755 -D $(@D)/server/etc/snapserver.conf $(TARGET_DIR)/etc/
endef

ifeq ($(BR2_PACKAGE_SNAPCAST_CLIENT),y)
SNAPCAST_POST_INSTALL_TARGET_HOOKS += SNAPCLIENT_INSTALL_CONFIG

define SNAPCLIENT_INSTALL_INIT_SYSV
	$(INSTALL) -m 0755 -D $(SNAPCAST_PKGDIR)/S99snapclient $(TARGET_DIR)/etc/init.d/S99snapclient
endef

define SNAPCLIENT_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(SNAPCAST_PKGDIR)/snapclient.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snapclient.service
endef

else # !BR2_PACKAGE_SNAPCAST_CLIENT
	SNAPCAST_CONF_OPTS += -DBUILD_CLIENT=OFF
endif

ifeq ($(BR2_PACKAGE_SNAPCAST_SERVER),y)
SNAPCAST_POST_INSTALL_TARGET_HOOKS += SNAPSERVER_INSTALL_CONFIG

define SNAPSERVER_INSTALL_INIT_SYSV
	$(INSTALL) -m 0755 -D $(SNAPCAST_PKGDIR)/S99snapserver $(TARGET_DIR)/etc/init.d/S99snapserver
endef

define SNAPSERVER_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(SNAPCAST_PKGDIR)/snapserver.service \
		$(TARGET_DIR)/usr/lib/systemd/system/snapserver.service
endef

else # !BR2_PACKAGE_SNAPCAST_SERVER
	SNAPCAST_CONF_OPTS += -DBUILD_SERVER=OFF
endif

define SNAPCAST_INSTALL_INIT_SYSV
	$(SNAPCLIENT_INSTALL_INIT_SYSV)
	$(SNAPSERVER_INSTALL_INIT_SYSV)
endef

define SNAPCAST_INSTALL_INIT_SYSTEMD
	$(SNAPCLIENT_INSTALL_INIT_SYSTEMD)
	$(SNAPSERVER_INSTALL_INIT_SYSTEMD)
endef

$(eval $(cmake-package))
