################################################################################
#
# JackTrip
#
################################################################################

JACKTRIP_VERSION = 1.7.0
JACKTRIP_SOURCE = jacktrip-$(JACKTRIP_VERSION).tar.gz
JACKTRIP_SITE = $(call github,jacktrip,jacktrip,v$(JACKTRIP_VERSION))
JACKTRIP_LICENSE = GPL-3.0+
JACKTRIP_LICENSE_FILES = LICENSE.md
JACKTRIP_INSTALL_STAGING = NO

JACKTRIP_CONF_OPTS += -Dnogui=true -Djack=enabled -Drtaudio=disabled

$(eval $(meson-package))
