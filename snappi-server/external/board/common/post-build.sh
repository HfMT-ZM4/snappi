#!/bin/sh

set -u
set -e

for arg in "$@"
do
	case "${arg}" in

		--mount-boot)
		if ! grep -qE '^/dev/mmcblk0p1' "${TARGET_DIR}/etc/fstab"; then
			mkdir -p "${TARGET_DIR}/boot"
			echo "Adding mount point for /boot to /etc/fstab."
			cat << __EOF__ >> "${TARGET_DIR}/etc/fstab"
/dev/mmcblk0p1	/boot		vfat	defaults	0	2
__EOF__
		fi
		;;

        --hostname-from-env)
        if [ -n "${SNAPPISERVER_HOSTNAME:-}" ]; then
            echo "Setting hostname to ${SNAPPISERVER_HOSTNAME}"
            echo "${SNAPPISERVER_HOSTNAME}" > ${TARGET_DIR}/etc/hostname
        fi
        ;;

	esac

done

