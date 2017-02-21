#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Update for MojaTV sport
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from xbmcswift import Plugin, download_page, xbmc, xbmcgui
from BeautifulSoup import BeautifulSoup as BS
from urlparse import urljoin
import re
import xbmcplugin
import sys
import urllib
import xbmcaddon
import auth
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json


PLUGIN_NAME = 'Moja webTV'
PLUGIN_ID = 'plugin.video.mojawebtv'





pluginhandle = int(sys.argv[1])
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)
usern =  xbmcplugin.getSetting(pluginhandle, 'username')
passwd = xbmcplugin.getSetting(pluginhandle, 'password')

def parse_video(video):
    '''Returns a dict of information for a given json video object.'''
    info = {
        'title': video['epgstart']+'  '+video['epgtitle']+' ('+str(video['epgduration'])+' min)',
        'summary': video['title'],
        'videoid': video['ch'],
        'start': video['epgstart'],
        'thumbnail': 'http://webtv.bhtelecom.ba/thumbs/'+video['ch']+'.jpg?x='+datetime.now().strftime('%Y%m%d%H%M%S'),
        'logo': 'http://webtv.bhtelecom.ba/hq_logo/'+video['ch']+'.png',
        'cluster': int(video['cluster'])
    }
    return info


def parse_recs(video):
    '''Returns a dict of information for a given json video object.'''
    info = {
        'title': video['start']+'  '+video['title']+' ('+str(video['epgduration'])+' min)',
        'summary': video['title'],
        'ts': video['ts'],
        'start': video['start'],
        'now': video['now'],
        'duration': video['epgduration']

    }
    return info


def get_videos(list_id):


    '''Returns a tuple of (videos, total_videos) where videos is a list of
    dicts containing video information and total_videos is the toal number
    of videos available for the given list_id. The number of videos returned
    is specified by the given count.'''
    if list_id == 'sd':
      url  = 'http://webtv.bhtelecom.ba/channels'
    if list_id == 'cam':
      url  = 'http://webtv.bhtelecom.ba/channels_cat_4'
    if list_id == 'radio':
      url  = 'http://webtv.bhtelecom.ba/channels_cat_11'
    if list_id == 'rec':
      url = 'http://webtv.bhtelecom.ba/channels_rec'

    src = download_page(url)
    resp = json.loads(src)
    videos  = resp['feed']

    video_infos = map(parse_video, videos)
    total_results = resp
    return video_infos, total_results


def get_recordings(id):


    url  = 'http://webtv.bhtelecom.ba/epg/'+id
    #xbmcgui.Dialog().ok("EPG URL", url)
    src = download_page(url)
    resp = json.loads(src)
    recs  = resp['feed']

    video_infos = map(parse_recs, recs)
    total_results = resp
    return video_infos, total_results



@plugin.route('/', default=True)
def show_homepage():


    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
      xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
    elif skin_used == 'skin.aeon.nox':
      xbmc.executebuiltin('Container.SetViewMode(512)') # "Info-wall" view.


    if usern!='':
      items = [
        # SD Live
        {'label': plugin.get_string(30100), 'thumbnail': 'http://webtv.bhtelecom.ba/kodi/livetv.png',
         'url': plugin.url_for('show_live', label='sd')},
        # Live cam
        {'label': plugin.get_string(30101), 'thumbnail': 'http://webtv.bhtelecom.ba/kodi/cam.png',
         'url': plugin.url_for('show_live', label='cam')},
         # Radio
        {'label': plugin.get_string(30102), 'thumbnail': 'http://webtv.bhtelecom.ba/kodi/radio.png',
         'url': plugin.url_for('show_live', label='radio')},
        # Recordings
        {'label': plugin.get_string(30103), 'thumbnail': 'http://webtv.bhtelecom.ba/kodi/rec.png',
         'url': plugin.url_for('show_live', label='rec')},

      ]

    if usern=='':
      items = [
        # Live cam
        {'label': plugin.get_string(30101), 'thumbnail': 'http://webtv.bhtelecom.ba/kodi/cam.png',
         'url': plugin.url_for('show_live', label='cam')},
         # Radio
        {'label': plugin.get_string(30102), 'thumbnail': 'http://webtv.bhtelecom.ba/kodi/radio.png',
         'url': plugin.url_for('show_live', label='radio')},

      ]

    return plugin.add_items(items)



