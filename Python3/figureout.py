import numpy as np
import cv2

import webcam
import client


def takeImage(webcamCurrent):
	return webcam.runWebcam(webcamCurrent)

def sendTo(clientCurrent, x, y, state):
	clientCurrent.update_state(x, y, state)

def areCoordsValid(x, y):
	return x > 0 and x < 480 and y > 0 and y < 640


def getYellowZones(image, day):
	if day is False:
		lowerOrange = np.uint8([[[5, 154, 222]]])
		upperOrange = np.uint8([[[7, 205, 247]]])
		lowerOrange = np.uint8([[[9, 87, 149]]])
		upperOrange = np.uint8([[[34, 161, 206]]])
	else:
		lowerOrange = np.uint8([[[9, 105, 151]]])
		upperOrange = np.uint8([[[22, 147, 197]]])
		lowerOrange = np.uint8([[[9, 87, 149]]])
		upperOrange = np.uint8([[[34, 161, 206]]])


	lowerOrange = (cv2.cvtColor(lowerOrange, cv2.COLOR_BGR2HSV))[0][0]
	upperOrange = (cv2.cvtColor(upperOrange, cv2.COLOR_BGR2HSV))[0][0]
	lowerOrange = [lowerOrange[0] - 5, 150, 140]
	upperOrange = [upperOrange[0] + 10, 255, 255]
	lowerOrange = np.array(lowerOrange, dtype = "uint8")
	upperOrange = np.array(upperOrange, dtype = "uint8")
	blurred = cv2.GaussianBlur(image,(5,5),0)
	kernel = np.ones((5,5),np.uint8)

	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	#blurred = cv2.erode(blurred,kernel,iterations = 5)
	#blurred = cv2.dilate(blurred,kernel,iterations = 5)
	mask = cv2.inRange(hsv, lowerOrange, upperOrange)
	return cv2.bitwise_and(blurred, image, mask = mask)


def findContour(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
	contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	cv2.drawContours(image,contours,-1,(255,0,0),3)
	cv2.imshow('Cursor', image)
	
	if len(contours) > 0:
		contour = max(contours, key=cv2.contourArea)
		x, y, z, t = cv2.boundingRect(contour)
		if z < 25 or t < 25:
			return None
		state = 1; 
		if z < t:
			state = 0
		return(x+z/2, y+t/2, state)

def main():
	isDay = True
	clientCurrent = client.Client()
	clientCurrent.start()
	webcamCurrent = webcam.initWebcam()
	while True:
		image = takeImage(webcamCurrent)
		image2 = image.copy()
		image = getYellowZones(image, isDay)
		result = findContour(image)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
		if result is not None:
			(x, y, state) = result
			sendTo(clientCurrent, x, y, state)
	webcam.destroyWebcam(webcamCurrent)

if __name__ == "__main__":
  main()
