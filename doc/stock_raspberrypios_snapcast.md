To install the Snapcast client on a stock Raspberry PI OS, execute the following commands (as root):
```shell
apt-get update
apt-get install snapclient
```

This will install the SnapCast client and enable the service to start at boot.
It will try to autodetect a SnapCast server in the current network and connect
to it.

To edit the settings of the SnapCast client, you can modify the file /etc/default/snapclient:
```shell
vi /etc/default/snapclient
```

Here you can add additional command-line switches to the SNAPCLIENT_OPTS
variable. For example, to connect to a specific SnapCast server on IP
192.168.178.199 and use the ALSA device blafoo to output sound:

```shell
SNAPCLIENT_OPTS="-h 192.168.178.199 -s balfoo"
```
