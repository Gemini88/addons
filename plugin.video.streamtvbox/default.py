import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
from t0mm0.common.net import Net
from threading import Timer

import tvguide

PLUGIN='plugin.video.streamtvbox'
ADDON = xbmcaddon.Addon(id=PLUGIN)
deletepy = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'),ADDON.getSetting('delete')))
image='http://www.xunitytalk.com/oss/'

auth=ADDON.getSetting('authtoken')
forOffset=tvguide.offset_time()
forOffset_gmt=tvguide.offset_gmt()
USER='[COLOR yellow]'+ADDON.getSetting('user')+'[/COLOR]'
updateid= int(ADDON.getSetting('id'))


net=Net()


def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    
    
if ADDON.getSetting('user')=='':
    dialog = xbmcgui.Dialog()
    if dialog.yesno("StreamTVBox", "If You Dont Have An Account", "Please Sign Up At","WWW.STREAMTVBOX.COM","Exit","Carry On"):
        
        dialog.ok("StreamTVBox", "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, "StreamTVBox")
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('user',search_entered)
        
        dialog.ok("StreamTVBox", "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, "StreamTVBox")
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('pass',search_entered)
        ADDON.setSetting('login_time','2000-01-01 00:00:00')
    else:
        EXIT()
    
    
site='http://streamtvbox.com/site/live-tv/'


datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "streamtvbox_new.lwp")
channeljs=os.path.join(cookie_path, "channel.js")




def LOGOUT():
    net.set_cookies(cookie_jar)
    html = net.http_GET(site).content
    match=re.compile('  href="(.+?)">Log Out</a>').findall(html)[0]
    net.set_cookies(cookie_jar)
    logout = net.http_GET(match.replace('#038;','')).content
    if 'You are now logged out' in logout:
        print '===============LOGGED OUT !!==============='
        dialog = xbmcgui.Dialog()
        dialog.ok("StreamTVBox",'', "You Are Now Logged Out", "")
        EXIT()
        
        
    
def LOGIN():
    print '###############    LOGIN TO STVB   #####################'
    loginurl = 'http://streamtvbox.com/site/wp-login.php'
    username = ADDON.getSetting('user')
    password = ADDON.getSetting('pass')
    
    data     = {'pwd': password,
                                            'log': username,
                                            'wp-submit': 'Log In','redirect_to':'http://streamtvbox.com/site','testcookie':'1'}
    headers  = {'Host':'streamtvbox.com',
                                            'Origin':'http://streamtvbox.com',
                                            'Referer':'http://streamtvbox.com/site/wp-login.php',
                                                    'X-Requested-With':'XMLHttpRequest'}
    html = net.http_POST(loginurl, data, headers).content
    if 'account is already logged in using another ip address' in html:
        KICKOUT()
        return
        
    if os.path.exists(cookie_path) == False:
            os.makedirs(cookie_path)
    net.save_cookies(cookie_jar)
	
	
        
def KICKOUT():
        dialog = xbmcgui.Dialog()
        dialog.ok("Multiple Logins Using "+USER+" Account", "Please Do Not Share Your Account Details If You Do Not", "Have An Account Please Sign Up To ", "[COLOR yellow]WWW.STREAMTVBOX.COM[/COLOR]")
        EXIT()
        ADDON.setSetting('user','')
        ADDON.setSetting('pass','')
        ADDON.setSetting('authtoken','')
        ADDON.setSetting('login_time', '2000-01-01 00:00:00')
        return
    
def GRAB_AUTH():
    print '###############     GRAB AUTH     #####################'
    net.set_cookies(cookie_jar)
  
    html = net.http_GET(site).content
    
    if 'account is already logged in using another ip address' in html:
        KICKOUT()
        return
    var  = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
    ADDON.setSetting('authtoken',var[0])
    now = datetime.datetime.today()
    ADDON.setSetting('login_time', str(now).split('.')[0])
    
def downloadchannel():
    if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
    
	
    import downloader
    dp = xbmcgui.DialogProgress()
    dp.create("Grabbing Channel List","Downloading ",'', 'Please Wait')
    downloader.download('http://offsidestreams.com/site/nl-channels.js', channeljs, dp)

    
def server():
    if os.path.exists(cookie_path) == False:
            os.makedirs(cookie_path)
    if os.path.exists(channeljs) == False:
        downloadchannel()
    try:
        a=open(channeljs).read()
    except:
        a=OPEN_URL('http://offsidestreams.com/site/nl-channels.js')      
    return a

def CheckChannels():
    update=OPEN_URL('http://mikey1234-repo.googlecode.com/svn/addons/plugin.video.offside/update.txt')
    id=re.compile('id<(.+?)>').findall(update)[0]
    if int(id) > updateid:
        notification=re.compile('<NOT>(.+?)</NOT>.+?line1>(.+?)</line1.+?line2>(.+?)</line2.+?line3>(.+?)</line3>',re.DOTALL).findall(update)
        for show,line1,line2,line3 in notification:
            if '%s' in line1:
                line1=line1%USER
            if '%s' in line2:    
                line2=line2%USER
            if '%s' in line3:    
                line3=line3%USER
            if show=='yes':
                dialog = xbmcgui.Dialog()
                dialog.ok("StreamTVBox", line1, line2,line3)
            if 'Download' in line3:
                downloadchannel()
        ADDON.setSetting('id',id)
    
def CATEGORIES():
    CheckChannels()
    addDir('[COLOR red].Full Match Replays HD[/COLOR]','url',3,'','','','')
    link = server()
    link = link.split('window.channels =')[1]
    match = re.findall('"title": "(.+?)".+?"file": "(.+?)",',link,re.M|re.DOTALL)
    for _name,url in match:
        iconimage=image+_name.replace(' ','').replace('-Free','').replace('HD','').replace('i/H','i-H').replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','').lower()+'.png'
        if ADDON.getSetting('tvguide')=='true':
            try:
                name=_name+'[COLOR yellow]%s[/COLOR]'% tvguide.tvguide(_name)
            except:
                name=_name
        else:
            if tvguide.return_url(_name):
                name=_name+'[COLOR yellow] (G)[/COLOR]'
            else:
                name=_name
        if ADDON.getSetting('hd')=='true':
            if 'HD' in name:
                addDir(name,url,2,iconimage,'False','',_name)
        else:
            addDir(name,url,2,iconimage,'False','',_name)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
        
        
        
        
def month(name):
    if 'Jan' in name:
        return '01'
    elif 'Feb' in name:
        return '02'
    elif 'Mar' in name:
        return '03'
    elif 'Apr' in name:
        return '04'
    elif 'May' in name:
        return '05'
    elif 'Jun' in name:
        return '06'
    elif 'Jul'in name:
        return '07'
    elif 'Aug' in name:
        return '08'
    elif 'Sep' in name:
        return '09'
    elif 'Oct' in name:
        return '10'
    elif 'Nov' in name:
        return '11'
    elif 'Dec' in name:
        return '12'
        
def _ret_time(start):
    start = getTime(start)

    return start.strftime('%d-%m-%Y')
        
        
def schedule(name,url,iconimage):

    if 'color' in name:
         For_Name=name.split('[color')[0]
         
    else:
         For_Name=name
         
    if 'jsc' in For_Name:
        url    =  'http://www.en.aljazeerasport.tv/fragment/aljazeera/fragments/components/ajax/channelList/channel/plus%s/maxRecords/0'%(For_Name.split('  ')[1])
          
        link   =  OPEN_URL(url).replace('\n','').replace('  ','')
        link   =  link.split('<h')[1]
        _date  =  re.compile('>(.+?) (.+?) (.+?)<span class="arrow">',re.DOTALL).findall(link)
        day    =  _date[0][0]
        _month =  month(_date[0][1])
        year   =  _date[0][2]
        
        
        if '+' in forOffset:
            Z= forOffset.split('+')[1]
        elif '-' in forOffset:
            Z= forOffset.split('-')[1]
        else :
            Z= '0'
        print Z
        pattern='<td class="eventsCell hardAlign">(.+?)</td.+?<td class="category">(.+?)</td>.+?<td class="startTime">(.+?):(.+?)</td>'
        match = re.compile(pattern,re.DOTALL).findall(link)
        for game,league,hour,minute in match:
        
            if '+' in forOffset:
            
                t   =   datetime.datetime(int(year), int(_month) , int(day), int(hour), int(minute), 00)
                t  +=   datetime.timedelta(hours = int(Z))
                
            if '-' in forOffset:
            
                t   =   datetime.datetime(int(year), int(_month) , int(day), int(hour), int(minute), 00)
                t  -=   datetime.timedelta(hours = int(Z))
                
            else:
                t  =    datetime.datetime(int(year), int(_month) , int(day), int(hour), int(minute), 00)
                
                
                
            game_league=game+' ('+league+')'
            _name_='[COLOR white][%s]-[/COLOR][COLOR yellow][B]%s[/B][/COLOR]'%(t.strftime('%H:%M'),game_league)
            addDir(_name_,'url',2,iconimage.replace(' ','+'),'True','','JSC +'+For_Name.split('  ')[1])

    else:
        try:
	        url=tvguide.return_url(name.title())
	        link=OPEN_URL(url)
	        _date  =  re.compile('<!-- produced for the bleb.org TV system at .+? (.+?) (.+?) .+? (.+?) -->', re.M|re.DOTALL).findall(link)
	        day    =  _date[0][1]
	        _month =  month(_date[0][0])
	        year   =  _date[0][2]
	        
	        match=re.findall('<title>(.+?)</title>.+?<start>(.+?)</start>',link,re.M|re.DOTALL)
	        for _name,start in match:
	            hour=start[0:2]
	            minute=start[2:4]
	            if '+' in forOffset_gmt:
	                Z   =   forOffset_gmt.split('+')[1]
	                t   =   datetime.datetime(int(year), int(_month) , int(day), int(hour), int(minute), 00)+ datetime.timedelta(hours = int(Z))
	                time  =    t.strftime('%H:%M')
	                
	            elif '-' in forOffset_gmt:
	                Z= forOffset_gmt.split('-')[1]
	                t   =   datetime.datetime(int(year), int(_month) , int(day), int(hour), int(minute), 00)- datetime.timedelta(hours = int(Z))
	                time  =    t.strftime('%H:%M')
	            else:
	                time  =   '%s:%s'%(hour,minute)
	            
	            name_='[COLOR white][%s][/COLOR]-[COLOR yellow][B]%s[/B][/COLOR]'%(time,_name)
	            addDir(name_,url,2,iconimage,'True','',For_Name.title())
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("StreamTVBox", '',"Sorry No Schedule Found", "")
            xbmc.executebuiltin('XBMC.Container.Update(%s?mode=None&url=None,replace)'%sys.argv[0])
 
def Show_Dialog():
    dialog = xbmcgui.Dialog()
    dialog.ok("StreamTVBox", '',"All Done Try Now", "")
        
def REPLAY():
        ok=True
        cmd = 'plugin://plugin.video.footballreplays/'
        xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)
        return ok
 
        
 
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
        
        
        
        
    
        
        
