#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc, xbmcaddon, xbmcgui
import xbmcplugin
import os
import json
import urllib
import sys, time
from xbmcswift import Plugin, download_page, xbmc, xbmcgui

def doAuth(username, password):
        try:
          dict_name_value_pairs = {
            "u"   : username,
            "p"   : password,
            "x" : "1"
          }
          url = 'https://www.bhtelecom.ba/index.php?id=5363&'+ urllib.urlencode(dict_name_value_pairs)
          src = download_page(url)
          resp = json.loads(src)
          auth  = resp['auth']
          #xbmc.log(resp)
          #xbmcgui.Dialog().ok("dooing","auth "+str(pluginhandle))
          if auth == 0:
            xbmcgui.Dialog().ok("Autorizacija nije uspješna","Niste unijeli korisničke podatke ili uneseni podaci nisu tačni.\n Nakon što kliknete OK otvoriće Vam se postavke te je neophodno da unesete ispravno korisničko ime i lozinku za Moja webTV servis ")
            xbmcaddon.Addon(id='plugin.video.mojawebtv').openSettings()
        except:
           xbmcgui.Dialog().ok("Autorizacija nije uspješna","Autorizacija nije moguća\nProvjerite da li ste spojeni na Internet pa pokušajte ponovo ")


