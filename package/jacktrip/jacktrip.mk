################################################################################
#
# JackTrip
#
################################################################################

JACKTRIP_VERSION = 2.2.5
JACKTRIP_SOURCE = jacktrip-$(JACKTRIP_VERSION).tar.gz
JACKTRIP_SITE = $(call github,jacktrip,jacktrip,v$(JACKTRIP_VERSION))
JACKTRIP_LICENSE = GPL-3.0+
JACKTRIP_LICENSE_FILES = LICENSE.md
JACKTRIP_INSTALL_STAGING = NO

#JACKTRIP_DEPENDENCIES = host-pkgconf
JACKTRIP_CONF_OPTS += -Dnogui=true -Djack=enabled -Dnovs=true
JACKTRIP_CONF_OPTS += -Dnoupdater=true -Dnofeedback=true -Dwair=false

$(eval $(meson-package))
