# TODO
- Test power consumption with RPi 0W
- Add buildroot for snappi-server
- Test power consumption of server on RPi 4B
- Make number and setup of channels configurable during build

# Client Setup with stock RPiOS
```
apt-get install snapclient
systemctl enable --now snapclient
```
## Enable equalizer and other LADSPA plugins

```
apt-get install libasound2-plugin-equal caps ladspa-sdk
```

/etc/asound.conf
```
cm.highlow {
    type ladspa
    slave.pcm "plughw:0,0"
    path "/usr/lib/ladspa"
    plugins [
        {
            id 1041 # lpf
            policy none
            input.bindings.0 "Input";
            output.bindings.0 "Output";
            input {
                controls [ 440.0 ]
            }
        }
        {
            id 1042 # hpf
            policy none
            input.bindings.1 "Input";
            output.bindings.1 "Output";
            input {
                controls [ 440.0 ]
            }
        }
    ]
}

pcm.plughighlow {
    type plug;
    slave.pcm "highlow";
}

pcm.equal {
    type equal;
    slave.pcm "plughighlow";
}

ctl.equal {
    type equal;
}

pcm.!default {
    type plug;
    slave {
        pcm "equal";
        rate 48000;
    }
}
```

Change EQ with:
```
sudo -u _snapclient alsamixer -D equal
```

## WIFI Setup
/etc/NetwokManager/system-connections/preconfigured.nmconnection
```
[connection]
id=preconfigured
uuid=3333f04b-317e-443f-a8ba-806cc5e55e51
type=wifi
[wifi]
mode=infrastructure
ssid=Snappi
hidden=false
[ipv4]
method=auto
[ipv6]
addr-gen-mode=default
method=auto
[proxy]
[wifi-security]
key-mgmt=wpa-psk
psk=12345678
auth-alg=open
```

# Server Setup

## Disable unused services
```
systemctl disable --now ModemManager
systemctl disable --now triggerhappy.socket
systemctl disable --now triggerhappy

apt-get purge bluez -y
apt-get autoremove -y
```

## Add hotspot to RaspberryPi OS
```
nmcli con add con-name hotspot ifname wlan0 type wifi ssid "Snappi"
nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
nmcli con modify hotspot wifi-sec.psk "12345678"
nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify hotspot ipv4.addresses 10.10.10.1/24
nmcli con up hotspot
```

## Load ALSA loopback on startup
```
echo "snd-aloop" >> /etc/modules
```

## Setup ALSA Routing 8-Chan Loopback to separate channels
/etc/asound.conf
```
pcm_slave.loop8 {
    pcm "hw:0,0,0"
    channels 8
    rate 48000
}

pcm.out1 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 0
    }
}

pcm.out2 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 1
    }
}

pcm.out3 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 2
    }
}

pcm.out4 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 3
    }
}

pcm.out5 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 4
    }
}

pcm.out6 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 5
    }
}

pcm.out7 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 6
    }
}

pcm.out8 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 7
    }
}

pcm.out12 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 0
        bindings.1 1
    }
}

pcm.out34 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 2
        bindings.1 3
    }
}

pcm.out56 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 4
        bindings.1 5
    }
}

pcm.out78 {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop8
        bindings.0 6
        bindings.1 7
    }
}
```

## Setup jack2 and jacktrip on snappi server
```
apt-get install jackd2 jacktrip
useradd -M -r audio -G audio
```

/etc/audio.env
```
JACK_NO_AUDIO_RESERVATION=1
JACK_OPTS=-P75 -R -dalsa -dhw:0,0 -r48000 -p1024 -n3
JACKTRIP_OPTS=-s --receivechannels 8 --sendchannels 1 --udprt
SNAPSERVER_OPTS=-c /etc/snapserver.conf --server.datadir=/var/lib/snapserver
```

