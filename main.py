#! /usr/bin/python3
#sudo bash ./requirements.sh
#which python3, chmod +x main.py
from pytube import YouTube
from sys import argv
from pydub import AudioSegment #needed "sudo apt install ffmpeg"
from os.path import splitext
from os import remove

url = argv[1]
ytvideo = YouTube(url) #ytvideo.title, thumbnail_url
abr = ytvideo.streams.filter(only_audio=True) #list with all audio bit rates
maxi = float("-inf")
for i in range(len(abr)):
	rate = float(getattr(abr[i], "abr")[:-4])
	maxi = max(maxi, rate)
	if maxi == rate:
		maxIndex = i
		#ext_max = getattr(abr[i], "mime_type")[6:]#mime_type="audio/mp4"

downloaded = abr[maxIndex].download() #downloaded file (name)
name, ext = splitext(downloaded)
if ext != ".mp3":
	AudioSegment.from_file(downloaded).export(name + ".mp3", format="mp3", bitrate="320k")
	remove(downloaded)