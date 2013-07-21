#!/usr/bin/python
#coding: utf-8

import pylast
import os
import urllib2
import re
import threading
import ConfigParser

network = None

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
	#print song_id
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

	return (song_title, artist)


def handle_cached_dir(dir):
	print "start handle cached history"
	global network 
	filelist = os.listdir(dir)
	for onefile in filelist:
		filepath = os.path.join(dir,onefile)
		if os.path.isfile(filepath): 
			#filename: timestamp-songid
			info = onefile.split('-')
			print info[0], info[1]
			(song_title, artist) = parse_song_info(info[1])
			print song_title, artist
			#network = getLastFMScrobbleObject()
			network.scrobble(artist, song_title, info[0])
			os.remove(filepath)
	timer_start()

def timer_start(): 
	t = threading.Timer(60, handle_cached_dir, {"data"}) 
	t.start() 

def main():
	global network
	network = getLastFMScrobbleObject()
	print "start works!"
	timer_start()

if __name__ == '__main__' :
	main()
