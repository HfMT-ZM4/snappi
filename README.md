# Snappi - Multichannel Audio via Wifi

Snappi is a project that uses RaspberryPis and open-source software to
implement a multichannel audio distribution setup via Wifi.

One RPi acts as the server that accepts multichannel audio from Windows, Mac or
Linux computers via [JackTrip](https://github.com/jacktrip/jacktrip). The audio
is then distributed as separate channels via
[SnapCast](https://github.com/badaix/snapcast) to an arbitrary number of snappi
clients.

## Build Snappi client image using buildroot

The following assumes you are on a Linux machine.

Create a base directory for all things "snappi":
```
mkdir ~/snappi/
cd ~/snappi/
```

Checkout this repository and the buildroot submodule:
```
git clone git@github.com:HfMT-ZM4/snappi.git
cd snappi
git submodule init
git submodule update
```

Create a build directory for your desired platform. We use the "rpi0w" variant
(Raspberry Zero W) in this example. Replace all "rpi0w" occurences below with "rpi4" to build
for Raspberry Pi 4B.
```
mkdir ~/snappi/build-rpi0w
```

Initialize build for rpi0w variant:
```
cd ~/snappi/snappi/buildroot
make BR2_EXTERNAL=$HOME/snappi/snappi/snappi-client/external O=$HOME/snappi/build-rpi0w snappi_client_rpi0w_defconfig
```

Start the build (this will take very long, depending on your machine and internet connection, possibly 15 - 30 minutes):
```
cd ~/snappi/build-rpi0w
make
```

After the successful build, the resulting sd-card image (`sdcard.img`) can be found in `~/snappi/build-rpi0w/images`.
