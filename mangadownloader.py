import re
import os
import string
import zipfile
from subprocess import check_output as co

import mangafox
import kissmanga

# Save Home Directory
homeDirectory = os.getcwd()

# Get Manga
mangaURL = raw_input("Manga URL: ")
if(mangaURL != "GG"):
	downloadManga(mangaURL)

def downloadManga(url, source="MF", zip=False, remove=False):
	# Get Source
	mangaSource = getMangaSource(source)

	# Get Manga Info
	mangaInfo = mangaSource.getMangaInfo(url)

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
			chapterImageURLs = mangaSource.getChapterImages(chapterURL)
			
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
					if(remove == True):
						deleteImages()
		
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

def zipDirectory(name):
	zf = zipfile.ZipFile("../" + name + ".zip", "w")
	files = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
	for fileItem in files:
		if(fileItem != ".DS_Store" and fileItem != ".mangadone"):
			zf.write(fileItem)
	zf.close()

def deleteImages():
	filenames = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
	for filename in filenames:
		if(filename != '.mangadone'):
			os.remove(filename)

def goToHomeDirectory():
	os.chdir(homeDirectory)

def getMangaSource(source):
	mangaSource = kissmanga
	if source == "MF":
		mangaSource = mangafox
	elif source == "KM":
		mangaSource = kissmanga

	return mangaSource


