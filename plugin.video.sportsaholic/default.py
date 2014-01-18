#-*- coding: utf-8 -*-
import urllib,re
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net

try:
        from xbmcads import ads
except:
        pass
from resources.libs import main


#Sports-A-Holic - by Mash2k3 2013.

addon_id = 'plugin.video.sportsaholic'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
ads.ADDON_ADVERTISE(addon_id)
from universal import watchhistory
wh = watchhistory.WatchHistory('plugin.video.sportsaholic')

art = main.art

################################################################################ Source Imports ##########################################################################################################



################################################################################ Directories ##########################################################################################################


def MAIN():
        main.addDir("My Favorites",'Favorites',650,art+'/fav.png')
        main.addDir('Watch History','history',222,art+'/whistory.png')
        main.addDir('ESPN','http:/espn.com',44,art+'/espn.png')
        main.addDir('TSN','http:/tsn.com',95,art+'/tsn.png')
        main.addDir('SkySports.com','www1.skysports.com',172,art+'/skysports.png')
        main.addDir('Fox Soccer  [COLOR red](US ONLY)[/COLOR]','http:/tsn.com',124,art+'/foxsoc.png')
        main.addDir('All MMA','mma',537,art+'/mma.png')
        main.addDir('Outdoor Channel','http://outdoorchannel.com/',50,art+'/OC.png')
        main.addDir('Wild TV','https://www.wildtv.ca/shows',92,art+'/wildtv.png')
        main.addDir('Workouts','https://www.wildtv.ca/shows',194,art+'/workout.png')
        main.addDir('The Golf Channel','golf',217,art+'/golfchannel.png')
        link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/Sport_Directory.xml')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('type=playlistname=Sorted by user-assigned order','').replace('name=Sorted [COLOR=FF00FF00]by user-assigned order[/COLOR]','').replace('name=Live Tv Channels Twothumb','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)
        main.addPlayc('Need Help?','http://www.movie25.com/',100,art+'/xbmchub.png','','','','','')
        main.VIEWSB()


def MMA():
        main.addDir('UFC','ufc',47,art+'/ufc.png')
        main.addDir('Bellator','BellatorMMA',47,art+'/bellator.png')
        main.addDir('MMA Fighting.com','http://www.mmafighting.com/videos',113,art+'/mmafig.png')
        main.GA("None","MMA")

def WorkoutMenu():
        main.addDir('Fitness Blender[COLOR red](Full Workouts)[/COLOR]','fb',198,art+'/fitnessblender.png')
        main.addDir('Body Building[COLOR red](Instructional Only)[/COLOR]','bb',195,art+'/bodybuilding.png')
        main.GA("None","Workout")





################################################################################ XBMCHUB POPUP ##########################################################################################################


