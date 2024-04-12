
Alsaequal is a real-time adjustable equalizer plugin for ALSA. It
can be adjusted using an ALSA compatible mixer, like alsamixergui
or alsamixer.

For example, add the following line to /etc/asound.conf

ctl.equal {
    type equal;
}

pcm.plugequal {
    type equal;
    slave.pcm "plughw:0,0";
}

pcm.equal{
    type plug;
    slave.pcm plugequal;
}

you can now adjust the 10 band equaliser using

    alsamixer -D equal

and then play using

    aplay -D equal some_audio.wav

By default alsaequal uses the 10 band equaliser (Eq10) from the alsa
ladspa plugin caps.  You can bypass alsaequal and directly use caps in
/etc/asound.conf. This can be useful if you want to fix the equaliser
settings.

Add the following lines to /etc/asound.conf to add a fixed 10 band
equaliser setup to attenuate frequencies below 500Hz

pcm.plugequal_fixed {
    type equal;
    slave.pcm "plughw:0,0";
}

pcm.equal_fixed {
    type ladspa
    slave.pcm plugequal_fixed;
    path "/usr/lib/ladspa";
    plugins [{
        label Eq10
        input {
            # bands (Hz)   31   63   125  250  500  1000 2000 4000 8000 16000
            controls     [ -48  -48  -48  -48  -48  0    0    0    0    0     ]
        }
    }]
}


Further reading:
    http://alsa.opensrc.org/Ladspa_(plugin)
    http://quitte.de/dsp/caps.html#Eq10
