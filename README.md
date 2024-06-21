# Snappi - Multichannel Audio via Wifi

Snappi is a project that uses RaspberryPis and open-source software to
implement a multichannel audio distribution setup via Wifi.

One RPi acts as the server that accepts multichannel audio from Windows, Mac or
Linux computers via [JackTrip](https://github.com/jacktrip/jacktrip). The audio
is then distributed as separate channels via
[SnapCast](https://github.com/badaix/snapcast) to an arbitrary number of snappi
clients.

## Build Snappi client image using buildroot

The following assumes you are on a Linux machine and that you have
podman installed.

Create a base directory and some supporting directories
for all things "snappi":
```
mkdir ~/snappi/
cd ~/snappi/
mkdir dl
mkdir build
```

Checkout this repository:
```
git clone git@github.com:HfMT-ZM4/snappi.git
```

Build the buildroot podman image:
```
podman build -f snappi/build/Dockerfile -t buildroot
```

Initialize and run the build for the desired component.

Snappi-Server:
```
snappi/build/init.sh snappi-server snappi_server_rpi4_defconfig server
snappi/build/run.sh server make
```

Snappi-Client for RPi4
```
snappi/build/init.sh snappi-client snappi_client_rpi4_defconfig client-rpi4
snappi/build/run.sh client-rpi4 make
```

Snappi-Client for RPi 0W
```
snappi/build/init.sh snappi-client snappi_client_rpi0w_defconfig client-rpi0w
snappi/build/run.sh client-rpi0w make
```

The build will take quite some time, depending on your machine and internet
connection 15 - 30 minutes, maybe more.

After the successful build, the resulting sd-card image (`sdcard.img`) can be found in `~/snappi/build/$NAME/images`.



The default build sets the hostname of the client to "snappi-client" and
attempts to connect to the Wifi with SSID "Snappi" using passphrase "1234578".
To set a different hostname or configure different Wifi networks, you can run
`make` again with the following environment variables set:

- SNAPPICLIENT_HOSTNAME (sets the hostname in the generated image)
- SNAPPICLIENT_WIFI (space separated pairs of "SSID=PASSPHRASE")

Example, to configure the hostname to "snappi1" and make two Wifi networks
("MyWifi1" with passphrase "secure1", "MyWifi2" with passphrase "secure2"):

```
SNAPPICLIENT_HOSTNAME=snappi1 SNAPPICLIENT_WIFI="MyWifi1=secure1 MyWifi2=secure2" make
`````
