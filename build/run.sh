#!/bin/bash

ALL_ARGS=("$@")
COMPONENT="$1"

podman run -it --rm \
    -v ./build/:/build \
    -v ./snappi:/snappi \
    -v ./dl:/buildroot/dl \
    -w /build/$COMPONENT \
    --userns="keep-id:uid=1001,gid=1001" \
    buildroot \
    ${ALL_ARGS[@]:1}
    
