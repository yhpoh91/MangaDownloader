import re
import urllib
import zlib
from subprocess import check_output as co


def getURLContent(url):
	response = urllib.urlopen(url)
	data = response.read()
	if(response.headers.getheader('Content-Encoding') == 'gzip'):
		data = zlib.decompress(data, 16+zlib.MAX_WBITS)
	return data

def getChapterImages(url):
	imageURLsReturn = []
	chapterURLDirectory = ""
	optionLine = ""
	optionLinesSplit = []
	imageNumbers = []
	try:
		# response = co("curl \"" + url + "\"", shell=True)
		# response = zlib.decompress(response, 16+zlib.MAX_WBITS)
		response = getURLContent(url)
		responseDataSplit = response.split('\n')
		
		# Number of Chapters
		for line in responseDataSplit:
			if(re.match("(.+)tion value=(.+)<option value=\"0\" >Comments</opt(.+)", line)):
				optionLine = line;

		if(len(optionLine) > 0):
			optionLinesSplit = optionLine.split('</option>')
			imageNumbers = getNumberOfImages(optionLinesSplit)

		# Chapter URL Directory
		regexResults = re.findall("(.+)1.html", url)
		if(len(regexResults) > 0):
			chapterURLDirectory = regexResults[0]

		# Image
		for imageNumber in imageNumbers:
			imageURL = getImageURL(str(chapterURLDirectory) + str(imageNumber) + ".html")
			if(imageURL != ""):
				imageURLsReturn.append(imageURL)
	except Exception, e:
		print str(e)
		pass

	return imageURLsReturn

def getImageURL(pageURL):
	imageURL = ""
	try:
		# response = co("curl \"" + pageURL + "\"", shell=True)
		# response = zlib.decompress(response, 16+zlib.MAX_WBITS)
		response = getURLContent(pageURL)
		responseDataSplit = response.split('\n')

		for line in responseDataSplit:
			regexResults = re.findall("(.+)mg src=\"(.+)\" onerror=\"this.src=(.+)/></a(.+)", line)
			if(len(regexResults) > 0):
				imageURL = regexResults[0][1]
				break
	except Exception, e:
		print str(e)
		pass
	return imageURL

def getNumberOfImages(optionLines):
	imageNumbers = ["1"]
	for line in optionLines:
		option = re.findall("<option value=\"(.+)\" >(.+)", line)
		if(len(option) > 0):
			if(option[0][1] != "Comments"):
				imageNumbers.append(option[0][0])
	return imageNumbers

def getMangaInfo(url):
	chapterURLs = []
	chapterURLsReturn = []
	mangaTitle = "gg"
	try:
		# response = co("curl \"" + url + "\"", shell=True)
		response = getURLContent(url)
		responseDataSplit = response.split('\n')

		for line in responseDataSplit:
			mangaTitles = re.findall("<h1 style=\"font-size:28px\">(.+) Manga</h1>", line)
			if(len(mangaTitles) > 0):
				mangaTitle = mangaTitles[0]

			mangaTitles = re.findall("<h1 style=\"font-size:28px\">(.+) Manhua</h1>", line)
			if(len(mangaTitles) > 0):
				mangaTitle = mangaTitles[0]

			mangaTitles = re.findall("<h1 style=\"font-size:28px\">(.+) Manhwa</h1>", line)
			if(len(mangaTitles) > 0):
				mangaTitle = mangaTitles[0]

			# chapterURL = re.findall("<a href=\"(.+)\" title=\"Read (.+) online\">", line)
			chapterURL = re.findall("(.+)<a href=\"(.+)\" title=\"(.+)\" class=\"tips\">(.+)</a>", line)
			if(len(chapterURL) > 0):
				chapterURLsReturn.append({"url":str(chapterURL[0][1]), "name":str(chapterURL[0][3])})
	
	except Exception, e:
		print str(e)
		pass

	mangaInfo = {"title":mangaTitle, "chapters":chapterURLsReturn}
	return mangaInfo