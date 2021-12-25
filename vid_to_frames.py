import cv2

# Opens the video file
cap = cv2.VideoCapture('shawn_cee_top_50_songs.mp4')

i = 0
while(cap.isOpened()):
	ret, frame = cap.read() 
	if ret == False:
		break
	cv2.imwrite('images/shawn/image' + str(i) + '.jpg', frame) 
	i += 1

cap.release()
cv2.destroyAllWindows()
