import urllib,urllib2, re, xbmc, xbmcplugin, xbmcgui, xbmcaddon, os, xbmcvfs, time
import base64
addonID = 'plugin.video.tv-release'


try:
    try:import urlresolver
    except: raise Exception ('Module Urlresolver Not Found')
    try:from sqlite3 import dbapi2 as database
    except: raise Exception ('Module Sqlite2 Not Found')
    try:from BeautifulSoup import BeautifulSoup
    except: raise Exception ('Module BeautifulSoup Not Found')
    try:from addon.common.net import Net as net
    except: raise Exception ('Module Addon Common Net Not Found')
    try:from t0mm0.common.addon import Addon
    except:from addon.common.addon import Addon
    try:from metahandler import metahandlers
    except: raise Exception ('Module Metahandler  Not Found')
    try:from universal import playbackengine
    except: raise Exception ('Module Universal  Not Found')
except Exception, e:
    xbmc.log('ERROR TV-Release:- '+str(e))
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR red]Failed To Find Needed Modules[/COLOR]','[COLOR red][B]'+str(e)+'[/COLOR][/B]',
              'Please Goto [COLOR green][B]XBMCTALK.COM[/COLOR][/B] For Support')
    sys.exit(0)

local = xbmcaddon.Addon(id=addonID)
Addon = Addon(addonID, sys.argv)
grab = metahandlers.MetaData()
art = xbmc.translatePath(os.path.join( local.getAddonInfo('path'), 'resources', 'art' ))


#DB TABLE Thanks to Voinage for the insperation for this
db_dir = os.path.join(xbmc.translatePath("special://database"), 'tvrelease.db')
if not xbmcvfs.exists(os.path.dirname(db_dir)):
    xbmcvfs.mkdirs(os.path.dirname(db_dir))
db = database.connect(db_dir)
db.execute('CREATE TABLE IF NOT EXISTS url_cache (name UNIQUE, url UNIQUE)')#A_Z is the Table name and unique allows you to select and search for it, any of them an be unique 
db.commit()
db.close()

def get(name, url):
    db = database.connect( db_dir )
    cur = db.cursor()
    now = time.time()
    cur.execute('SELECT * FROM url_cache WHERE url = "%s"' %url)
    cached = cur.fetchone()
    if cached:
        db.close()
        return cached
    else:
        xbmc.log('No cached response. Requesting from internet')
        try: data = net().http_GET(url).content
        except:pass
        sql = 'INSERT OR REPLACE INTO url_cache (name, url) VALUES(?,?)'
        cur.execute(sql, (name, url))
        db.commit()
        db.close()
        return name, url

def MAIN():#addDir(mode, url, metaname, types, name, img, totalitems, folder):
    addDir(1, 'url', '', '', 'TV Shows', '', 0, True)
    addDir(200, 'url', '', '', 'Search', '', 0, True)
    addDir(2, 'url', '', '', '[COLOR blue][B]Resolver Settings[/COLOR][/B]', '', 0, '')

def TvShows():
    addDir(100, 'http://tv-release.net/?cat=TV-480p', '',    None,
           'TV Shows 480p[COLOR red][B]*HD*[/COLOR][/B]', '', 0, True)
    addDir(100, 'http://tv-release.net/?cat=TV-720p', '',    None,
           'TV Shows 720p[COLOR red][B]*HD*[/COLOR][/B]', '', 0, True)
    addDir(100, 'http://tv-release.net/?cat=TV-Mp4', '',     None,
           'TV Shows MP4[COLOR red][B]*HD*[/COLOR][/B]', '', 0, True)
    #addDir(100, 'http://tv-release.net/category/tvshows/tvdvdrip/', '',  None,
    #       'TV Shows DvdRip', '', 0, True)
    addDir(100, 'http://tv-release.net/?cat=TV-XviD', '',    None,
           'TV Shows Xvid[COLOR red][B]*HD*[/COLOR][/B]', '', 0, True)
    addDir(100, 'http://tv-release.net/?cat=TV-Foreign', '',None,
           'TV Shows Foreign', '', 0, True)
    
    
