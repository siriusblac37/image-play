import requests
import sys; sys.path.insert(0, '../dataset/')

from data_manipulator import DataManager

class ImageScraper:
	def __init__(self):
		self.dataManagerObj = DataManager()

	def getAllPicturesFromWeb(self):
		while True:
			line = self.dataManagerObj.getMovieNamesOneByOne()
			if not line:
				break
			elif line == 'skipped':
				continue
			else:
				# Parse the line to get the required info
				# Send the request to OMDb
				r = requests.get('')
				# If response is False from OMDb, try other combinations.
				# Name may be in the follwing way - Seven (Se7en). Try with name in (...)
				# Name may be Usual Suspects, The. Try putting things after the comma before.
				# Remove the punctuation marks and just send the whole thing 
				# If all combinations fail, just add to the failed list. We will know what failed atleast.
				
				

obj = ImageScraper()
obj.getAllPicturesFromWeb()
