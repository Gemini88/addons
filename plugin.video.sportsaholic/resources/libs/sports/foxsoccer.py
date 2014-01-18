import urllib,urllib2,re,cookielib,string, urlparse,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Sports-A-Holic - by Mash2k3 2013.

from t0mm0.common.addon import Addon
import playbackengine
addon_id = 'plugin.video.sportsaholic'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
art = main.art
from universal import watchhistory
wh = watchhistory.WatchHistory('plugin.video.sportsaholic')

def FOXSOC():
        main.addDir('Premier League','http://edge4.catalog.video.msn.com/videoByTag.aspx?ff=8a&ind=1&mk=us&ns=Fox%20Sports_Gallery&ps=100&rct=1,3&sf=ActiveStartDate&tag=premier%20league&vs=1&responseEncoding=xml&template=foxsports',125,art+'/foxsoc.png')
        main.addDir('Champions League','http://edge4.catalog.video.msn.com/videoByTag.aspx?ff=8a&ind=1&mk=us&ns=Fox%20Sports_Gallery&ps=100&rct=1,3&sf=ActiveStartDate&tag=champions%20league&vs=1&responseEncoding=xml&template=foxsports',125,art+'/foxsoc.png')
        main.addDir('FA Cup','http://edge4.catalog.video.msn.com/videoByTag.aspx?ff=8a&ind=1&mk=us&ns=Fox%20Sports_Gallery&ps=100&rct=1,3&sf=ActiveStartDate&tag=fa%20cup&vs=1&responseEncoding=xml&template=foxsports',125,art+'/foxsoc.png')
        main.addDir('USA','http://edge4.catalog.video.msn.com/videoByTag.aspx?ff=8a&ind=1&mk=us&ns=Fox%20Sports_Gallery&ps=100&rct=1,3&sf=ActiveStartDate&tag=usa&vs=1&responseEncoding=xml&template=foxsports',125,art+'/foxsoc.png')
        main.addDir('Euro 2012','http://edge4.catalog.video.msn.com/videoByTag.aspx?ff=8a&ind=1&mk=us&ns=Fox%20Sports_Gallery&ps=100&rct=1,3&sf=ActiveStartDate&tag=euro%202012&vs=1&responseEncoding=xml&template=foxsports',125,art+'/foxsoc.png')
        main.GA("None","FoxSoccer")
def FOXSOCList(murl):
        main.GA("FoxSoccer","List")
        link=main.OPENURL(murl)
        match=re.compile('<video xmlns=".+?">(.+?)</video>').findall(link)
        for entry in match:
            name=re.compile('<title>([^<]+)</title>').findall(entry)
            desc=re.compile('<description>([^<]+)</description>').findall(entry)
            thumb=re.compile('<file formatCode="2001".+?<uri>([^<]+)</uri></file>').findall(entry)
            main.addPlayMs(name[0],entry,126,thumb[0],desc[0],'','','','')

def FOXSOCLink(mname,entry):
        main.GA("FoxSoccer","Watched")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        ok= True
        low=re.compile('<videoFile formatCode="102".+?<uri>([^<]+)</uri></videoFile>').findall(entry)
        med=re.compile('<videoFile formatCode="103".+?<uri>([^<]+)</uri></videoFile>').findall(entry)
        high=re.compile('<videoFile formatCode="104".+?<uri>([^<]+)</uri></videoFile>').findall(entry)
        if selfAddon.getSetting("tsn-qua") == "0":
            if len(high)>0:
                stream_url=high[0]
            else:
                stream_url=low[0]
        if selfAddon.getSetting("tsn-qua") == "1":
            if len(med)>0:
                stream_url=med[0]
            else:
                stream_url=low[0]
        if selfAddon.getSetting("tsn-qua") == "2":
            if len(low)>0:
                stream_url=low[0]
            else:
                stream_url=med[0]
        desc=re.compile('<description>([^<]+)</description>').findall(entry)
        thumb=re.compile('<file formatCode="2001".+?<uri>([^<]+)</uri></file>').findall(entry)
        listitem = xbmcgui.ListItem(mname, thumbnailImage= thumb[0])
        listitem.setInfo("Video", infoLabels={ "Title": mname, "Plot": desc[0]})
        # play with bookmark
        playlist.add(stream_url,listitem)
        player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
        player.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Fox Soccer[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb[0], fanart='', is_folder=False)
        while player._playbackLock.isSet():
            addon.log('Playback lock set. Sleeping for 250.')
            xbmc.sleep(250)
        return ok
