import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Sports-A-Holic - by Mash2k3 2012.

from t0mm0.common.addon import Addon
import playbackengine
addon_id = 'plugin.video.sportsaholic'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
art = main.art
from universal import watchhistory
wh = watchhistory.WatchHistory('plugin.video.sportsaholic')


def YOUList(mname,durl):
        if 'gdata' in durl:
                murl=durl
        else:
                murl='http://gdata.youtube.com/feeds/api/users/'+durl+'/uploads?start-index=1&max-results=50'
        link=main.OPENURL(murl)
        match=re.compile("http\://www.youtube.com/watch\?v\=([^\&]+)\&.+?<media\:descriptio[^>]+>([^<]+)</media\:description>.+?<media\:thumbnail url='([^']+)'.+?<media:title type='plain'>(.+?)/media:title>").findall(link)
        for url,desc,thumb,name in match:
                name=name.replace('<','')
                main.addPlayMs(name,url,48,thumb,desc,'','','','')
        if len(match) >=49:   
            paginate=re.compile('http://gdata.youtube.com/feeds/api/users/(.+?)/uploads.?start-index=(.+?)&max-results=50').findall(murl)
            for id, page in paginate:
                i=int(page)+50
                purl='http://gdata.youtube.com/feeds/api/users/'+id+'/uploads?start-index='+str(i)+'&max-results=50'
                main.addDir('[COLOR blue]Next[/COLOR]',purl,47,art+'/next2.png')

def YOULink(mname,url,thumb):
        ok=True
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+url+"&hd=1"
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = url
        listitem = xbmcgui.ListItem(mname,thumbnailImage=thumb)
        # play with bookmark
        playlist.add(stream_url,listitem)
        player = playbackengine.Player(plugin='plugin.video.sportsholic', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
        player.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]YoutubeChannel[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        while player._playbackLock.isSet():
            addon.log('Playback lock set. Sleeping for 250.')
            xbmc.sleep(250)
        return ok