class HUB( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/theme.mp3'%selfAddon.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()
        if controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        import time
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        
def pop():
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup

################################################################################ Favorites Function##############################################################################################################




def ListglobalFavMs():
        from universal import favorites
        fav = favorites.Favorites(addon_id, sys.argv)
        
        fav_items = fav.get_my_favorites(section_title="Sports Favs", item_mode='addon')
        
        if len(fav_items) > 0 :
        
            for fav_item in fav_items:
                if (fav_item['isfolder'] == 'false'):
                    main.addPlayMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                else:
                    main.addDirMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR white]Sports-A-Holic[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')


################################################################################ Histroy ##########################################################################################################

def History():
    main.GA("None","WatchHistory")
    if selfAddon.getSetting("whistory") == "true":
        history_items = wh.get_my_watch_history()
        for item in history_items:
                item_title = item['title']
                item_url = item['url']
                item_image = item['image_url']
                item_fanart = item['fanart_url']
                item_infolabels = item['infolabels']
                item_isfolder = item['isfolder']
                if item_image =='':
                    item_image= art+'/noimage.png'
                main.addLink(item_title,item_url,item_image)
    else:
        dialog = xbmcgui.Dialog()
        ok=dialog.ok('[B]MashUp History[/B]', 'Watch history is disabled' ,'To enable go to addon settings','and enable Watch History')
        history_items = wh.get_my_watch_history()
        for item in history_items:
                item_title = item['title']
                item_url = item['url']
                item_image = item['image_url']
                item_fanart = item['fanart_url']
                item_infolabels = item['infolabels']
                item_isfolder = item['isfolder']
                main.addLink(item_title,item_url,item_image)
        


################################################################################ Modes ##########################################################################################################


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
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None




try:
        name=urllib.unquote_plus(params["name"])
except:
        pass

try:
        
        url=urllib.unquote_plus(params["url"])
        
except:
        pass

try:
        mode=int(params["mode"])
except:
        pass

try:
        iconimage=urllib.unquote_plus(params["iconimage"])
        iconimage = iconimage.replace(' ','%20')
except:
        pass
try:
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
        fanart = fanart.replace(' ','%20')
except:
        pass

try:
        genre=urllib.unquote_plus(params["genre"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
        print ""
        MAIN()     
        
elif mode==43:
        print ""+url
        SPORTS()

elif mode==44:
        from resources.libs.sports import espn
        print ""+url
        espn.ESPN()
        
elif mode==45:
        from resources.libs.sports import espn
        print ""+url
        espn.ESPNList(url)

elif mode==46:
        from resources.libs.sports import espn
        print ""+url
        espn.ESPNLink(name,url,iconimage,plot)

elif mode==47:
        from resources.libs import youtube
        print ""+url
        youtube.YOUList(name,url)
        
elif mode==48:
        from resources.libs import youtube
        print ""+url
        youtube.YOULink(name,url,iconimage)

elif mode==50:
        from resources.libs.sports import outdoorch
        print ""+url
        outdoorch.OC()
        
elif mode==51:
        from resources.libs.sports import outdoorch
        print ""+url
        outdoorch.OCList(url)

elif mode==52:
        from resources.libs.sports import outdoorch
        print ""+url
        outdoorch.OCLink(name,url,iconimage)
        
elif mode==59:
        print ""+url
        UFC()
        
elif mode==92:
        from resources.libs.sports import wildtv
        print ""+url
        wildtv.WILDTV(url)        

elif mode==93:
        from resources.libs.sports import wildtv
        print ""+url
        wildtv.LISTWT(url)
        
elif mode==94:
        from resources.libs.sports import wildtv
        print ""+url
        wildtv.LINKWT(name,url)

elif mode==95:
        from resources.libs.sports import tsn
        print ""+url
        tsn.TSNDIR()

elif mode==96:
        from resources.libs.sports import tsn
        print ""+url
        tsn.TSNDIRLIST(url)        

elif mode==97:
        from resources.libs.sports import tsn
        print ""+url
        tsn.TSNLIST(url)
        
elif mode==98:
        from resources.libs.sports import tsn
        print ""+url
        tsn.TSNLINK(name,url,iconimage)
        
elif mode==100:
        pop()

elif mode==113:
        from resources.libs.sports import mmafighting
        mmafighting.MMAFList(url)

elif mode==114:
        from resources.libs.sports import mmafighting
        mmafighting.MMAFLink(name,url,iconimage)   


elif mode==124:
        from resources.libs.sports import foxsoccer
        print ""+url
        foxsoccer.FOXSOC()
elif mode==125:
        from resources.libs.sports import foxsoccer
        print ""+url
        foxsoccer.FOXSOCList(url)
elif mode==126:
        from resources.libs.sports import foxsoccer
        print ""+url
        foxsoccer.FOXSOCLink(name,url)


elif mode==172:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTS()

elif mode==173:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSList(url)

elif mode==174:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSLink(name,url)

elif mode==175:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSTV(url)

elif mode==176:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSList2(url)
        
elif mode==177:
        dialog = xbmcgui.Dialog()
        dialog.ok("Mash Up", "Sorry this video requires a SkySports Suscription.","Will add this feature in later Version.","Enjoy the rest of the videos ;).")

elif mode==178:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSCAT()

elif mode==179:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSCAT2(url)

elif mode==180:
        from resources.libs.sports import skysports
        print ""+url
        skysports.SKYSPORTSTEAMS(url)

elif mode==181:
        from resources.libs.live import  vipplaylist
        print ""+url
        vipplaylist.VIPplaylists(url)

elif mode==182:
        from resources.libs.live import  vipplaylist
        print ""+url
        vipplaylist.VIPList(name,url)

elif mode==183:
        from resources.libs.live import  vipplaylist
        print ""+url
        vipplaylist.VIPLink(name,url,iconimage)

elif mode==194:
        print ""+url
        WorkoutMenu()

elif mode==195:
        from resources.libs.sports import bodybuilding
        print ""+url
        bodybuilding.MAINBB()

elif mode==196:
        from resources.libs.sports import bodybuilding
        print ""+url
        bodybuilding.LISTBB(url)

elif mode==197:
        from resources.libs.sports import bodybuilding
        print ""+url
        bodybuilding.LINKBB(name,url,iconimage)

elif mode==198:
        from resources.libs.sports import fitnessblender
        print ""+url
        fitnessblender.MAINFB()

elif mode==199:
        from resources.libs.sports import fitnessblender
        print ""+url
        fitnessblender.BODYFB()

elif mode==200:
        from resources.libs.sports import fitnessblender
        print ""+url
        fitnessblender.DIFFFB()

elif mode==201:
        from resources.libs.sports import fitnessblender
        print ""+url
        fitnessblender.TRAINFB()

elif mode==202:
        from resources.libs.sports import fitnessblender
        print ""+url
        fitnessblender.LISTBF(url)

elif mode==203:
        from resources.libs.sports import fitnessblender
        print ""+url
        fitnessblender.LINKBB(name,url,iconimage)

elif mode==217:
        from resources.libs.sports import golfchannel
        golfchannel.MAIN()
        
elif mode==218:
        from resources.libs.sports import golfchannel
        print ""+url
        golfchannel.LIST(url)

elif mode==219:
        from resources.libs.sports import golfchannel
        print ""+url
        golfchannel.LIST2(name,url,iconimage,plot)


elif mode==220:
        from resources.libs.sports import golfchannel
        print ""+url
        golfchannel.LINK(name,url,iconimage)

elif mode==221:
        from resources.libs.sports import golfchannel
        print ""+url
        golfchannel.LIST3(url)


elif mode==222:
        print ""+url
        History()
elif mode==235:
    from resources.libs import movieplaylist
    print ""+url
    movieplaylist.Mplaylists(url)

elif mode==236:
    from resources.libs import movieplaylist
    print ""+url
    movieplaylist.MList(name,url)

elif mode==237:
    from resources.libs import movieplaylist
    print ""+url
    movieplaylist.MLink(name,url,iconimage)
elif mode==245:
    from resources.libs import multilinkplaylist
    print ""+url
    multilinkplaylist.Mplaylists(url)

elif mode==246:
    from resources.libs import multilinkplaylist
    print ""+url
    multilinkplaylist.MList(name,url)

elif mode==247:
    from resources.libs import multilinkplaylist
    print ""+url
    multilinkplaylist.MLink(name,url,iconimage)
elif mode==249:
    from resources.libs import movieplaylist
    movieplaylist.subLink(name,url)        
elif mode==537:
        print ""+url
        MMA() 



elif mode==650:
        print ""+url
        ListglobalFavMs()
                                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
