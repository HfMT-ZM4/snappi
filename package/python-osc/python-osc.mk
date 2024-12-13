################################################################################
#
# python-osc
#
################################################################################

PYTHON_OSC_VERSION = 1.9.0
PYTHON_OSC_SOURCE = python_osc-$(PYTHON_OSC_VERSION).tar.gz
PYTHON_OSC_SITE = https://files.pythonhosted.org/packages/2f/c9/d529263be224e4e093f4f5903025c0014a3e8a35505d15d82660378b31ef
PYTHON_OSC_SETUP_TYPE = setuptools
PYTHON_OSC_LICENSE = MIT
PYTHON_OSC_LICENSE_FILES = LICENSE

$(eval $(python-package))
