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
__QUALITY_OPTION = -1 # 0..5
__URL_LIST = {
    'tdp': 'http://hlsliveamdgl1-lh.akamaihd.net/i/hlslive_1@39733/master.m3u8',
    'tve1': 'http://hlsliveamdgl7-lh.akamaihd.net/i/hlslive_1@583043/master.m3u8',
    'tve2': 'http://hlsliveamdgl0-lh.akamaihd.net/i/hlslive_1@586367/master.m3u8',
    'tve24h': 'http://hlsliveamdgl8-lh.akamaihd.net/i/hlslive_1@583029/master.m3u8',
}

def get_link(session, channel):

    session.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'pragma': 'no-cache',
        'accept-encoding': 'gzip',
        'accept-language': 'es-ES,es;q=0.9,ca;q=0.8,en;q=0.7',
    })

    request_headers = {}

    r = session.get(__URL_LIST[channel], headers=request_headers)

    if r.status_code != 200:
        raise Exception(r.status_code, "Error {}, message: {}".format(r.status_code, r.text.encode('utf-8')))

    options = re.findall('^[^#][^\n]+', r.text, re.MULTILINE)

    stream_link = options[__QUALITY_OPTION]

    return stream_link


def get_channel_link(channel):
    with requests.Session() as s:
        return get_link(s, channel)


if __name__ == '__main__':

    with requests.Session() as s:
        if len(sys.argv) > 1:
            print(get_link(s, sys.argv[1]))

        else:
            channels = __URL_LIST.keys()

            print("Channels\n")
            for i, c in enumerate(channels):
                print(str(i) + '\t' + c)

            channel = channels[int(input('\nEnter channel index: '))]

            subprocess.call([__PLAYER, get_link(s, channel)])