def Grab_Day(date):
    year, month, day = (int(x) for x in date.split('-'))    
    ans=datetime.date(year,month,day)
    return (ans.strftime("%a"))


def parse_date(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 365)


def sessionExpired(hour_threshold=3):
    secsInHour = 60 * 60
    threshold  = hour_threshold * secsInHour
    now        = datetime.datetime.today()
    
    prev = ADDON.getSetting('login_time')
    if not prev or prev == '':
        prev = '2000-01-01 00:00:00'
    prev  = parse_date(prev)
    
    delta = now - prev
    nSecs = delta.seconds + (86400*delta.days)

    return (nSecs > threshold)
    
    

def SetResolvedURL(rtmp):
    if sessionExpired() or ADDON.getSetting('authtoken')=='':
        print '###############   AUTH  EXPIRED    #####################'
        LOGIN()
        GRAB_AUTH()
    else:
        print '###############   AUTH  IN DATE   #####################'

    
    rtmp=rtmp.replace('"','').replace(' ','').replace('+','')

    stream_url = '%s swfUrl=http://p.jwpcdn.com/6/7/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10' % (rtmp.replace('urlkey1', auth), auth, site)

    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        
        
def PLAY_STREAM(name, url, iconimage, play, description):
    if play == 'True':
        desc = description.replace('%20',' ').replace('i-H','i/H').replace('  ',' +')

        link = OPEN_URL(server())
        link = link.split('"title": "')
        r    = '"file": "(.+?)",'

        for p in link:
            if desc in p:
                match = re.findall(r,p,re.M|re.DOTALL)
                rtmp  = match[0]
                SetResolvedURL(rtmp)
                return
    else:
        SetResolvedURL(url)
        

        
    
            
        
        
        
    
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

