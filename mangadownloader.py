import re
import os
import string
from subprocess import check_output as co

def downloadManga(url):
	# Get Manga Info
	mangaInfo = getMangaInfo(url)

	# Create Manga Directory
	title = getPossibleFileName(mangaInfo['title'])
	os.mkdir(title)

	# Change to Manga Directory
	os.chdir(title)
	
	for chapter in mangaInfo['chapters']:
		# Create Chapter Directory
		name = getPossibleFileName(chapter['name'])
		os.mkdir(name)

		# Change to Chapter Directory
		os.chdir(name)
		
		# Get Chapter Images URLs
		chapterURL = chapter['url']
		chapterImageURLs = getChapterImages(chapterURL)
		
		# Download Images
		downloadChapter(chapterImageURLs)
		
		# Return to Parent Directory
		os.chdir("..")

	# Return to Parent Directory
	os.chdir("..")

def getPossibleFileName(name):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	# name = ''.join(c for c in name if c in valid_chars)
	newName = ""
	for c in name:
		if c in valid_chars:
			newName += c
		else:
			newName += '-'
	return newName

def downloadChapter(imageURLs):
	for line in imageURLs:
		co("curl -O -J \"" + line + "\"", shell=True)
	pass

def getChapterImages(url):
	imageURLsReturn = []
	response = co("curl \"" + url + "\"", shell=True)
	responseDataSplit = response.split('\n')

	for line in responseDataSplit:
		imageURL = re.findall("\s+lstImages.push\(\"(.+)\"\);", line)
		if(len(imageURL) > 0):
			imageURLsReturn.append(imageURL[0])

	return imageURLsReturn

def getMangaInfo(url):
	chapterURLs = []
	chapterURLsReturn = []
	mangaTitle = "gg"
	response = co("curl \"" + url + "\"", shell=True)
	responseDataSplit = response.split('\n')

	for line in responseDataSplit:
		mangaTitles = re.findall("<a Class=\"bigChar\" href=\"(.+)\">(.+)</a>", line)
		if(len(mangaTitles) > 0):\
			mangaTitle = mangaTitles[0][1]

		chapterURL = re.findall("<a href=\"(.+)\" title=\"Read (.+) online\">", line)
		if(len(chapterURL) > 0):
			chapterURLsReturn.append({"url":"http://kissmanga.com" + str(chapterURL[0][0]), "name":str(chapterURL[0][1])})

	mangaInfo = {"title":mangaTitle, "chapters":chapterURLsReturn}
	return mangaInfo

