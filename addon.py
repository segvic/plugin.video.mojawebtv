#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
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
#from urllib import urlencode
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


PLUGIN_NAME = 'MojawebTV'
PLUGIN_ID = 'plugin.video.mojawebtv'





pluginhandle = int(sys.argv[1])

plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)



BASE_URL = 'http://www.bhtelecom.ba/'
def full_url(path):
    return urljoin(BASE_URL, path)


YOUTUBE_PTN = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
def youtube_url(videoid):
    return YOUTUBE_PTN % (videoid)


def parse_video(video):
    '''Returns a dict of information for a given json video object.'''
    info = {
        'title': video['epgstart']+'  '+video['epgtitle']+' ('+str(video['epgduration'])+' min)',
        'summary': video['title'],
        'videoid': video['ch'],
        'start': video['epgstart'],
        'thumbnail': 'http://195.222.33.193/thumbs/'+video['ch']+'.jpg?x='+datetime.now().strftime('%Y%m%d%H%M%S'),
        'logo': 'http://195.222.33.193/hq_logo/'+video['ch']+'.png',
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
      url  = 'http://195.222.33.193/channels'
    if list_id == 'cam':
      url  = 'http://195.222.33.193/channels_cat_4'
    if list_id == 'radio':
      url  = 'http://195.222.33.193/channels_cat_11'
    if list_id == 'rec':
      url = 'http://195.222.33.193/channels_rec'

    src = download_page(url)
    resp = json.loads(src)
    videos  = resp['feed']

    video_infos = map(parse_video, videos)
    total_results = resp
    return video_infos, total_results


def get_recordings(id):


    url  = 'http://195.222.33.193/epg/'+id
    #xbmcgui.Dialog().ok("EPG URL", url)
    src = download_page(url)
    resp = json.loads(src)
    recs  = resp['feed']

    video_infos = map(parse_recs, recs)
    total_results = resp
    return video_infos, total_results



@plugin.route('/', default=True)
def show_homepage():
    usern =  xbmcplugin.getSetting(pluginhandle, 'username')
    passwd = xbmcplugin.getSetting(pluginhandle, 'password')
    auth.doAuth(usern, passwd)
    items = [
        # SD Live
        {'label': plugin.get_string(30100),
         'url': plugin.url_for('show_live', label='sd')},
        {'label': plugin.get_string(30101),
         'url': plugin.url_for('show_live', label='cam')},
        {'label': plugin.get_string(30102),
         'url': plugin.url_for('show_live', label='radio')},
        # Recordings
        {'label': plugin.get_string(30103),
         'url': plugin.url_for('show_live', label='rec')},

    ]
    return plugin.add_items(items)



@plugin.route('/labels/<label>/')
def show_live(label):
    '''
    '''
    items = []
    usern =  xbmcplugin.getSetting(pluginhandle, 'username')
    passwd = xbmcplugin.getSetting(pluginhandle, 'password')
    auth.doAuth(usern, passwd)


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
      videos, total_results = get_videos('sd')
      i = 0;
      for video in videos:

          items.append({
            'label': video['summary'],
            'info': {'plot': video['start']+' '+video['title'], },
            'thumbnail': video['thumbnail'],
            'url': plugin.url_for('play_live', url='http://'+server[video['cluster']]+':1935/live/'+video['videoid']+''+ext[video['cluster']]+'/playlist.m3u8', title=(video['title'].encode('utf8')), thumb=video['logo']),
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
            'url': plugin.url_for('play_live', url='http://'+server[video['cluster']]+':1935/live/'+video['videoid']+''+ext[video['cluster']]+'/playlist.m3u8', title=(video['title'].encode('utf8')), thumb=video['logo']),
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
            'url': plugin.url_for('play_live', url='http://'+server[video['cluster']]+':1935/live/'+video['videoid']+''+ext[video['cluster']]+'/playlist.m3u8', title=(video['title'].encode('utf8')), thumb=video['logo']),
            'is_folder': False,
            'is_playable': False,
          })

    if label=='rec':
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


@plugin.route('/live/<url>/<title>/<thumb>')
def play_live(url, title, thumb):

    rtmpurl = url
    epgtitle = title
    li = xbmcgui.ListItem(label=epgtitle, thumbnailImage=thumb)
    li.setInfo(type='Video', infoLabels={ "Title": epgtitle })
    li.setProperty('IsPlayable', 'true')
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmpurl, li)
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
          'thumbnail': 'http://195.222.33.193/hq_logo/'+ch+'.png',
          'info': {'plot': video['summary'], },
          'url': 'http://195.222.59.138:1935/vod/mp4:'+tsname+'.mp4/playlist.m3u8',
          'is_folder': False,
          'is_playable': True,
        })

    if was_now == 0:
      items = []
    return plugin.add_items(items)



if __name__ == '__main__':
    plugin.run()
