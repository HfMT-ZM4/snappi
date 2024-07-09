#!/bin/bash

ALL_ARGS=("$@")
COMPONENT="$1"

# forward all SNAPPI* env vars to container
ENV_OPTS=""
for var in $(env | grep ^SNAPPI); do
    ENV_OPTS="${ENV_OPTS} -e ${var}"
done

podman run -it --rm \
    -v ./build/:/build \
    -v ./snappi:/snappi \
    -v ./dl:/buildroot/dl \
    -w /build/$COMPONENT \
    ${ENV_OPTS} \
    --userns="keep-id:uid=1001,gid=1001" \
    buildroot \
    ${ALL_ARGS[@]:1}
    
