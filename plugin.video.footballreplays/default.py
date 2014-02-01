import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time


PLUGIN='plugin.video.footballreplays'
ADDON = xbmcaddon.Addon(id='plugin.video.footballreplays')
maxVideoQuality = ADDON.getSetting("maxVideoQuality")
qual = ["480p", "720p", "1080p"]
maxVideoQuality = qual[int(maxVideoQuality)]


    
VERSION = "1.0.2"
PATH = "Football Replays"            
UATRACK="UA-35537758-1"  


def CATEGORIES():
    addDir('Full Matches','url',3,'','1')
    addDir('Search Team','url',4,'','1')
    addDir('Highlights','url',5 ,'','1')
    setView('movies', 'main') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
 
    
def CATEGORIES2():
    link=OPEN_URL('http://livefootballvideo.com/fullmatch')
    r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?)">.+?<img src="(.+?)".+?<p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
    match=re.compile(r,re.DOTALL).findall(link)
    print match
    for url,name,iconimage,month,day,year in match:
        _date='%s/%s/%s'%(day,month,year)  
        _name='%s-[COLOR yellow][%s][/COLOR]'%(name,_date)    
        addDir(_name,url,1,iconimage,'')
    addDir('Next Page >>','url',2,'','1')
    setView('movies', 'main') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
       
def NEXTPAGE(page):
    pagenum=int(page) +1
    link=OPEN_URL('http://livefootballvideo.com/fullmatch/page/'+str(pagenum))
    r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?)">.+?<img src="(.+?)".+?<p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
    match=re.compile(r,re.DOTALL).findall(link)
    print match
    for url,name,iconimage,month,day,year in match:
        _date='%s/%s/%s'%(day,month,year)  
        _name='%s-[COLOR yellow][%s][/COLOR]'%(name,_date)    
        addDir(_name,url,1,iconimage,'')
    addDir('Next Page >>','url',2,'','1')
    setView('movies', 'main') 
                      												  
def GETLINKS(name,url):#  cause mode is empty in this one it will go back to first directory
    link=OPEN_URL(url)
    if "www.youtube.com/embed/" in link :
        r = 'youtube.com/embed/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        yt= match[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % yt.replace('?rel=0','')
        url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % yt.replace('?rel=0','')
        addDir( name+' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , iconimage , '' )
    if "dailymotion.com" in link :
        r = 'src="http://www.dailymotion.com/embed/video/(.+?)\?.+?"></iframe>'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir ( name+' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , GETTHUMB(url), '' )
    if "http://videa" in link :
        r = 'http://videa.+?v=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]VIDEA[/COLOR]',url,200,'', '' )
            
    if "rutube.ru" in link :
        r = 'ttp://rutube.ru/video/embed/(.+?)\?'
        match = re.compile(r,re.DOTALL).findall(link)
        print match
        for url in match :
            addDir (name+' - [COLOR red]RUTUBE[/COLOR]',url,200,'', '' )
    if "playwire" in link :
        r = 'cdn.playwire.com.+?config=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]PLAYWIRE[/COLOR]',url,200,'', '' )
    if "vk.com" in link :
        r = '<iframe src="http://vk.com/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]VK.COM[/COLOR]','http://vk.com/'+url,200,'', '' )
            
        
def HIGHLIGHTS():
    link=OPEN_URL('http://livefootballvideo.com/highlights')
    r= '<div class="team home column">(.+?)&nbsp;.+?.+?<a href="(.+?)" class="score">(.+?)</a></div>.+?</noscript>&nbsp;(.+?)</div>'
    match = re.compile ( r , re.DOTALL).findall (link)
    for team_a ,url,score,  team_b  in match :
        name = '%s vs %s [COLOR yellow]%s[/COLOR]' % ( team_a , team_b,score )
        iconimage = 'http://livefootballvideo.com'
        addDir(name,url,7,iconimage,'')
    addDir('Next Page >>' , 'url' , 6 , '' , '1' )
    setView('movies', 'default') 
    
def HIGHLIGHTS_NEXTPAGE( page ) :
    page_num =int ( page ) + 1
    link=OPEN_URL( 'http://livefootballvideo.com/highlights/page/' + str ( page_num ) )
    r= '<div class="team home column">(.+?)&nbsp;.+?.+?<a href="(.+?)" class="score">(.+?)</a></div>.+?</noscript>&nbsp;(.+?)</div>'
    match = re.compile ( r , re.DOTALL).findall (link)
    for team_a ,url,score,  team_b  in match :
        name = '%s vs %s [COLOR yellow]%s[/COLOR]' % ( team_a , team_b,score )
        iconimage = 'http://livefootballvideo.com'
        addDir(name,url,7,iconimage,'')
    addDir('Next Page >>' , 'url' , 6 , '' , '1' )
    setView('movies', 'default') 
    
    
    
