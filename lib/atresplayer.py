#!/usr/bin/env python

import sys
import requests
import json
import subprocess
import re

if sys.version_info[0] < 3:
    from exceptions import Exception
else:
    from builtins import Exception

__PLAYER = "mpv"
__QUALITY_OPTION = 1 # 0..3

def get_link(session, channel):
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'pragma': 'no-cache',
        'accept-encoding': 'gzip',
        'accept-language': 'es-ES,es;q=0.9,ca;q=0.8,en;q=0.7',
    })

    request_headers = {}

    r = session.get('https://www.atresplayer.com/', headers=request_headers)

    if r.status_code != 200:
        raise Exception(r.status_code, "Error {}, message: {}".format(r.status_code, r.text.encode('utf-8')))

    m = re.findall('= ({.*SERVICES_HOST[^;]+)', r.text.encode('utf-8'))

    if not m:
        raise Exception(1, "Service host list not found")

    hosts = json.loads(m[0])

    channel_id = hosts[channel + '_ID']

    r = session.get('https://api.atresplayer.com/client/v1/player/live/' + channel_id, headers=request_headers)

    if r.status_code != 200:
        raise Exception(r.status_code, "Error {}, message: {}".format(r.status_code, r.text.encode('utf-8')))

    channel_info = json.loads(r.text.encode('utf-8'))

    master = channel_info['sources'][0]['src']

    r = session.get(master, headers=request_headers)

    options = re.findall('^[^#][^\n]+', r.text, re.MULTILINE)

    stream_link = re.sub('[^/]+$', options[__QUALITY_OPTION], master)

    return stream_link


def get_channel_link(channel):
    with requests.Session() as s:
        return get_link(s, channel)


if __name__ == '__main__':

    with requests.Session() as s:
        if len(sys.argv) > 1:
            print(get_link(s, sys.argv[1]))

        else:
            channels = ['ANTENA_3', 'LA_SEXTA', 'NEOX', 'NOVA', 'MEGA', 'ATRESERIES']

            print("Channels\n")
            for i, c in enumerate(channels):
                print(str(i) + '\t' + c)

            channel = channels[int(input('\nEnter channel index: '))]

            subprocess.call([__PLAYER, get_link(s, channel)])
