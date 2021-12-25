import cv2
from PIL import Image
import os
import pytesseract

def split_image(img):
	height = img.shape[0]
	width = img.shape[1]
	width_cutoff = width // 2
	height_cutoff = height // 2 
#	print(f"Height: {height}, width: {width}") 
	return img[height_cutoff:, :width_cutoff]

 
def split_height(img):
	height = img.shape[0]

	height_cutoff = height // 2 
	return img[:height_cutoff,:]

def resizeImg(img):
	scale_perc = 200
	height = (img.shape[0] * scale_perc // 100)
	width = (img.shape[1] * scale_perc // 100 )
	dim = (width, height)
	return dim


filename = 'images/shawn/image37325.jpg'
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
images = cv2.imread(filename)
images = split_image(images) 
images = split_height(images)
images = split_height(images)
dim = resizeImg(images)
images = cv2.resize(images, dim, interpolation=cv2.INTER_AREA)

# Bluring
images  = cv2.GaussianBlur(images, (7,7), cv2.BORDER_DEFAULT)
# images = cv2.medianBlur(images, 3)

# gray scale
gray=cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

# threshold
_, gray = cv2.threshold(
	gray, 150, 255, cv2.THRESH_BINARY )

# img = cv2.imread('/Users/josimages/shawn/image5712.jpg')

# Opening 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=3)

cv2.imwrite(filename, gray) 
text = pytesseract.image_to_string(Image.open(filename), lang='eng', config='--psm 7')

print(text)


