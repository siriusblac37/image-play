import json
import re
import requests
import sys; sys.path.insert(0, '../dataset/')

from data_manipulator import DataManager

class ImageScraper:
	def __init__(self):
		self.dataManagerObj = DataManager()

	def getRequestForUs(self, requestLink):
		r = requests.get(requestLink)
		if 200 != r.status_code:
			raise
		return r.content

	def writeToAFile(self, pathToWriteTo, whatToWrite):
		try:
			with open(pathToWriteTo, 'wb') as fp:
				fp.write(whatToWrite)
		except:
			raise

	def getAndSaveMoviePoster(self, maybeMovieName, movieYear, itemIndex):
		requestLink = 'http://www.omdbapi.com/?t=%s&y=%s&r=json' %('+'.join(maybeMovieName.split()), movieYear)
		responseFromOmdb = json.loads(self.getRequestForUs(requestLink))
		if 'True' == responseFromOmdb['Response']:
			# Get the poster Link from the response and query that
			posterForMovie = self.getRequestForUs(responseFromOmdb['Poster'])
			self.writeToAFile('../dataset/images/%s.jpg' %(itemIndex,), posterForMovie)
		return responseFromOmdb['Response']

	def getAllPicturesFromWeb(self):
		failedList = []
        
		while True:
			punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
			line = self.dataManagerObj.getMovieNamesOneByOne()
			if not line:
				break
			elif line == 'skipped':
				continue
			else:
				# Parse the line to get the required info
				lineSplittedList = line.split('|')
				try:
					itemIndex = lineSplittedList[0].strip()
					movieName = re.findall(r'.+(?=\(\d{4}\))', lineSplittedList[1])[0].strip()
					movieYear = re.findall(r'\(\d{4}\)', lineSplittedList[1])[0].strip(' ()')
					
					maybeMovieName = ''.join([ch for ch in movieName if ch not in punctuations])	
					if True == self.getAndSaveMoviePoster(maybeMovieName, movieYear, itemIndex):
						continue
					
					# Name may be Usual Suspects, The. Try putting things after the comma before.
					splitName = movieName.rsplit(',', 1)
					maybeMovieName = ' '.join([splitName[1], splitName[0]])
					if True == self.getAndSaveMoviePoster(maybeMovieName, movieYear, itemIndex):
						continue

					# Name may be in the follwing way - Seven (Se7en). Try with name in (...)
					maybeMovieName = re.findall(r'\(.+\)', movieName)
					if maybeMovieName:
						maybeMovieName = maybeMovieName[0].strip(' ()')
						if True == self.getAndSaveMoviePoster(maybeMovieName, movieYear, itemIndex):
							continue
					
					# If all combinations fail, just add to the failed list. We will know what failed atleast.
					raise
				except:
					failedList.append(line)
				
		if failedList:
			print 'List of Movies which failed to be scraped'
			for indx, item in enumerate(failedList):
				print '%d : %s' %(indx, item)

obj = ImageScraper()
obj.getAllPicturesFromWeb()
