import urllib,urllib2,re,cookielib,string,os,sys
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



def MAIN():
        main.GA("None","GolfChannel")
        main.addDir('Full Episodes','http://www.golfchannel.com/tv/?WOtab=#watchOnlineTab',218,art+'/golfchannel.png')
        main.addDir('Featured Videos','http://www.golfchannel.com/search/?&q=&submitSearch=+&mediatype=Video',221,art+'/golfchannel.png')

def LIST(murl):
        main.GA("GolfChannel","List")
        link=main.OPENURL(murl)
        link=main.unescapes(link)
        match = re.compile('<div class="showThumbNailItem .+?<img src="(.+?)" class=".+?" /></a> <h4>                                               <a href=".+?" title=".+?">(.+?)</a>                                                               </h4> <small(.+?)/small>                                    <strong>Watch Full Episodes:</strong><br />(.+?)</div>').findall(link)
        for thumb, name,desc,url in match:
            thumb=thumb.replace(' ','%20')
            main.addDirc(name,url,219,thumb,desc,'','','','')

def LIST3(murl):
        link=main.OPENURL(murl)
        link=main.unescapes(link)
        match = re.compile("""<a title="([^<]+)" target="" rel=".+? href="(.+?)"><img src=".+?onerror=".+?altVideoThumbnail.?this, '(.+?)'.?"></a>.+?<p class="ez-desc">(.+?)</p>""").findall(link)
        for name,url,thumb,desc in match:
            thumb=thumb.replace(' ','%20')
            main.addPlayMs(name,url,220,thumb,desc,'','','','')
        paginate = re.compile("""href="javascript:window.location='(.+?)';" class=".+?">Next</a><a title=".+?" rel=".+?" onclick=".+?""").findall(link)
        if len(paginate)>0:
            paginates=main.unescapes(paginate[0])
            main.addDir('Next',paginates,221,art+'/next2.png')

             


def LIST2(mname,murl,thumb,desc):
        main.GA("GolfChannel","List")
        match = re.compile('<a href="(.+?)" class="showLinks">(.+?)</a>').findall(murl)
        for url,name in match:
            main.addPlayMs(mname+" [COLOR red]"+name+"[/COLOR]",'http://www.golfchannel.com'+url,220,thumb,'','','','','')


def LINK(mname,murl,thumb):
        
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Playing Video,4000)")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        ok= True
        link=main.OPENURL(murl)
        link=main.unescapes(link)
        r = re.findall('player.releaseURL = "(.+?)";',link)
        if r:
            print r
            try: 
                    link=main.OPENURL(r[0])
                    link=main.unescapes(link)
            except:
                    xbmc.executebuiltin("XBMC.Notification(Sorry!,No Link Found,3000)")
                    link=''
            match = re.findall('<video src="(.+?)" title=.+?abstract="(.+?)"',link)
            for vurl,desc in match:
                    flv = re.findall('flv',vurl)
                    if flv:
                            vid='rtmp://cp74847.edgefcs.net/ondemand/'+vurl
                    else:
                            vid=vurl
                    stream_url=vid
                    listitem = xbmcgui.ListItem(mname,thumbnailImage=thumb)
                    listitem.setInfo("Video", infoLabels={ "Title": mname, "Plot": desc})
                    # play with bookmark
                    playlist.add(stream_url,listitem)
                    player = playbackengine.Player(plugin='plugin.video.movie25', video_type='', title=mname,season='', episode='', year='', watch_percent=0.85, watchedCallback=main.WatchedCallback)                
                    player.play(playlist)
                    main.GA("GolfChannel","Watched")
                    #WatchHistory
                    if selfAddon.getSetting("whistory") == "true":
                        wh.add_item(mname+' '+'[COLOR green]GolfChannel[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                    while player._playbackLock.isSet():
                        addon.log('Playback lock set. Sleeping for 250.')
                        xbmc.sleep(250)
                    return ok
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,No Link Found,3000)")
        return ok
