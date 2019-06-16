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

__PLAYER = ["mpv", "--border=no"]
__QUALITY_OPTION = 0 # 0..3

def get_link(session):
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'pragma': 'no-cache',
        'accept-encoding': 'gzip',
        'accept-language': 'es-ES,es;q=0.9,ca;q=0.8,en;q=0.7',
    })

    request_headers = {}

    r = session.get('https://api.goltelevision.com/api/v1/media/hls/service/live', headers=request_headers)

    if r.status_code != 200:
        raise Exception(r.status_code, "Error {}, message: {}".format(r.status_code, r.text.encode('utf-8')))

    live_info = json.loads(r.text.encode('utf-8'))

    playlist = live_info['message']['success']['manifest']

    request_headers = {}

    r = session.get(playlist, headers=request_headers)

    if r.status_code != 200:
        raise Exception(r.status_code, "Error {}, message: {}".format(r.status_code, r.text.encode('utf-8')))

    options = re.findall('^[^#][^\n]+', r.text, re.MULTILINE)

    stream_link = options[__QUALITY_OPTION]

    return stream_link.strip()


def get_channel_link():
    with requests.Session() as s:
        return get_link(s)


if __name__ == '__main__':

    with requests.Session() as s:
        if len(sys.argv) > 1:
            print(get_link(s))

        else:
            subprocess.call(__PLAYER + [get_link(s)])
