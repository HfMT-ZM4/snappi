################################################################################
#
# snappi-users
#
################################################################################

define SNAPPI_USERS_USERS
    snappi 2001 audio  2001 * - - - Snappi things
endef


$(eval $(generic-package))