def Index(url, types):
    if 'aHR0' in url:
        url = base64.b64decode(url)
        Referer = url
    else:
        Referer = ''
        
    try:
        headers = {}
        headers['Referer'] = Referer
        soup = BeautifulSoup(net().http_GET(url, headers = headers).content)
        r = re.findall('Tv-Release.Net .. We\'ll Be Back', str(soup), re.I)
        if r:
            e = 'TV- Release is Down For Maintenance'.title()
            HTMLERROR(e)
            
    except Exception, e:
        HTMLERROR(e)
    pattern = 'a href=\"(\d+\/.+?)\"\>(.+?)\<\/a\>'
    r = re.findall(r''+pattern+'', str(soup), re.I|re.DOTALL)
    totalitems = len(r)
    for url, Tname in r:
        name = getName(Tname)
        addDir(150, 'http://tv-release.net/'+url, name, 'episode', name, '', totalitems, True)
    r = re.findall('zmg_pn_current\">(\d+)</span', str(soup), re.I)
    if r:
        currentP = r[0]
        r = re.findall('zmg_pn_current\">'+currentP+'</span><span class=\"zmg_pn_standar\"><a href=\"(.+?)\">\d+</a>',
                       str(soup), re.I|re.DOTALL)
        try:
            url = base64.b64encode('http://tv-release.net/'+r[0].replace('amp;', '').replace(' ', '%20'))
        except:
            pass
        addDir(100, url, '', '', '[COLOR orange][B]Next Page >>>[/COLOR][/B]', '', 0, True)

                    
    setView('episodes', 'episode')


def Search():
    last_search = Addon.load_data('search')
    if not last_search: last_search = ''
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, '[B][I] SEARCH TV-REALEASE.NET TVShows[/B][/I]')
    last_search = last_search.replace('%20',' ')
    keyboard.setDefault(last_search)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','%20')# sometimes you need to replace spaces with + or %20#
        Addon.save_data('search',search_entered)
    if search_entered == None or len(search_entered)<1:
        MAIN()
    else:
        url = base64.b64encode('http://www.tv-release.net/?s='+search_entered+'&cat=')
        Index(url, '')
    

def getName(Tname):
    r = re.findall('\s\d+p\s', Tname)
    if r:
        name = re.split('\s\d+p\s', Tname)[0]
    else: name = Tname

    return name
        


def FindHosts(url, name):
    print url
    EpName = name
    sources = []
    try:
        soup = BeautifulSoup(net().http_GET(url).content)
    except Exception, e:
        HTMLERROR(e)

    print str(soup)

    pattern = 'blank\"\shref=\"(.+?)\"\>'
    
    r = re.findall(r''+pattern+'', str(soup), re.I|re.DOTALL)

    print r
    for hoster in r[:-1]:
        name = re.findall('//(.+?)/', hoster)[0]
        name = name.replace('www.','')
        hosted_media = urlresolver.HostedMediaFile(url=hoster, title=name)
        sources.append(hosted_media)
    source = urlresolver.choose_source(sources)
    if source:
        try:
            stream_url = source.resolve()
            liz=xbmcgui.ListItem(EpName, iconImage='',thumbnailImage='')
            liz.setInfo('Video', {'Title': EpName} )
            liz.setProperty("IsPlayable","true")
            liz.setPath(stream_url)
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addonID, video_type='', title=EpName.title(),
                                                            season='', episode='', year='', watch_percent=0.9, watchedCallback='',
                                                            watchedCallbackwithParams=None, imdb_id=None, img='', fanart='', infolabels='')
            player.KeepAlive()
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=stream_url,isFolder=False,listitem=liz)
        except:
            pass
            
    
        

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if local.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % local.getSetting(viewType) )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )


