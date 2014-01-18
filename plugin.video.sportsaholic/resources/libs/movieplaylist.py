import urllib,urllib2,re,cookielib,sys,os,urlresolver
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
net = Net()
from urlresolver import common

#Sports-A-Holic - by Mash2k3 2013.


from universal import playbackengine, watchhistory
addon_id = 'plugin.video.sportsaholic'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.sportsaholic', sys.argv)
art = main.art
    
wh = watchhistory.WatchHistory('plugin.video.sportsaholic')



def Mplaylists(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip='Unknown'
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fan=f[0]
        else:
                fan=art+'/fanart2.jpg'
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><date>(.+?)</date>').findall(link)
        for name,url,thumb,date in match:
            main.addDirc(name+' [COLOR red] Updated '+date+'[/COLOR]',url,236,thumb,'',fan,'','','')
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addPlayc(name,image,244,thumb,'',fan,'','','')
        main.GA("MoviePL",vip+"-Directory")


def MList(mname,murl):
        mname  = mname.split('[C')[0]
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip='Unknown'
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fan=f[0]
        else:
                fan=art+'/fanart2.jpg'
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addPlayc(name,image,244,thumb,'',fan,'','','')
                
        directory=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail></dir>').findall(link)
        for name,url,thumb in directory:
                main.addDirb(name,url,236,thumb,fan)
        
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,url,thumb in match:
                
                if '</sublink>' in url:
                        main.addDirMs(name+' [COLOR blue]'+vip+'[/COLOR]',url,249,thumb,'',fan,'','','')
                        
                else:        
                        main.addPlayMs(name+' [COLOR blue]'+vip+'[/COLOR]',url,237,thumb,'',fan,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA(vip+"-Directory",vip+"-Playlist")



def subLink(mname,suburl):
        match=re.compile('<sublink>(.+?)</sublink>').findall(suburl)
        for url in match:
                match6=re.compile('http://(.+?)/.+?').findall(url)
                for url2 in match6:
                        host = url2.replace('www.','').replace('.in','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','')
                        main.addPlayc(mname+' [COLOR blue]'+host.upper()+'[/COLOR]',url,237,art+'/mainevent.png','','','','','')

def MLink(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
        hosted_media = urlresolver.HostedMediaFile(url=murl)
        try:
            if hosted_media:
                source = hosted_media
                if source:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")
                        stream_url = source.resolve()
                else:
                        stream_url = False
                        return
            else:
                stream_url = murl
            infoL={'Title': mname, 'Plot': '', 'Genre': ''}
            # play with bookmark
            stream_url=stream_url.replace(' ','%20')
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='', title=str(mname),season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallback,imdb_id='')
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(mname+' '+'[COLOR green]Main Event[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok

