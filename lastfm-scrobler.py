#!/usr/bin/python
#coding: utf-8

import pylast
import os
import urllib2
import re
import ConfigParser
import time

network = None
now_playing = None
now_playing_countdown = 20

def get_config(config_file):
	config = ConfigParser.ConfigParser()
	config.readfp(open(config_file),"rb")
	appkey = config.get("profile","appkey")
	appsecret = config.get("profile","appsecret")
	username = config.get("profile","username")
	password = config.get("profile","password")
	return (appkey, appsecret, username, password)

def getLastFMScrobbleObject():
	(API_KEY, API_SECRET, username, password) = get_config("config.ini")
	password_hash = pylast.md5(password)

	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
	        API_SECRET, username = username, password_hash = password_hash)

	#track = network.get_track("石进", "初恋的美好")
	#print track.get_duration()
	#print track.get_playcount()

	return network
	
def parse_song_info(song_id):

	xml_loc = 'http://www.xiami.com/song/playlist/id/' + song_id + '/object_name/default/object_id/0'
	#print xml_loc

	headers = {
		'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) Chrome/24.0.1312.57'
	}
	request = urllib2.Request(xml_loc, headers = headers)
	response = urllib2.urlopen(request)
	text = response.read()
	#print text

	song_title_reg=r"<title><\!\[CDATA\[(.*)\]\]></title>"
	match = re.search(song_title_reg, text)
	if match:
		song_title = match.group(1).strip()
		#print song_title
	else:
		print 'song_title not match'
		song_title = "未知"

	artist_reg=r"<artist><\!\[CDATA\[(.*)\]\]></artist>"
	match = re.search(artist_reg, text)
	if match:
		artist = match.group(1).strip()
		#print artist
	else:
		print 'artist not match'
		artist = "未知"

	return (song_title, artist.split(";")[0])


def handle_cached_dir(dir):

	global network, now_playing, now_playing_countdown

        now_playing_countdown = now_playing_countdown - 1

	filelist = os.listdir(dir)
        count = len(filelist)
	for onefile in filelist:
		filepath = os.path.join(dir,onefile)

                count = count -1
		if os.path.isfile(filepath): 
			#filename: timestamp-songid
			info = onefile.split('-')
			
                        if count == 0:
                                if now_playing != onefile or now_playing_countdown == 0:

                                        (song_title, artist) = parse_song_info(info[1])
                                        network.update_now_playing(artist, song_title, info[0])
                                        if now_playing_countdown > 0:
                                                print "Now playing:", artist, "-", song_title
                                        now_playing = onefile
                                        now_playing_countdown = 20

                        else:
                                (song_title, artist) = parse_song_info(info[1])
                                if int(time.time())-int(info[0]) > 30:

                                        network.scrobble(artist, song_title, info[0])
                                        print "Scrobbled: ", artist, "-", song_title
                                else:
                                        print "Skipped: ", artist, "-", song_title

                                os.remove(filepath)

def main():
	global network
	network = getLastFMScrobbleObject()
	print "Scrobbler initiated."
        while (True):
                handle_cached_dir("data")
                time.sleep(1)

if __name__ == '__main__' :
        main()
