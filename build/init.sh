#!/bin/bash

COMPONENT="$1"
DEFCONFIG="$2"
OUTPUTDIR="$3"

podman run -it --rm \
    -v ./build/:/build \
    -v ./snappi:/snappi \
    -v ./dl:/buildroot/dl \
    -w /buildroot \
    --userns="keep-id:uid=1001,gid=1001" \
    buildroot \
    make BR2_EXTERNAL=/snappi/$COMPONENT O=/build/$OUTPUTDIR $DEFCONFIG

    

