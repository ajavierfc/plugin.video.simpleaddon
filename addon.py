import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
from time import sleep

settings = xbmcaddon.Addon(id='plugin.video.simpleaddon')


def ADD_LINKS():
    img_path = xbmcaddon.Addon().getAddonInfo("path") + "/img/"

    addLink('Boing', 'boing', 1, img_path + 'boing.png')
    addLink('Divinity', 'divinity', 1, img_path + 'divinity.png')
    addLink('FDF', 'fdf', 1, img_path + 'fdf.png')
    addLink('Energy', 'energy', 1, img_path + 'energy.png')
    addLink('BeMad', 'bemad', 1, img_path + 'bemad.png')
    addLink('Antena 3', 'ANTENA_3', 2, img_path + 'antena3.png')
    addLink('La sexta', 'LA_SEXTA', 2, img_path + 'lasexta.png')
    addLink('Neox', 'NEOX', 2, img_path + 'neox.png')
    addLink('Nova', 'NOVA', 2, img_path + 'nova.png')
    addLink('Mega', 'MEGA', 2, img_path + 'mega.png')
    addLink('Atreseries', 'ATRESERIES', 2, img_path + 'atreseries.png')
    addLink('GOL', 'golt', 3, img_path + 'golt.png')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PLAY_URL(url, name):
    xbmc.log('URL=' + url)
    progress = xbmcgui.DialogProgress()
    progress.create("", name, "Espera unos segundos...")
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

    elif mode == 0:
        PLAY_URL(url, name)

    elif mode == 1:
        import lib.mitele
        PLAY_URL(lib.mitele.get_channel_link(url), name)

    elif mode == 2:
        import lib.atresplayer
        PLAY_URL(lib.atresplayer.get_channel_link(url), name)

    elif mode == 3:
        import lib.golt
        PLAY_URL(lib.golt.get_channel_link(), name)


if __name__ == "__main__":
    main()
