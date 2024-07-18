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

Snappi-Client for RPi Zero 2W
```
snappi/build/init.sh snappi-client snappi_client_rpizero2w_defconfig client-rpizero2w
snappi/build/run.sh client-rpizero2w make
```


The build will take quite some time, depending on your machine and internet
connection 15 - 30 minutes, maybe more.

After the successful build, the resulting sd-card image (`sdcard.img`) can be found in `~/snappi/build/$NAME/images`.

## Writing the images to an sd-card

The images have support for the [RaspberryPi Imager](https://www.raspberrypi.com/software/) OS customization. So you can 
write the images using that tool and also adjust the hostname and WiFi settings.

If you don't apply Wifi customizations, then the default build uses a WiFi hotspot with SSID "Snappi"
and passphrase "12345678" on the server and configures the Wifi accordingly on the clients.
