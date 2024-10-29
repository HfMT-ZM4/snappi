DEFAULT_ROUTES = [
    {
        'target': 'Mono-1:::input_0',
        'source': 'JackTrip:::receive_1',
    },
    {
        'target': 'Mono-2:::input_0',
        'source': 'JackTrip:::receive_2',
    },
    {
        'target': 'Mono-3:::input_0',
        'source': 'JackTrip:::receive_3',
    },
    {
        'target': 'Mono-4:::input_0',
        'source': 'JackTrip:::receive_4',
    },
    {
        'target': 'Mono-5:::input_0',
        'source': 'JackTrip:::receive_5',
    },
    {
        'target': 'Mono-6:::input_0',
        'source': 'JackTrip:::receive_6',
    },
    {
        'target': 'Mono-7:::input_0',
        'source': 'JackTrip:::receive_7',
    },
    {
        'target': 'Mono-8:::input_0',
        'source': 'JackTrip:::receive_8',
    },
    {
        'target': 'Stereo-1:::input_0',
        'source': 'JackTrip:::receive_1',
    },
    {
        'target': 'Stereo-1:::input_1',
        'source': 'JackTrip:::receive_2',
    },
    {
        'target': 'Stereo-2:::input_0',
        'source': 'JackTrip:::receive_3',
    },
    {
        'target': 'Stereo-2:::input_1',
        'source': 'JackTrip:::receive_4',
    },
    {
        'target': 'Stereo-3:::input_0',
        'source': 'JackTrip:::receive_5',
    },
    {
        'target': 'Stereo-3:::input_1',
        'source': 'JackTrip:::receive_6',
    },
    {
        'target': 'Stereo-4:::input_0',
        'source': 'JackTrip:::receive_7',
    },
    {
        'target': 'Stereo-4:::input_1',
        'source': 'JackTrip:::receive_8',
    },
]


DEFAULT_CONFIG = {
    'hostname': 'snappi-server',
    'channels': 8,
    'samplerate': 48000,
    'bits': 16,
    'periodsize': 512,
    'latency': 600,
    'wifi': {
        'ssid': 'Snappi',
        'password': '12345678',
        'mode': 'ap',
        'band': 'auto',
    },
    'routes': DEFAULT_ROUTES,
    'streams': [
        {'name': 'Mono-1',   'channels': 1, 'inputs': []},
        {'name': 'Mono-2',   'channels': 1, 'inputs': []},
        {'name': 'Mono-3',   'channels': 1, 'inputs': []},
        {'name': 'Mono-4',   'channels': 1, 'inputs': []},
        {'name': 'Mono-5',   'channels': 1, 'inputs': []},
        {'name': 'Mono-6',   'channels': 1, 'inputs': []},
        {'name': 'Mono-7',   'channels': 1, 'inputs': []},
        {'name': 'Mono-8',   'channels': 1, 'inputs': []},
        {'name': 'Stereo-1', 'channels': 2, 'inputs': []},
        {'name': 'Stereo-2', 'channels': 2, 'inputs': []},
        {'name': 'Stereo-3', 'channels': 2, 'inputs': []},
        {'name': 'Stereo-4', 'channels': 2, 'inputs': []},
    ],
    'uac2': {
        'enable': True,
        'name': 'SnappiAudio',
        'channels': 2,
        'samplerate': 44100,
        'bits': 16,
    },
}

