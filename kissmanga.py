import re
import os
import string
import zipfile
import urllib
from subprocess import check_output as co

def getChapterImages(url):
	imageURLsReturn = []
	try:
		response = co("curl \"" + url + "\"", shell=True)
		responseDataSplit = response.split('\n')

		for line in responseDataSplit:
			imageURL = re.findall("\s+lstImages.push\(\"(.+)\"\);", line)
			if(len(imageURL) > 0):
				imageURLsReturn.append(imageURL[0])
	except Exception, e:
		print str(e)
		pass

	return imageURLsReturn

def getMangaInfo(url):
	chapterURLs = []
	chapterURLsReturn = []
	mangaTitle = "gg"
	try:
		response = co("curl \"" + url + "\"", shell=True)
		responseDataSplit = response.split('\n')

		for line in responseDataSplit:
			mangaTitles = re.findall("<a Class=\"bigChar\" href=\"(.+)\">(.+)</a>", line)
			if(len(mangaTitles) > 0):\
				mangaTitle = mangaTitles[0][1]

			chapterURL = re.findall("<a href=\"(.+)\" title=\"Read (.+) online\">", line)
			if(len(chapterURL) > 0):
				chapterURLsReturn.append({"url":"http://kissmanga.com" + str(chapterURL[0][0]), "name":str(chapterURL[0][1])})
	
	except Exception, e:
		print str(e)
		pass

	mangaInfo = {"title":mangaTitle, "chapters":chapterURLsReturn}
	return mangaInfo