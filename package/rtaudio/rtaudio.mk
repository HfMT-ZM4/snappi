################################################################################
#
# RtAudio
#
################################################################################

RTAUDIO_VERSION = 6.0.1
RTAUDIO_SOURCE = rtaudio-$(RTAUDIO_VERSION).tar.gz
RTAUDIO_SITE = http://www.music.mcgill.ca/~gary/rtaudio/release
RTAUDIO_LICENSE = MIT
RTAUDIO_LICENSE_FILES = LICENSE
RTAUDIO_INSTALL_STAGING = YES

$(eval $(meson-package))

