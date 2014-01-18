import urllib,urllib2,re,cookielib,string, urlparse,sys,os
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

def WILDTV(murl):
        main.GA("None","Wildtv")
        link=main.OPENURL(murl)
        match=re.compile('<option value="(.+?)">(.+?)</option>').findall(link)
        for idnum, name in match:
            url='https://www.wildtv.ca/show/'+idnum
            main.addDir(name,url,93,art+'/wildtv.png')

def LISTWT(murl):
        main.GA("Wildtv","Wildtv-list")
        link=main.OPENURL(murl)
        match=re.compile('alt="Video: (.+?)" href="(.+?)">\r\n<img class=".+?" src="(.+?)"').findall(link)
        for name, url, thumb in match:
            thumb='https:'+thumb
            url='https://www.wildtv.ca/' +url
            main.addPlayMs(name,url,94,thumb,'','','','','')

def LINKWT(mname,murl):
        main.GA("Wildtv-list","Watched")
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Playing Link,3000)")
        link=main.OPENURL(murl)
        ok=True
        stream=re.compile('streamer: "(.+?)",').findall(link)
        Path=re.compile('file: "mp4:med/(.+?).mp4",').findall(link)
        if len(Path)>0:
            desc=re.compile('<meta name="description" content="(.+?)" />').findall(link)
            if len(desc)>0:
                desc=desc[0]
            else:
                desc=''
            thumb=re.compile('image: "(.+?)",').findall(link)
            if len(thumb)>0:
                thumb='https:'+thumb[0]
            else:
                thumb=''
            stream_url = stream[0]+'/'
            if selfAddon.getSetting("wild-qua") == "0":
                    playpath = 'mp4:high/'+Path[0]+'.mp4'
            elif selfAddon.getSetting("wild-qua") == "1":
                    playpath = 'mp4:med/'+Path[0]+'.mp4'
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            listitem = xbmcgui.ListItem(mname, thumbnailImage= thumb)
            listitem.setProperty('PlayPath', playpath);
            listitem.setInfo("Video", infoLabels={ "Title": mname, "Plot": desc})
            # play with bookmark
            playlist.add(stream_url,listitem)
            player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
            player.play(playlist)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]WildTv[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
            while player._playbackLock.isSet():
                    addon.log('Playback lock set. Sleeping for 250.')
                    xbmc.sleep(250)
            return ok
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link not found,3000)")
