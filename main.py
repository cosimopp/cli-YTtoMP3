#! /usr/bin/python3
#sudo bash ./requirements.sh
#which python3, chmod +x main.py
from pytube import YouTube
from pytube import Playlist #the playlist must be public for the download to succeed
from sys import argv
from pydub import AudioSegment #needed "sudo apt install ffmpeg"
from os.path import splitext
from os import remove, getcwd

#toDo check whether user is connected
def DownloadSong(url, path):
	ytvideo = YouTube(url) #ytvideo.title, thumbnail_url
	abr = ytvideo.streams.filter(only_audio=True) #list of songs with all audio bit rates
	maxi = float("-inf")
	for i in range(len(abr)):
		rate = float(getattr(abr[i], "abr")[:-4])
		maxi = max(maxi, rate)
		if maxi == rate:
			maxIndex = i
			#ext_max = getattr(abr[i], "mime_type")[6:]#mime_type="audio/mp4"

	downloaded = abr[maxIndex].download(path) #downloaded file (name), in requested path 
	name, ext = splitext(downloaded)
	if ext != ".mp3":
		AudioSegment.from_file(downloaded).export(name + ".mp3", format="mp3", bitrate="320k")
		remove(downloaded)
	print(f"{name}.mp3 successfully downloaded!")

url = argv[1]
if len(argv) > 2:
	path = argv[2] # user indicated path
else:
	path = getcwd() # current path
if "playlist" in url:
	playlist = Playlist(url) #lista degli url dei video nella playlist #https://github.com/pytube/pytube/issues/848
	for yturl in playlist.video_urls: DownloadSong(yturl, path)
	print(f"all {len(playlist.video_urls)} songs successfully downloaded!\n")
else: DownloadSong(url, path)