import urllib,urllib2,re,cookielib,os,sys
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

def MMAFList(murl):
        if murl=='http://www.mmafighting.com/videos':
            link=main.OPENURL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
            match = re.compile('<img alt=.+? data-original="([^<]+)" em_content=.+?<a href=".+?href=".+?href=".+?<h3><a href="(.+?)">(.+?)</a></h3>').findall(link)
            for  thumb,url, name in match:
                main.addPlayMs(name,url,114,thumb,'','','','','')
            main.addDir('Next','http://www.mmafighting.com/videos/archives',113,art+"/next2.png")
        else:
            link=main.OPENURL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
            match = re.compile('<img alt=.+? data-original="([^<]+)" em_content=.+?<a href=".+?href=".+?href=".+?<h3><a href="(.+?)">(.+?)</a></h3>').findall(link)
            for thumb,url, name in match:
                main.addPlayMs(name,url,114,thumb,'','','','','')
            paginate = re.compile('<a href="([^<]+)" rel="next">Next</a>').findall(link)
            if len(paginate)>0:
                main.addDir('Next',paginate[0],113,art+"/next2.png")
        main.VIEWSB()

def MMAFLink(mname,murl,thumb2):
    main.GA("MMA-Fighting","Watched")
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    ok=True
    match=re.compile('content="https://player.ooyala.com/tframe.html.?ec=(.+?)&pbid=.+?"').findall(link)
    if len(match)>0:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
        desci=re.compile('<meta property="og:description" content="(.+?)" />').findall(link)
        if len(desci)>0:
            desc=desci[0]
        else:
            desc=''
        thumbi=re.compile('<meta property="og:image" content="(.+?)" />').findall(link)
        if len(thumbi)>0:
            thumb=thumbi[0]
        else:
            thumb=''
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        durl='http://player.ooyala.com/player/ipad/'+match[0]+'.m3u8'
        link2=main.OPENURL(durl)
        match=re.compile('http://(.+?).m3u8').findall(link2)
        if len(match)==0:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Played,5000)")
        else:
            if selfAddon.getSetting("vice-qua") == "0":
                try:
                    stream_url = 'http://'+match[len(match)-1]+'.m3u8'
                except:
                    stream_url = 'http://'+match[0]+'.m3u8'
            elif selfAddon.getSetting("vice-qua") == "1":
                try:
                    stream_url = 'http://'+match[0]+'.m3u8'
                except:
                    stream_url = 'http://'+match[2]+'.m3u8'
            else:
                try:
                    stream_url = 'http://'+match[2]+'.m3u8'
                except:
                    stream_url = 'http://'+match[0]+'.m3u8'
            listitem = xbmcgui.ListItem(mname, thumbnailImage= thumb)
            listitem.setInfo("Video", infoLabels={ "Title": mname, "Plot": desc})
            # play with bookmark
            playlist.add(stream_url,listitem)
            player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
            player.play(playlist)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]MMAFighting[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
            while player._playbackLock.isSet():
                    addon.log('Playback lock set. Sleeping for 250.')
                    xbmc.sleep(250)
            return ok
    else:
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        match=re.compile('src="//www.youtube.com/embed/(.+?)"').findall(link)
        if len(match)>0:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
            stream_url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+match[0] 
            # play with bookmark
            playlist.add(stream_url,listitem)
            player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
            player.play(playlist)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]MMAFighting[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb2, fanart='', is_folder=False)
            while player._playbackLock.isSet():
                    addon.log('Playback lock set. Sleeping for 250.')
                    xbmc.sleep(250)
            return ok
        
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Found,5000)")
