#!/bin/bash

RELEASE_DIR=$1
BUILD_DIR=$2
VERSION=$3

COMPONENT=`grep BR2_EXTERNAL_NAMES ${BUILD_DIR}/.config | cut -d \" -f2 | tr '[:upper:]' '[:lower:]'`
VARIANT=`ls -1 ${BUILD_DIR}/images/*.dtb | xargs basename -s .dtb`

NAME=${COMPONENT}-${VERSION}-${VARIANT}
IMAGE_NAME=${NAME}.img

echo Copying ${BUILD_DIR}/images/sdcard.img to ${RELEASE_DIR}/${IMAGE_NAME}

mkdir -p ${RELEASE_DIR}
cp ${BUILD_DIR}/images/sdcard.img ${RELEASE_DIR}/${IMAGE_NAME}
zip -9 -o ${RELEASE_DIR}/${IMAGE_NAME}.zip ${RELEASE_DIR}/${IMAGE_NAME}



