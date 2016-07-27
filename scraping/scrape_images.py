import sys; sys.path.insert(0, '../dataset/')

from data_manipulator import DataManager

class ImageScraper:
	def __init__(self):
		pass

	def getAllPicturesFromWeb(self):
		obj = DataManager()
		while True:
			line = obj.getMovieNamesOneByOne()
			if not line:
				break
			elif line == 'skipped':
				continue
			else:
				print line

obj = ImageScraper()
obj.getAllPicturesFromWeb()
