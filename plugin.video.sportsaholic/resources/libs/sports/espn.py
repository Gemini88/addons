import urllib,urllib2,re,cookielib,string, urlparse,os,sys
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

def ESPN():
        main.addDir('NFL','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3520083',45,art+'/espn.png')
        main.addDir('NBA','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3631756',45,art+'/espn.png')
        main.addDir('NCAAM','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3707293',45,art+'/espn.png')
        main.addDir('NCAAF','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3573504',45,art+'/espn.png')
        main.addDir('TENNIS','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=4830039',45,art+'/espn.png')
        main.addDir('MLB','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3573503',45,art+'/espn.png')
        main.addDir('MMA','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3685710',45,art+'/espn.png')
        main.addDir('BOXING','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=4117562',45,art+'/espn.png')
        main.addDir('NHL','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3631758',45,art+'/espn.png')
        main.addDir('GOLF','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=4331063',45,art+'/espn.png')
        main.addDir('MOTORSPORTS','http://m.espn.go.com/mobilecache/general/apps/videohub/moreVideos?xhr=1&pageNum=1&numResults=100&trackingPage=espntablet%3Ageneral%3Avideo&format=json&cid=3879997',45,art+'/espn.png')
        main.GA("None","ESPN")

def ESPNList(murl):
        link=main.OPENURL(murl)
        match=re.compile('"videoDuration":"(.+?)",.+?"video":.+?{"headline":"(.+?)",.+?,"includePlatforms":.+?,"imageUrl":"(.+?)","mobileSubHead":"(.+?)","internalUrl720p":"(.+?)",').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Sports list is loaded.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Loading....[/B]',remaining_display)
        for dur,name,thumb,desc, url, in match:
                dur=dur.replace('00:','')
                main.addPlayMs(name,url,46,thumb,desc,'',dur,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Loading....[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("ESPN","ESPN-List")

def ESPNLink(mname,murl,thumb,desc):
        main.GA("ESPN-List","Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = murl
        listitem = xbmcgui.ListItem(thumbnailImage= thumb)
        listitem.setInfo("Video", infoLabels={ "Title": mname, "Plot": desc})
        # play with bookmark
        playlist.add(stream_url,listitem)
        player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
        player.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Espn[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        while player._playbackLock.isSet():
            addon.log('Playback lock set. Sleeping for 250.')
            xbmc.sleep(250)
        return ok