def addDir(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        #print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+u
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        menu=[]
        menu.append(('[COLOR green]Download Channel List[/COLOR]','XBMC.RunPlugin(%s?mode=204&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        menu.append(('[COLOR yellow]Schedule[/COLOR]','XBMC.Container.Update(%s?mode=200&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        menu.append(('[COLOR orange]Grab AuthToken[/COLOR]','XBMC.RunPlugin(%s?mode=202&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        menu.append(('[COLOR red]Delete Cookie[/COLOR]','XBMC.RunPlugin(%s?mode=203&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        menu.append(('[COLOR cyan]Log Out[/COLOR]','XBMC.RunPlugin(%s?mode=205&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        if mode == 2:
            liz.setProperty("IsPlayable","true")
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
date=None
description=None
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
        play=urllib.unquote_plus(params["play"])
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()
               
elif mode==2:
        PLAY_STREAM(name,url,iconimage,play,description)
        
elif mode==3:
        REPLAY()
        
elif mode==200:
        schedule(name,url,iconimage)
        
elif mode==201:
        fullguide(name,url,iconimage,description)
        
elif mode==202:
        LOGIN()
        try:GRAB_AUTH()
        except:pass
        Show_Dialog()
        
elif mode==203:
        os.remove(cookie_jar)
        Show_Dialog()
    
elif mode==204:
        downloadchannel()     
        
elif mode==205:
        LOGOUT()        
           
            
elif mode==2001:
        ADDON.openSettings()

else:
        #just in case mode is invalid 
        CATEGORIES()

try:xbmcplugin.endOfDirectory(int(sys.argv[1]))
except:pass

