class DataManager:
	def __init__(self):
		self.basePath = None
		self.fp = None

	def getMovieNamesOneByOne(self):
		if self.fp is None:
			try:
				self.fp = open('../dataset/ml-100k/u.item')
			except IOError:
				return None
		try:
			line = self.fp.readline()
		except:
			line = 'skipped'
		finally:
			if not line:
				self.fp.close()
			return line
