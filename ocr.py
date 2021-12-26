import cv2
from PIL import Image
import pytesseract
# image4492
files = [f'images/shawn/image{x}.jpg' for x in range(4200,37394,2)]
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
config = '--psm 7'


test_files = ['images/shawn/image4200.jpg',
              'images/shawn/image4420.jpg', 'images/shawn/image37393.jpg']
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

def outputDim(img):
	print(img.shape)

def display(text,img):
	cv2.imshow(text, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# remove excess from top 
def split_height(img):
	height = img.shape[0]

	height_cutoff = height // 2 
	return img[height_cutoff+10:,:]

def split_width(img):
	width = img.shape[1]
	width_cutoff = width // 2
	return img[:, :width_cutoff-200]


def resizeImgDim(img):
	scale_perc = 200
	height = (img.shape[0] * scale_perc // 100)
	width = (img.shape[1] * scale_perc // 100 )
	dim = (width, height)
	return dim


def main(filename):

	def writeToFile(text):
		with open('results_dec_25_2021.txt', 'a') as f:
			f.write(text)

	try:

		# Expose only the text
		images = cv2.imread(filename)
		images = split_image(images)
		# images = split_height(images)
		# images = split_height(images)
		images = recenter(images)

		# Perform resize to improve readability
		dim = resizeImgDim(images)
		sizedImg = cv2.resize(images, dim, interpolation=cv2.INTER_AREA)

		# Bluring
		blurImg = cv2.GaussianBlur(sizedImg, (7, 7), cv2.BORDER_ISOLATED)
		# blurImg = cv2.medianBlur(blurImg, 1)

		# gray scale
		gray = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

		# threshold
		_, gray = cv2.threshold(
                    gray, 155, 255, cv2.THRESH_BINARY + cv2.THRESH_TOZERO
                )

		# img = cv2.imread('/Users/josimages/shawn/image5712.jpg')

		# Perform morphological operation - opening
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
		gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=3)

		newFileName = f'{filename}-modified.jpg'
		# Write file to new location
		
		# outputDim(sizedImg)
		# display("original", sizedImg)
		# outputDim(gray)
		# display("gray", gray)
		
		# bitwise-and 
		result = cv2.bitwise_and(sizedImg, sizedImg, mask=gray)


		result[gray == 0] = (0, 0, 0)
		# _, result = cv2.threshold(
		# 	gray, 240, 255, cv2.THRESH_BINARY)
		cv2.imwrite(newFileName, result)


		# display("bitwise", result)	

		# Attempt text recognition
		text = pytesseract.image_to_string(
			Image.open(newFileName), lang='eng', config=config)
		
		writeToFile(text)
		
	except cv2.error as e:
		writeToFile(f"Error modifying filename {filename} {e}" )

	except AttributeError as e:
		writeToFile(f"Error modifying filename {filename} {e}")

	

		


if __name__ == '__main__':
	for file in files:
		main(file)
