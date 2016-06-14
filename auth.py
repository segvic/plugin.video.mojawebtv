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

          dict_name_value_pairs = {
            "u"   : username,
            "p"   : password,
            "x" : "1"
          }
          url = 'https://www.bhtelecom.ba/index.php?id=6905&'+ urllib.urlencode(dict_name_value_pairs)
          src = download_page(url)
          resp = json.loads(src)
          auth  = resp['auth']
         # xbmc.log(resp)
          return auth
          #xbmcgui.Dialog().ok("dooing","auth "+str(pluginhandle)+" "+username)



