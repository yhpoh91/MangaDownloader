import re
import os
import string
import zipfile
from subprocess import check_output as co

def downloadManga(url, zip=False):
	# Get Manga Info
	mangaInfo = getMangaInfo(url)

	# Create Manga Directory
	title = getPossibleFileName(mangaInfo['title'])
	if(not os.path.exists(title)):
		os.mkdir(title)

	# Change to Manga Directory
	os.chdir(title)
	chapters = []
	for chapter in mangaInfo['chapters']:
		chapters.insert(0, chapter)

	for chapter in chapters:
		# Create Chapter Directory
		name = getPossibleFileName(chapter['name'])
		if(not os.path.exists(name)):
			os.mkdir(name)

		# Change to Chapter Directory
		os.chdir(name)
		
		if(not os.path.exists('.mangadone')):
			# Get Chapter Images URLs
			chapterURL = chapter['url']
			chapterImageURLs = getChapterImages(chapterURL)
			
			# Download Images
			downloadChapter(chapterImageURLs)

			# Check number of Images
			numberOfImages = len(chapterImageURLs)
			numberOfDownloadedFiles = getNumberOfFiles()
			if(numberOfImages == numberOfDownloadedFiles):
				# Create Done File
				open('.mangadone', 'a').close()

				# Create Zip File
				if(zip == True):
					zipDirectory(name)
		
		# Return to Parent Directory
		os.chdir("..")

	# Return to Parent Directory
	os.chdir("..")

def getNumberOfFiles():
	numberOfFiles = len([filename for filename in os.listdir('.') if os.path.isfile(filename)])
	if(os.path.exists(".DS_Store")):
		numberOfFiles -= 1

	return numberOfFiles

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
		try:
			co("curl -O -J \"" + line + "\"", shell=True)
		except Exception, e:
			print str(e)
			pass
	pass

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

def zipDirectory(name):
	zf = zipfile.ZipFile("../" + name + ".zip", "w")
	files = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
	for fileItem in files:
		if(fileItem != ".DS_Store" and fileItem != ".mangadone"):
			zf.write(fileItem)
	zf.close()