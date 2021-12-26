import cv2
from PIL import Image
import pytesseract

filename = ['images/shawn/image37394.jpg']
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
config = '--psm 7'

def split_image(img):
	heightSplit = split_height(img)
	widthSplit = split_width(heightSplit)
#	print(f"Height: {height}, width: {width}") 
	return widthSplit

def recenter(img):
	new_img = img
	for i in range(3):
		new_img = split_height_btm(new_img)
	return new_img
# remove excess from bottom 
def split_height_btm(img):
	height = img.shape[0]

	height_cutoff = height // 2
	return img[:height_cutoff+10, :]



# remove excess from top 
def split_height(img):
	height = img.shape[0]

	height_cutoff = height // 2 
	return img[height_cutoff+10:,:]

def split_width(img):
	width = img.shape[1]
	width_cutoff = width // 2
	return img[:, :width_cutoff]


def resizeImgDim(img):
	scale_perc = 200
	height = (img.shape[0] * scale_perc // 100)
	width = (img.shape[1] * scale_perc // 100 )
	dim = (width, height)
	return dim


def main():
	# Expose only the text
	images = cv2.imread(filename[0])
	images = split_image(images)
	# images = split_height(images)
	# images = split_height(images)
	images = recenter(images)

	# Perform resize to improve readability
	dim = resizeImgDim(images)
	sizedImg = cv2.resize(images, dim, interpolation=cv2.INTER_AREA)

	# Bluring
	blurImg = cv2.GaussianBlur(sizedImg, (7, 7), cv2.BORDER_DEFAULT)
	# images = cv2.medianBlur(images, 3)

	# gray scale
	gray = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

	# threshold
	_, gray = cv2.threshold(
		gray, 150, 255, cv2.THRESH_BINARY)

	# img = cv2.imread('/Users/josimages/shawn/image5712.jpg')

	# Perform morphological operation - opening
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=3)

	cv2.imwrite(filename[0], gray)

	# Attempt text recognition
	text = pytesseract.image_to_string(
		Image.open(filename[0]), lang='eng', config=config)
	print(text)



if __name__ == '__main__':
	main()
