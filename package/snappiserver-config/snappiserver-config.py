#!/usr/bin/python3

import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--channels', type=int, default=2,
                        help='Number of audio channels')

    parser.add_argument('-r', '--samplerate', type=int, default=44100,
                        help='Sample rate to use')

    parser.add_argument('-b', '--bits', type=int, default=16,
                        help='Bits to use')

    parser.add_argument('-s', '--stereo-pairs', type=int, default=0,
                        help='Add stereo pairs for all channels')

    parser.add_argument('-l', '--latency', type=int, default=1000,
                        help='End-to-end latency in ms for snapserver')

    parser.add_argument('-i', '--idle-threshold', type=int, default=2000,
                        help='Idle threshold for snapserver streams')

    parser.add_argument('-o', '--filename',
                        help='Filename of output file')

    parser.add_argument('output', choices=('alsa', 'snapserver'))

    args = parser.parse_args()

    if args.output == 'alsa':
        conf = generate_alsa_config(
            channels=args.channels,
            samplerate=args.samplerate,
            stereo_pairs=args.stereo_pairs,
        )

    elif args.output == 'snapserver':
        conf = generate_snapserver_config(
            channels=args.channels,
            samplerate=args.samplerate,
            bits=args.bits,
            stereo_pairs=args.stereo_pairs,
            idle_threshold=args.idle_threshold,
            latency=args.latency,
        )
    else:
        conf = ''

    if args.filename:
        with open(args.filename, 'w') as f:
            f.write(conf)
    else:
        print(conf)


def generate_alsa_config(channels, samplerate, stereo_pairs=False):
    conf = TMPL_ALSA_PCM_LOOP % {
        'channels': channels,
        'samplerate': samplerate,
    }

    for i in range(channels):
        conf += '\n'
        conf += TMPL_ALSA_PCM_MONO % {
            'name': f'mono{i + 1}',
            'channel': i,
        }

    if stereo_pairs:
        for i in range(channels // 2):
            conf += '\n'
            conf += TMPL_ALSA_PCM_STEREO % {
                'name': f'stereo{i + 1}',
                'left_channel': i * 2,
                'right_channel': i * 2 + 1,
            }

    return conf


def _snapserver_source_url(**kwargs):
    params = '&'.join(f'{key}={val}' for key, val in kwargs.items())
    return f'alsa:///?{params}'


def generate_snapserver_sources(channels, samplerate, bits, stereo_pairs, idle_threshold):
    source_lines = []
    for i in range(channels):
        source_url = _snapserver_source_url(
            name=f'Mono-{i + 1}',
            device=f'mono{i + 1}',
            sampleformat=f'{samplerate}:{bits}:1',
            idle_threshold=idle_threshold,
        )
        source_lines.append(f'source = {source_url}')

    if stereo_pairs:
        for i in range(channels // 2):
            source_url = _snapserver_source_url(
                name=f'Stereo-{i + 1}',
                device=f'stereo{i + 1}',
                sampleformat=f'{samplerate}:{bits}:2',
                idle_threshold=idle_threshold,
            )
            source_lines.append(f'source = {source_url}')


    return '\n'.join(source_lines)


def generate_snapserver_config(channels, samplerate, bits, stereo_pairs, idle_threshold, latency):
    sources = generate_snapserver_sources(channels, samplerate, bits, stereo_pairs, idle_threshold)
    return TMPL_SNAPSERVER_CONFIG % {
        'end_to_end_latency': latency,
        'sources': sources,
    }


TMPL_ALSA_PCM_LOOP = '''
pcm_slave.loop {
    pcm "hw:0,0,0"
    channels %(channels)d
    rate %(samplerate)d
}
'''

TMPL_ALSA_PCM_MONO = '''
pcm.%(name)s {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop
        bindings.0 %(channel)d
    }
}
'''

TMPL_ALSA_PCM_STEREO = '''
pcm.%(name)s {
    type plug
    slave.pcm {
        type dsnoop
        ipc_key 4242
        slave loop
        bindings.0 %(left_channel)d
        bindings.1 %(right_channel)d
    }
}
'''

TMPL_SNAPSERVER_CONFIG = '''
[server]
user = snappi
group = audio

[http]
doc_root = /usr/share/snapserver/snapweb

[stream]
codec = pcm
buffer = %(end_to_end_latency)d

%(sources)s
'''

main()