/etc/systemd/system/jackd.service
```
[Unit]
Description=Jack audio server 
After=sound.target

[Install]
WantedBy=multi-user.target

[Service]
User=audio
Type=simple
LimitRTPRIO=infinity
LimitMEMLOCK=infinity
LimitRTTIME=infinity
EnvironmentFile=/etc/audio.env
ExecStart=/usr/bin/jackd $JACK_OPTS
Restart=always
RestartSec=2s
```

/etc/systemd/system/jacktrip.service
```
[Unit]
Description=jacktrip
Requires=jackd.service
After=network.target jackd.service

[Install]
WantedBy=multi-user.target

[Service]
User=audio
Type=simple
LimitRTPRIO=infinity
LimitMEMLOCK=infinity
LimitRTTIME=infinity
EnvironmentFile=/etc/audio.env
ExecStartPre=/usr/bin/jack_wait -w -t 5
ExecStart=/usr/bin/jacktrip $JACKTRIP_OPTS
Restart=always
RestartSec=2s
```

## Setup snapserver
```
apt-get install snapserver
```

/etc/systemd/system/snapserver.service
```
[Unit]
Description=Snapcast server
Wants=network-online.target avahi-daemon.service
After=network-online.target time-sync.target avahi-daemon.service

[Service]
EnvironmentFile=/etc/audio.env
ExecStart=/usr/bin/snapserver --logging.sink=system $SNAPSERVER_OPTS
User=audio
Group=audio
Restart=always
RestartSec=2s

[Install]
WantedBy=multi-user.target
```

/etc/snapserver.conf
```
[stream]
source = alsa:///?name=Channel1&device=out1&sampleformat=48000:16:1
source = alsa:///?name=Channel2&device=out2&sampleformat=48000:16:1
source = alsa:///?name=Channel3&device=out3&sampleformat=48000:16:1
source = alsa:///?name=Channel4&device=out4&sampleformat=48000:16:1
source = alsa:///?name=Channel5&device=out5&sampleformat=48000:16:1
source = alsa:///?name=Channel6&device=out6&sampleformat=48000:16:1
source = alsa:///?name=Channel7&device=out7&sampleformat=48000:16:1
source = alsa:///?name=Channel8&device=out8&sampleformat=48000:16:1
source = alsa:///?name=Channel12&device=out12&sampleformat=48000:16:2
source = alsa:///?name=Channel34&device=out34&sampleformat=48000:16:2
source = alsa:///?name=Channel56&device=out56&sampleformat=48000:16:2
source = alsa:///?name=Channel78&device=out78&sampleformat=48000:16:2
```

# Minimal SnapPi-Client Image

Build with BuildRoot 2024.02.01

Notes on Wifi:
https://www.stefanocottafavi.com/buildroot_rpi_wifi/


# Power Consumption

## Snappi Client RPi 4B
Governor: powersave, 600MHz

### Without HifiBerry MiniAMP
Idle: 470mA @ 5V / 2.35W
Playing: 480mA @ 5V / 2.4W
Max per hour: 0.48Ah @ 5V / 2.4Wh
Add 10% safety margin: 0.53Ah @ 5V / 2.64Wh

Target: 5 hours runtime
Energy: 13.2Wh
2640mAh @ 5V
3568mAh @ 3.7V

Target: 8 hours runtime
Energy: 21.12Wh
4224mAh @ 5V
5708mAh @ 3.7V

Target: 10 hours runtime
Energy: 26.4Wh
5300mAh @ 5V
7135mAh @ 3.7V

## Snappi Client Zero W

### Bare (Without HifiBerry MiniAMP)
Idle: 100mA @ 5V / 0.5W
Playing: 110mA @ 5V / 0.55W
Max per hour: 0.11Ah @ 5V / 0.55Wh
Add 10% safety margin: 0.12Ah @ 5V / 0.6Wh

Target: 5 hours runtime
Energy: 3Wh
600mAh @ 5V
810mAh @ 3.7V

Target: 8 hours runtime
Energy: 4.8Wh
960mAh @ 5V
1300mAh @ 3.7V

Target: 10 hours runtime
Energy: 6Wh
1200mAh @ 5V
4324mAh @ 3.7V
