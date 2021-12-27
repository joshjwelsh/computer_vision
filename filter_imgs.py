import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import shutil

# files = [f'images/shawn/image{x}.jpg' for x in range(4200, 37394, 1)]

# index = {}
# images = {}
# test_files = files[:500:100]
# test_files.append('images/shawn/image4205.jpg')
# for file in files[:10]:
# 	image = cv2.imread(file)
# 	filename = file.split('/')[-1]
# 	# print(filename)
# 	images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
# 	# print(file)
# 	hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
# 	hist = cv2.normalize(hist, hist).flatten()
# 	index[filename] = hist


# results = {}
# files_to_add = []
# for (k, hist) in index.items():
# 	d = cv2.compareHist(index["image4200.jpg"], hist, cv2.HISTCMP_CHISQR)
# 	results[k] = d
# 	if d > 1:
# 		files_to_add.append(k)

# print(files_to_add)

# print(results)
# 37394

class Controller:
	def __init__(self):

		self.start = 0
		self.index_i = self.start + 1
		self.files = [f'images/shawn/image{x}.jpg' for x in range(32337, 37394, 1)]
		self.end = len(self.files)

		self.images = {}
		self.index = {}
		self.results = {}
		self.files_to_add = []


	def buildHistogram(self, filename, image):
		hist = cv2.calcHist([image], [0, 1, 2], None, [
		8, 8, 8], [0, 256, 0, 256, 0, 256])
		hist = cv2.normalize(hist, hist).flatten()
		self.index[filename] = hist


	def readImage(self, file):
		image = cv2.imread(file)
		filename = file.split('/')[-1]
		# print(filename)
		self.images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		return image

	def getFilenameFromFile(self, file):
		return file.split('/')[-1]
	
	def clearIndexDict(self):
		self.images.clear()
		self.results.clear()
		self.index.clear()

	def path2File(self, filename):
		return f'images/shawn/{filename}'

	def compareImgs(self,file):
		try:
			# Get start img to compare with other images
			start = self.files[self.start]
			startFileName = self.getFilenameFromFile(start)
			startImg = self.readImage(start)
			print("start is ", startFileName)
			# set up file that will be juxaposed against start file
			image = self.readImage(file)
			filename = self.getFilenameFromFile(file)
		
			self.buildHistogram(filename, image)	
			self.buildHistogram(startFileName, startImg)

			for (k, hist) in self.index.items():
				d = cv2.compareHist(self.index[startFileName], hist, cv2.HISTCMP_CHISQR)
				self.results[k] = d	
				if d > 1:
					self.files_to_add.append(self.path2File(k))
					self.clearIndexDict()
					return True
			
			self.clearIndexDict()
			return False

		except cv2.error as e:
			print('Error - ', e)
			return False

		except AttributeError as e:
			print('Error - ', e)
			return False

	def findValidImgs(self):
		while self.start < self.end and self.index_i < self.end:		
			file = self.files[self.index_i]
			# name = self.getFilenameFromFile(file)
	
			if self.compareImgs(file):
				self.start = self.index_i + 1
				self.moveFiles()
				
			self.index_i += 1


	

	def moveFiles(self):
		for file in self.files_to_add:
			shutil.move(file, 'preproccesed/')
		self.files_to_add.clear()



controller = Controller()
controller.findValidImgs()

print(controller.files_to_add)


				

			
			



