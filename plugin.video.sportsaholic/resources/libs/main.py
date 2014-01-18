import urllib,urllib2,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.addon import Addon

#Sports-A-Holic - by Mash2k3 2013.

addon_id = 'plugin.video.sportsaholic'
selfAddon = xbmcaddon.Addon(id=addon_id)
mashpath = selfAddon.getAddonInfo('path')
addon = Addon(addon_id)
Dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.sportsaholic', ''))
repopath = xbmc.translatePath(os.path.join('special://home/addons/repository.mash2k3', ''))
art = 'https://github.com/mash2k3/MashupArtwork/raw/master/SAHart'
datapath = addon.get_profile()

VERSION = "1.0.4"


from universal import favorites
fav = favorites.Favorites(addon_id, sys.argv)


################################################################################ Common Calls ##########################################################################################################

def OPENURL(url):
    try:
        print "MU-Openurl = " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','').replace('&#038;','').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        return link
    except:
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000)")
        link ='website down'
        return link
        
def REDIRECT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.geturl()
        return link



def unescapes(text):
        try:            
            rep = {"&nbsp;": " ","\n": "","\t": "","\r": "","%5B": "[","%5D": "]","%3a": ":","%3A":":","%2f":"/","%2F":"/","%3f":"?","%3F":"?","%26":"&","%3d":"=","%3D":"=","%2C":",","%2c":",","%3C":"<","%20":" ","%22":'"',"%3D":"=","%3A":":","%2F":"/","%3E":">","%3B":",","%27":"'","%0D":"","%0A":""}
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text

def ErrorReport(e):
        elogo = xbmc.translatePath('special://home/addons/plugin.video.sportsaholic/icon.png')
        xbmc.executebuiltin("XBMC.Notification([COLOR red]Sports-A-Holic Error[/COLOR],"+str(e)+",10000,"+elogo+")")
        xbmc.log('***********Sports-A-Holic Error: '+str(e)+'**************')
################################################################################ AutoView ##########################################################################################################


def VIEWSB():
        if selfAddon.getSetting("auto-view") == "true":
                        if selfAddon.getSetting("home-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("home-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(500)")

                        return

############################################################################### Playback resume #################################################################################
def WatchedCallback():
        addon.log('Video completely watched.')
    
################################################################################ Google Analytics ##########################################################################################################

       
def GA(group,name):#GA has been removed
    pass


################################################################################ Types of Directories ##########################################################################################################
    
def addDirMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        script1=Dir+'/resources/addFavsMs.py'
        script2=Dir+'/resources/delFavsMs.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='Sports Favs', section_addon_title="Sports Favs", sub_section_title='Sports', img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Sports Favs', section_addon_title="Sports Favs", sub_section_title='Sports'))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,plot,type)]
        script1=Dir+'/resources/addFavsMs.py'
        script2=Dir+'/resources/delFavsMs.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='Sports Favs', section_addon_title="Sports Favs", sub_section_title='Sports', img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Sports Favs', section_addon_title="Sports Favs", sub_section_title='Sports'))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok



def addPlayc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems=[]
        if iconimage==None:
            iconimage=''
        if plot==None:
            plot=''
        if fanart==None:
            fanart=''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
    
def addDirb(name,url,mode,iconimage,fan):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addDir2(name,url,mode,iconimage,plot):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&plot="+str(plot)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Favorites",'XBMC.Container.Update(%s?name=None&mode=650&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

