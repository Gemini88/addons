import urllib,re,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
from t0mm0.common.net import Net as net
#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
smalllogo=art+'/smallicon.png'
    
user = selfAddon.getSetting('username')
passw = selfAddon.getSetting('password')
CookiesPath=os.path.join(main.datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
cookie_file = os.path.join(CookiesPath, 'noobroom.cookies')
if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR=FF67cc33]MashUp[/COLOR]", "Please set your Noobroom credentials", "in Addon settings under logins tab")
    selfAddon.openSettings()
    user = selfAddon.getSetting('username')
    passw = selfAddon.getSetting('password')

def setCookie(nrDomain):
    cookieExpired = False
    if os.path.exists(cookie_file):
        try:
            cookie = open(cookie_file).read()
            if not nrDomain.replace('http://','') in cookie:
                cookieExpired = True
        except: cookieExpired = True 
    if not os.path.exists(cookie_file) or cookieExpired:
        net().http_GET(nrDomain+'/login.php')
        net().http_POST(nrDomain+'/login2.php',{'email':user,'password':passw})
        net().save_cookies(cookie_file)
    else:
        net().set_cookies(cookie_file)     
               
def GetNewUrl():
    link=main.OPENURL('http://www.noobroom.com')
    match=re.compile('value="(.+?)">').findall(link)
    return match[0]

def LISTSP5(murl, retries = 1):
    try:
        nrDomain = GetNewUrl()
        murl=nrDomain+'/latest.php'
        setCookie(nrDomain)
        response = net().http_GET(murl)
    except:
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Noobroom website is down,5000,"+smalllogo+")")
        return
    link = response.content
    link = link.decode('iso-8859-1').encode('utf8')
    if response.get_url() != murl or murl+'?ckattempt' in link:
        if os.path.exists(cookie_file):
            try: os.remove(cookie_file)
            except: pass
        if murl+'?ckattempt' in link:
            if retries:
                retries -= 1
                return LISTSP5('retry',retries)
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Email or Password Incorrect,10000,"+smalllogo+")")
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'',art+'/link.png')
    match=re.compile("<br>(.+?) - <a[^>]+?href='(.+?)'>(.+?)</a>").findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    id = 1;
    for year,url,name in match:
        name=fix_title(main.unescapes(name))
        if(year=='0'):
                year='0000'  
        url=nrDomain+url
        main.addDown3(name+' [COLOR red]('+year+')[/COLOR]',url,58,'','',id)
        id += 1
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False    
    dialogWait.close()
    del dialogWait
    main.GA("HD","Starplay")
    main.VIEWS()
        
def fix_title(name):
    if name == "+1":
        name = "+1 (plus 1)"
    return name

def find_noobroom_video_url(page_url):
    import urllib2
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'}
    setCookie(re.sub('http://([^/]+?)/.*','\\1',page_url))
    html = net().http_GET(page_url).content
    media_id = re.compile('"file": "(.+?)"').findall(html)[0]
    fork_url = re.compile('"streamer": "(.+?)"').findall(html)[0] + '&start=0&file=' + media_id

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):    
        def http_error_302(self, req, fp, code, msg, headers):
            #print headers
            self.video_url = headers['Location']
            #print self.video_url
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    myhr = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(net()._cj),
        urllib2.HTTPBasicAuthHandler(),
        myhr)
    urllib2.install_opener(opener)

    req = urllib2.Request(fork_url)
    for k, v in headers.items():
        req.add_header(k, v)
    try: response = urllib2.urlopen(req)
    except: pass

    #print myhr.video_url
    return myhr.video_url

def download_noobroom_video(name,url):#starplay/noobroom
    originalName=name
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")

    stream_url= find_noobroom_video_url(url)
    name=name.split(' [')[0]
    name=name.replace('/','').replace('.','').replace(':','')

    if stream_url:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,2000)")
        if os.path.exists(main.downloadPath):
            match1=re.compile("flv").findall(stream_url)
            if len(match1)>0:
                name=name+'.flv'
            match2=re.compile("mkv").findall(stream_url)
            if len(match2)>0:
                name=name+'.mkv'
            match3=re.compile("mp4").findall(stream_url)
            if len(match3)>0:
                name=name+'.mp4'
            match4=re.compile("avi").findall(stream_url)
            if len(match4)>0:
                name=name+'.avi'
            mypath=os.path.join(main.downloadPath,name)
            if os.path.isfile(mypath) is True:
                xbmc.executebuiltin("XBMC.Notification(Download Alert!,The video you are trying to download already exists!,8000)")
            else:
                DownloadInBack=selfAddon.getSetting('download-in-background')
                if DownloadInBack == 'true':
                    main.QuietDownload(stream_url,mypath,originalName,name)
                else:
                    main.Download(stream_url,mypath,originalName,name)
        
        else:
            xbmc.executebuiltin("XBMC.Notification(Download Alert!,You have not set the download folder,8000)")
            return False
    else:
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Found,6000)")
        return False
            
def LINKSP5(mname,url):
    main.GA("Starplay","Watched")
    ok=True
    try:
        mname  = mname.replace('[COLOR red]','').replace('[/COLOR]','')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,9000)")

        stream_url=find_noobroom_video_url(url)
        infoLabels =main.GETMETAT(mname,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from universal import watchhistory
            wh = watchhistory.WatchHistory('plugin.video.movie25')
            wh.add_item(mname+' '+'[COLOR=FF67cc33]Starplay[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart='', is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        main.ErrorReport(e)
        return ok