def HTMLERROR(e):
    xbmc.log('ERROR TV-Release:- '+str(e))
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR red]ERROR INFORMATION[/COLOR]','[COLOR red][B]'+str(e)+'[/COLOR][/B]',
              'Please Try Again Later')
    sys.exit(0)

        
    
def GRABMETA(metaname, types):
    type = types
    #meta == ''
    if re.findall('\sCA\s', str(metaname)):
        mataname = metaname.replace('CA', '(CA)')
    if type == 'episode':
        r = re.findall(r'(.+?)\sS(\d+)E(\d+)', str(metaname), re.I)
        if r:
            for name, season, episode in r:
                t = grab.get_meta('tvshow', name, '', '', '', overlay=6)
                meta = grab.get_episode_meta(name, t['imdb_id'],str(season),str(episode),air_date='', episode_title='', overlay='')
                if meta['cover_url'] == '':
                    meta['cover_url'] = t['cover_url']
        if not r:
            r = re.findall(r'(.+?)\s(\d+)\s(\d+)\s(\d+)', str(metaname), re.I)
            if r:
                for name, year, month, date in r:
                    t = grab.get_meta('tvshow', name, '', '', '', overlay=6)
                    meta = grab.get_episode_meta(name, t['imdb_id'],0,'',str(year)+'-'+str(month)+'-'+str(date), episode_title='', overlay='')
            else:meta = {'cover_url': '','title': metaname}
    #if meta == '':meta = {'cover_url': '','title': metaname}
    return meta              
    


def addDir(mode, url, metaname, types, name, iconimage, totalitems, folder):
    u  = sys.argv[0]
    u += "?mode="       + str(mode)
    u += "&url="        + str(url)
    u += "&metaname="   + str(metaname)
    u += "&types="      + str(types)
    u += "&name="       + str(name)
    u += "&img="        + str(iconimage)
    u += "&totalitems=" + str(totalitems)
    u += "&folder="     + str(folder)

    ok=True
    if local.getSetting("usemeta") == "true" and metaname != '':
        infoLabels = GRABMETA(metaname,types)
    else:
        infoLabels = {'cover_url': "", 'title': name}
    if types == None: img = iconimage
    else: img = infoLabels['cover_url']
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
    try:
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        liz.setInfo( type="Video", infoLabels = infoLabels )
    except: pass
    if folder == True:ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=int(totalitems))
    elif folder == False:xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u, isFolder=False, listitem=liz)
    #return ok

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

params     = get_params()
mode       = None
url        = None
metaname   = None
types      = None
name       = None
iconimage  = None
totalitems = None
folder     = None

try: mode = int(params['mode'])
except:pass
try: url = urllib.unquote_plus(params["url"])
except:pass
try: metaname = urllib.unquote_plus(params["metaname"])
except:pass
try: types = urllib.unquote_plus(params["types"])
except:pass
try: name = urllib.unquote_plus(params["name"])
except:pass
try: iconimage = urllib.unquote_plus(params["iconimage"])
except:pass
try:totalitems = int(params["totalitems"])
except:pass
try: folder = urllib.unquote_plus(params["folder"])
except:pass

xbmc.log('Mode: '+str(mode))
xbmc.log('Url: '+str(url))
xbmc.log('Metaname: '+str(metaname))
xbmc.log('Types: '+str(types))
xbmc.log('Name: '+str(name))
xbmc.log('Iconimage: '+str(iconimage))
xbmc.log('Folder: '+str(folder))

if mode == None or url == None or len(url)<1:
    MAIN()

elif mode == 1:TvShows()
elif mode == 2: urlresolver.display_settings()
elif mode == 100:Index(url, types)
elif mode == 150:FindHosts(url, name)
elif mode == 200:Search()
    




xbmcplugin.endOfDirectory(int(sys.argv[1]),succeeded=True)
