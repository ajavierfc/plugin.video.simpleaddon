import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
from time import sleep


NONLIB = 0
MEDIASET = 1
ATRESMEDIA = 2
GOLTV = 3
RTVE = 4


def ADD_LINKS():
    img_path = xbmcaddon.Addon().getAddonInfo("path") + "/img/"

    # mediaset (mitele)
    addLink('Boing', 'boing', MEDIASET, img_path + 'boing.png')
    addLink('Divinity', 'divinity', MEDIASET, img_path + 'divinity.png')
    addLink('FDF', 'fdf', MEDIASET, img_path + 'fdf.png')
    addLink('Energy', 'energy', MEDIASET, img_path + 'energy.png')
    addLink('BeMad', 'bemad', MEDIASET, img_path + 'bemad.png')

    # atresmedia
    addLink('Antena 3', 'ANTENA_3', ATRESMEDIA, img_path + 'antena3.png')
    addLink('La sexta', 'LA_SEXTA', ATRESMEDIA, img_path + 'lasexta.png')
    addLink('Neox', 'NEOX', ATRESMEDIA, img_path + 'neox.png')
    addLink('Nova', 'NOVA', ATRESMEDIA, img_path + 'nova.png')
    addLink('Mega', 'MEGA', ATRESMEDIA, img_path + 'mega.png')
    addLink('Atreseries', 'ATRESERIES', ATRESMEDIA, img_path + 'atreseries.png')

    # goltv
    addLink('GOL', 'golt', GOLTV, img_path + 'golt.png')

    # rtve
    addLink('Teledeporte', 'tdp', RTVE, img_path + 'tdp.png')
    addLink('La 1', 'tve1', RTVE, img_path + 'tve1.png')
    addLink('La 2', 'tve2', RTVE, img_path + 'tve2.png')
    addLink('TVE 24H', 'tve24h', RTVE, img_path + 'tve24h.png')

    # non module streams, acestream, youtube or any stream which does not depends on a lib/any.py module
    #addLink('Acestream video', 'acestream://7452663b34b9390c83547c4f4c33163d62866459', NONLIB, img_path + 'acestream.png')
    #addLink('Youtube video', 'https://www.youtube.com/watch?v=jHWPYEt8398', NONLIB, img_path + 'youtube.png')

   xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PLAY_URL(url, name):
    xbmc.log('URL=' + url, xbmc.LOGNOTICE)

    if 'acestream://' == url[0:12]:
        vurl = 'plugin://program.plexus/?mode=1&url=%s&name=%s&iconimage=' % (urllib.quote_plus(url), urllib.quote_plus(name))
        xbmc.log('VURL=' + vurl, xbmc.LOGNOTICE)
        xbmc.Player().play(vurl)
        return

    progress = xbmcgui.DialogProgress()
    progress.create("Simple Video Addon", name, "Espera unos segundos...")
    progress.update(0)
    if 'youtube.' in url:
        vurl = 'plugin://plugin.video.youtube/play/?video_id=' + url.split('=')[1]
    else:
        vurl = url
    progress.update(0, name, "Reproduciendo...")
    li = xbmcgui.ListItem()
    li.setInfo(type = "Video", infoLabels = { "Title": name })
    xbmc.Player().play(vurl, li)
    wait = 0
    while not xbmc.Player().isPlayingVideo() and not progress.iscanceled():
        sleep(1)
        wait += 5
        progress.update(wait)
        if wait == 100:
            xbmc.Player().play(vurl, li)
            break
    if progress.iscanceled():
        xbmc.Player().stop()


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def addLink(name, url, mode, iconimage="DefaultFolder.png"):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconimage,
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
        "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok


def openURL(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, timeout = 30)
    link = response.read()
    response.close()
    return link


def main():
    params = get_params()
    url = None
    name = None
    mode = None

    try:
        url = urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name = urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        mode = int(params["mode"])
    except:
        pass

    if mode == None:
        ADD_LINKS()

    elif mode == NONLIB:
        PLAY_URL(url, name)

    elif mode == MEDIASET:
        import lib.mitele
        PLAY_URL(lib.mitele.get_channel_link(url), name)

    elif mode == ATRESMEDIA:
        import lib.atresplayer
        PLAY_URL(lib.atresplayer.get_channel_link(url), name)

    elif mode == GOLTV:
        import lib.golt
        PLAY_URL(lib.golt.get_channel_link(), name)

    elif mode == RTVE:
        import lib.rtve
        PLAY_URL(lib.rtve.get_channel_link(url), name)


if __name__ == "__main__":
    main()
