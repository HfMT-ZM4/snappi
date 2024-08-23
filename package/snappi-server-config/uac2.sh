#!/bin/sh

GADGET_NAME="virtual-audio"
CONFIGFS_ROOT=/sys/kernel/config/usb_gadget
GADGET_DIR="${CONFIGFS_ROOT}/${GADGET_NAME}"

# tear down old gadget if it exists
if [ -d "${GADGET_DIR}" ]; then
    echo '' > $GADGET_DIR/UDC
    for dir in $GADGET_DIR/configs/*/strings/*; do
            [ -d $dir ] && rmdir $dir
    done
    for func in $GADGET_DIR/configs/*.*/*.*; do
            [ -e $func ] && rm $func
    done
    for conf in $GADGET_DIR/configs/*; do
            [ -d $conf ] && rmdir $conf
    done
    for func in $GADGET_DIR/functions/*.*; do
            [ -d $func ] && rmdir $func
    done
    for str in $GADGET_DIR/strings/*; do
            [ -d $str ] && rmdir $str
    done
    rmdir $GADGET_DIR
fi

[ -r /etc/default/uac2 ] && . /etc/default/uac2

if [ "${UAC2_ENABLE}" != "yes" ]; then
    exit 0
fi

BCD_DEVICE=0x0100 # v.1.0.0
BCD_USB=0x0200 # USB2
ID_VENDOR=0x1d6b # Linux Foundation
ID_PRODUCT=0x0101 # 0x0104 for Multi Functional Gadget / 0x0101 for Audio Gadget

STRG_LANGUAGE=0x409 # no need to adapt - 0x409 is a standard value (for US English)
STRG_MANUFACTURER="LigetiZentrum" # adapt as you like
STRG_PRODUCT="${UAC2_NAME}"
STRG_SERIALNUMBER="${UAC2_SERIAL}" # adapt as you like

CONFIGURATION_CNF_1="Basic"

AUDIO_CHANNEL_MASK_CAPTURE=${UAC2_CHANNEL_MASK}
AUDIO_CHANNEL_MASK_PLAYBACK=0 # disabed
AUDIO_SAMPLE_RATES_CAPTURE=${UAC2_SAMPLE_RATE}
AUDIO_SAMPLE_RATES_PLAYBACK=${UAC2_SAMPLE_RATE}
AUDIO_SAMPLE_SIZE_CAPTURE=${UAC2_SAMPLE_SIZE} # 1 for S8LE / 2 for S16LE / 3 for S24LE / 4 for S32LE
AUDIO_SAMPLE_SIZE_PLAYBACK=${UAC2_SAMPLE_SIZE}

modprobe libcomposite

mkdir -p $GADGET_DIR
cd $GADGET_DIR

# basics
echo $BCD_DEVICE > bcdDevice
echo $BCD_USB > bcdUSB
echo $ID_VENDOR > idVendor
echo $ID_PRODUCT > idProduct

# strings
mkdir -p strings/$STRG_LANGUAGE
echo $STRG_SERIALNUMBER > strings/$STRG_LANGUAGE/serialnumber
echo $STRG_MANUFACTURER > strings/$STRG_LANGUAGE/manufacturer
echo $STRG_PRODUCT > strings/$STRG_LANGUAGE/product

# configuration(s)
mkdir configs/c.1 # index mandatory for every configuration
mkdir -p configs/c.1/strings/$STRG_LANGUAGE
echo $CONFIGURATION_CNF_1 > configs/c.1/strings/$STRG_LANGUAGE/configuration

# functions
mkdir -p functions/uac2.usb0
echo $AUDIO_CHANNEL_MASK_CAPTURE > functions/uac2.usb0/c_chmask
echo $AUDIO_SAMPLE_RATES_CAPTURE > functions/uac2.usb0/c_srate
echo $AUDIO_SAMPLE_SIZE_CAPTURE > functions/uac2.usb0/c_ssize
echo $AUDIO_CHANNEL_MASK_PLAYBACK > functions/uac2.usb0/p_chmask
echo $AUDIO_SAMPLE_RATES_PLAYBACK > functions/uac2.usb0/p_srate
echo $AUDIO_SAMPLE_SIZE_PLAYBACK > functions/uac2.usb0/p_ssize

echo "${STRG_PRODUCT}" > functions/uac2.usb0/function_name

# associate functions to configurations
ln -s functions/uac2.usb0 configs/c.1/

# enable the gadget
ls /sys/class/udc > UDC