@plugin.route('/labels/<label>/')
def show_live(label):
    '''
    '''
    items = []



    url_add = ''
    server = [0,1,2,3]
    server[0] = '195.222.59.132'
    server[1] = '195.222.59.142'
    server[2] = '195.222.57.183'
    server[3] = '195.222.59.140'

    ext = [0,1,2,3]
    ext[0] = '.smil'
    ext[1] = '.smil'
    ext[2] = '.smil'
    ext[3] = '.stream'


   # if xbmcplugin.getSetting(pluginhandle, 'hq') == "true":

    # The first link for the 'Clips' section links directly to a video so we
    # must handle it differently.
    if label=='sd':

      auth_resp = auth.doAuth(usern, passwd)
      if auth_resp < 100:
          xbmcgui.Dialog().ok("Autorizacija nije uspješna","Niste unijeli korisničke podatke ili uneseni podaci nisu tačni.\n\nNakon što kliknete OK otvoriće Vam se postavke te je neophodno da unesete ispravno korisničko ime i lozinku za Moja webTV servis ")
          xbmcaddon.Addon(id='plugin.video.mojawebtv').openSettings()
      if auth_resp > 99:
        videos, total_results = get_videos('sd')
        i = 0;
        for video in videos:
          items.append({
             'label': video['summary'],
             'info': {'plot': video['start']+' '+video['title'], },
             'thumbnail': video['thumbnail'],
             'url': plugin.url_for('play_live', url='http://webtvstream.bhtelecom.ba/kodi/'+video['videoid']+'.m3u8', title=(video['title'].encode('utf8')), thumb=video['logo'], chid=video['videoid'], usern=usern, passwd=passwd),
             'is_folder': False,
             'is_playable': False,
          })


    if label=='cam':
      videos, total_results = get_videos('cam')
      i = 0;
      for video in videos:
          items.append({
            'label': video['summary'],
            'info': {'plot': video['start']+' '+video['title'], },
            'thumbnail': video['thumbnail'],
            'url': plugin.url_for('play_live', url='http://webtvstream.bhtelecom.ba/kodi/'+video['videoid']+'.m3u8', title=(video['title'].encode('utf8')), thumb=video['logo'], chid=video['videoid'], usern=usern, passwd=passwd),
            'is_folder': False,
            'is_playable': False,
          })

    if label=='radio':
      videos, total_results = get_videos('radio')
      i = 0;
      for video in videos:
        items.append({
           'label': video['summary'],
           'info': {'plot': video['start']+' '+video['title'], },
           'thumbnail': video['logo'],
           'url': plugin.url_for('play_live', url='http://webtvstream.bhtelecom.ba/kodi/'+video['videoid']+'.m3u8', title=(video['title'].encode('utf8')), thumb=video['logo'], chid=video['videoid'], usern=usern, passwd=passwd),
           'is_folder': False,
           'is_playable': False,
        })

    if label=='rec':
      auth_resp = auth.doAuth(usern, passwd)
      if auth_resp < 100:
          xbmcgui.Dialog().ok("Autorizacija nije uspješna","Niste unijeli korisničke podatke ili uneseni podaci nisu tačni.\n\nNakon što kliknete OK otvoriće Vam se postavke te je neophodno da unesete ispravno korisničko ime i lozinku za Moja webTV servis ")
          xbmcaddon.Addon(id='plugin.video.mojawebtv').openSettings()
      if auth_resp > 99:
        videos, total_results = get_videos('rec')
        for video in videos:
          items.append({
            'label': video['summary'],
            'thumbnail': video['logo'],
            'info': {'plot': video['summary'], },
            'url': plugin.url_for('get_epg', ch=video['videoid']),
            'is_folder': True,
            'is_playable': False,
          })


    return plugin.add_items(items)


@plugin.route('/live/<url>/<title>/<thumb>/<chid>/<usern>/<passwd>/')
def play_live(url, title, thumb, chid, usern, passwd):

    if usern!='':
      auth_resp = auth.doAuth(usern, passwd)
      if auth_resp < 100:
        xbmcgui.Dialog().ok("Autorizacija nije uspješna","Niste unijeli korisničke podatke ili uneseni podaci nisu tačni.\n\nNakon što kliknete OK otvoriće Vam se postavke te je neophodno da unesete ispravno korisničko ime i lozinku za Moja webTV servis ")
        xbmcaddon.Addon(id='plugin.video.mojawebtv').openSettings()
      if auth_resp > 99:
        li = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
        li.setInfo(type='Video', infoLabels={ "Title": title })
        li.setProperty('IsPlayable', 'true')
        xbmc.Player().play(url, li)


    if usern=='':
      li = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
      li.setInfo(type='Video', infoLabels={ "Title": title })
      li.setProperty('IsPlayable', 'true')
      xbmc.Player().play(url, li)
      # Return an empty list so we can test with plugin.crawl() and
      # plugin.interactive()
      return []


@plugin.route('/epg/<ch>/')
def get_epg(ch):
    items = []
    was_now = 0
    #xbmcgui.Dialog().ok("get epg", epg)
    videos, total_results = get_recordings(ch)
    for video in videos:
      was_now = was_now + video['now']
      if was_now == 0:
        tsname = video['ts']
        items.append({
          'label': video['title'],
          'thumbnail': 'http://webtv.bhtelecom.ba/hq_logo/'+ch+'.png',
          'info': {'plot': video['summary'], },
          'url': 'http://webtvstream.bhtelecom.ba/rec/'+tsname+'.mp4',
          'is_folder': False,
          'is_playable': True,
        })

    if was_now == 0:
      items = []
    return plugin.add_items(items)



if __name__ == '__main__':
    plugin.run()
