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

		--raise-volume)
		if grep -qE '^ENV{ppercent}:="75%"' "${TARGET_DIR}/usr/share/alsa/init/default"; then
			echo "Raising alsa default volume to 100%."
			sed -i -e 's/ENV{ppercent}:="75%"/ENV{ppercent}:="100%"/g' "${TARGET_DIR}/usr/share/alsa/init/default"
			sed -i -e 's/ENV{pvolume}:="-20dB"/ENV{pvolume}:="4dB"/g' "${TARGET_DIR}/usr/share/alsa/init/default"
		fi
		;;

        --hostname-from-env)
        if [ -n "${SNAPPICLIENT_HOSTNAME}" ]; then
            echo "Setting hostname to ${SNAPPICLIENT_HOSTNAME}"
            echo "${SNAPPICLIENT_HOSTNAME}" > ${TARGET_DIR}/etc/hostname
        fi
        ;;

        --wifi-from-env)
        if [ -n "${SNAPPICLIENT_WIFI}" ]; then
            # Remove wifi config from rootfs overlay
            rm ${TARGET_DIR}/var/lib/iwd/*.psk

            # input format is "<SSID1>=<PSK> <SSID2>=<PSK2> ..."
            OIFS="$IFS"
            IFS=" "
            for ssid_psk in ${SNAPPICLIENT_WIFI}; do
                IFS="="
                set -- ${ssid_psk}
                ssid="$1"
                psk="$2"
                fname="${TARGET_DIR}/var/lib/iwd/${ssid}.psk"
                echo "Writing passphrase for SSID '${ssid}' to ${fname}"
                echo "[Security]\nPassphrase=${psk}" > ${fname}
                IFS=" "
            done
            IFS="$OIFS"
        fi
        ;;
	esac

done

