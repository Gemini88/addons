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

def OC():
        main.addDir('All Videos','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=',51,art+'/OC.png')
        main.addDir('Hunting','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=Outdoor%20Channel/Hunting',51,art+'/OC.png')
        main.addDir('Fishing','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=Outdoor%20Channel/Fishing',51,art+'/OC.png')
        main.addDir('Shooting','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=Outdoor%20Channel/Shooting',51,art+'/OC.png')
        main.addDir('Off Road','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=Outdoor%20Channel/Off-Road',51,art+'/OC.png')
        main.addDir('Adventure','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=Outdoor%20Channel/Adventure',51,art+'/OC.png')
        main.addDir('Conservation','http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/swTdEQGW9CKd?byCategories=Outdoor%20Channel/Conservation',51,art+'/OC.png')
        main.GA("None","OutChannel")

def OCList(murl):
        link=main.OPENURL(murl)
        match=re.compile('<item><titl[^>]+>([^<]+)</title><description>(.+?)</description>.+?<plrelease:url>(.+?)</plrelease:url></plfile:release></media:content><pubDate>.+?</pubDate><plmedia:defaultThumbnailUrl>(.+?)</plmedia:defaultThumbnailUrl>').findall(link)
        for name,desc,url,thumb in match:
                main.addPlayMs(name,url,52,thumb,desc,'','','','')
        main.GA("Sports","OC-List")

def OCLink(mname,url,thumb):
        main.GA("OC-List","Watched")
        link=main.OPENURL(url)
        ok=True
        match=re.compile('<video src="(.+?)" title="(.+?)" abstract="(.+?)" copyright="Outdoor Channel"').findall(link)
        for video, title, desc in match:
                print video
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = video
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo("Video", infoLabels={ "Title": mname, "Plot": desc})
        # play with bookmark
        playlist.add(stream_url,listitem)
        player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
        player.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Outdoor[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        while player._playbackLock.isSet():
            addon.log('Playback lock set. Sleeping for 250.')
            xbmc.sleep(250)
        return ok