def HIGHLIGHTS_LINKS(name,url):
    link = OPEN_URL( url )
    if "www.youtube.com/embed/" in link :
        r = 'youtube.com/embed/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        yt= match[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % yt.replace('?rel=0','')
        url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % yt.replace('?rel=0','')
        addDir( name+' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , iconimage , '' )
    if "dailymotion.com" in link :
        r = 'src="http://www.dailymotion.com/embed/video/(.+?)\?.+?"></iframe>'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir ( name+' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , GETTHUMB(url), '' )
    if "http://videa" in link :
        r = 'http://videa.+?v=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]VIDEA[/COLOR]',url,200,'', '' )
            
    if "rutube.ru" in link :
        r = 'rutube.ru/video/embed/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]RUTUBE[/COLOR]',url,200,'', '' )
            
    if "playwire" in link :
        r = 'cdn.playwire.com.+?config=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]PLAYWIRE[/COLOR]',url,200,'', '' )
    if "vk.com" in link :
        r = '<iframe src="(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]VK.COM[/COLOR]',url,200,'', '' )
        
def Search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Football Replays')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20#
            if search_entered == None:
                return False
        link=OPEN_MAGIC('http://www.google.com/cse?cx=partner-pub-9069051203647610:8413886168&ie=UTF-8&q=%s&sa=Search&ref=livefootballvideo.com/highlights'%search_entered)
        match=re.compile('" href="(.+?)" onmousedown=".+?">(.+?)</a>').findall(link)
        for url,dirtyname in match: 
            import HTMLParser
            cleanname= HTMLParser.HTMLParser().unescape(dirtyname)
            name= cleanname.replace('<b>','').replace('</b>','')
            addDir(name,url,1,'','')
        setView('movies', 'default') 
        
        
def GETTHUMB(url):
    try:
        import json
        content = OPEN_URL('https://api.dailymotion.com/video/%s?fields=thumbnail_large_url'%url)
        data = json.loads(content)
        icon=data['thumbnail_large_url']
        return icon
    except:
        return ''
        
        
def getStreamUrl(id):
    content = OPEN_URL("http://www.dailymotion.com/embed/video/"+id)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,Not Found (DailyMotion)!,5000)')
        return ""
    else:
        matchFullHD = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(content)
        matchHD = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(content)
        matchHQ = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(content)
        matchSD = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(content)
        matchLD = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(content)
        url = ""
        if matchFullHD and maxVideoQuality == "1080p":
            url = urllib.unquote_plus(matchFullHD[0]).replace("\\", "")
        elif matchHD and (maxVideoQuality == "720p" or maxVideoQuality == "1080p"):
            url = urllib.unquote_plus(matchHD[0]).replace("\\", "")
        elif matchHQ:
            url = urllib.unquote_plus(matchHQ[0]).replace("\\", "")
        elif matchSD:
            url = urllib.unquote_plus(matchSD[0]).replace("\\", "")
        elif matchLD:
            url = urllib.unquote_plus(matchLD[0]).replace("\\", "")
        return url
        
        
        
def GrabRu(id):
    print id
    link = OPEN_URL('http://rutube.ru/api/play/trackinfo/%s/?format=xml'%str(id))
    r = '<m3u8>(.+?)</m3u8>'
    match = re.compile(r,re.DOTALL).findall(link)
    return match[0]
    
def GrabVidea(id):
    link = OPEN_URL('http://videa.hu/flvplayer_get_video_xml.php?v=%s&m=0'%str(id))
    name=[]
    url=[]
    r = 'version quality="(.+?)" video_url="(.+?)"'
    match = re.compile(r,re.DOTALL).findall(link)
    for quality,stream in match:
        name.append(quality.title())
        url.append(stream)
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

def GrabVK(url):
    print url
    link = OPEN_URL(url.replace('amp;',''))
    print link
    name=[]
    url=[]
    r      ='"url(.+?)":"(.+?)"'
    match = re.compile(r,re.DOTALL).findall(link)
    for quality,stream in match:
        name.append(quality+'p')
        url.append(stream.replace('\/','/'))
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
        
        
        
def PLAYSTREAM(name,url,iconimage):
        if 'YOUTUBE' in name:
            link = str(url)
        elif 'VIDEA' in name:
            link = GrabVidea(url)
        elif 'VK.COM' in name:
            link = GrabVK(url)
            
        elif 'RUTUBE' in name:
            try:
                html = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml'% url.replace('_ru','')
                print html
                link = OPEN_URL(html)
                r = '<m3u8>(.+?)</m3u8>'
                match = re.compile(r,re.DOTALL).findall(link)
                if match:
                    link=match[0]
                else:
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                    return
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                return
        elif 'PLAYWIRE' in name:
            link = OPEN_URL(url)
            r = '"src":"(.+?)"'
            match = re.compile(r,re.DOTALL).findall(link)
            if match:
                link=match[0]
        elif 'DAILYMOTION' in name:
            link = getStreamUrl(url)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        liz.setProperty("IsPlayable","true")
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(link, liz)
        xbmc.Player().play(pl)
        
        
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


        
# this is the listing of the items        
def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        if mode == 200:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
#same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content         
def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
 
        
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
page=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        GETLINKS(name,url)
        
elif mode==2:
        NEXTPAGE(page)
        
elif mode==3:
        CATEGORIES2()
        
elif mode==4:
        Search()
        
elif mode==5:
        HIGHLIGHTS()
        
elif mode == 6 :
    HIGHLIGHTS_NEXTPAGE(page)
        
elif mode == 7 :
    HIGHLIGHTS_LINKS(name,url)
        
elif mode==200:
        PLAYSTREAM(name,url,iconimage)
        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
