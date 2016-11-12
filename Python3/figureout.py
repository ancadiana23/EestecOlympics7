import random
import time

import numpy as np
import cv2

import webcam
import client

def initOrangeBounds:
        lowerOrange = np.uint8([[[5, 154, 222]]])
        upperOrange = np.uint8([[[7, 205, 247]]])
        lowerOrange = (cv2.cvtColor(lowerOrange, cv2.COLOR_BGR2HSV))[0][0]
        upperOrange = (cv2.cvtColor(upperOrange, cv2.COLOR_BGR2HSV))[0][0]
        lowerOrange = [lowerOrange[0] - 10, 100, 100]
        upperOrange = [upperOrange[0] + 10, 255, 255]
        lowerOrange = np.array(lowerOrange, dtype = "uint8")
        upperOrange = np.array(upperOrange, dtype = "uint8")

def takeImage(webcamCurrent):
	return webcam.runWebcam(webcamCurrent)


def sendTo(clientCurrent, x, y, state):
	clientCurrent.update_state(x, y, state)

def areCoordsValid(x, y):
	return x > 0 and x < 480 and y > 0 and y < 640

def isRedPixel(colors):
	return colors[2] > 200 and colors[1] < 150 and colors[0] < 150

def isBluePixel(colors):
	return colors[0]  >= 2 * colors[2] and colors[0] >= 2 * colors[1]

def getYellowZones(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lowerOrange, upperOrange)
        return cv2.bitwise_and(frame, frame, mask = mask)
def findContour(x, y, image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
	contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	cv2.drawContours(image,contours,-1,(255,0,0),3)
	cv2.imshow('HALP', image)
	#blueRect = None
	redRect = None
	# only proceed if at least one contour was found
	if len(contours) > 0:
		for contour in contours:
			
			x, y, z, t = cv2.boundingRect(contour)
			print (x, y, z, t)
			print(contour)
			if isRedPixel(image[(x[0] + y[0] + z[0] + t[0]) /4, (x[1] + y[1] + z[1] + z[1])/4]):
				redRect = (x, y, z, t)
				break
		

def main():
	random.seed(time.clock())
	clientCurrent = client.Client()
	webcamCurrent = webcam.initWebcam()
	initOrangeBounds()
	while True:
		image = takeImage(webcamCurrent)
		image = getYellowZones(image)
		findContour(0, 0, image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		'''if result is not None:
			(x, y, state) = result
			sendTo(clientCurrent, x, y, state)
'''
	webcam.destroyWebcam(webcamCurrent)
if __name__ == "__main__":
  main()
