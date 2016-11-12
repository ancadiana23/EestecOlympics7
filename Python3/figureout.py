import random
import time

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
	else:
		lowerOrange = np.uint8([[[9, 105, 151]]])
		upperOrange = np.uint8([[[22, 147, 197]]])

	lowerOrange = (cv2.cvtColor(lowerOrange, cv2.COLOR_BGR2HSV))[0][0]
	upperOrange = (cv2.cvtColor(upperOrange, cv2.COLOR_BGR2HSV))[0][0]
	lowerOrange = [lowerOrange[0] - 5, 100, 100]
	upperOrange = [upperOrange[0] + 10, 255, 255]
	lowerOrange = np.array(lowerOrange, dtype = "uint8")
	upperOrange = np.array(upperOrange, dtype = "uint8")
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lowerOrange, upperOrange)
	return cv2.bitwise_and(image, image, mask = mask)

def getBlueZones(image, day):
	if day is False:
		lowerBlue = np.uint8([[[89, 42, 22]]])
		upperBlue = np.uint8([[[181, 96, 28]]])
	else:
		lowerBlue = np.uint8([[[89, 42, 22]]])
		upperBlue = np.uint8([[[181, 96, 28]]])

	lowerBlue = (cv2.cvtColor(lowerBlue, cv2.COLOR_BGR2HSV))[0][0]
	upperBlue = (cv2.cvtColor(upperBlue, cv2.COLOR_BGR2HSV))[0][0]
	print(lowerBlue, upperBlue)
	lower_lower_because_why_not = min(lowerBlue[0], upperBlue[0])
	lowerBlue = [lower_lower_because_why_not - 5, 50, 50]
	upperBlue = [upperBlue[0] - lower_lower_because_why_not + lowerBlue[0] + 10, 255, 255]
	lowerBlue = np.array(lowerBlue, dtype = "uint8")
	upperBlue = np.array(upperBlue, dtype = "uint8")
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lowerBlue, upperBlue)
	return cv2.bitwise_and(image, image, mask = mask)

def findContour(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
	contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	cv2.drawContours(image,contours,-1,(255,0,0),3)
	cv2.imshow('Galben', image)
	
	if len(contours) > 0:
		contour = max(contours, key=cv2.contourArea)
		x, y, z, t = cv2.boundingRect(contour)
		if z < 25 or t < 25:
			return None 
		return(x+z/2, y+t/2)

def findBlueContours(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
	contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	cv2.drawContours(image,contours,-1,(255,0,0),3)
	cv2.imshow('HALP', image)
	if len(contours) > 0:
		contour = max(contours, key=cv2.contourArea)
		x, y, z, t = cv2.boundingRect(contour)
		if z > 25 or t > 25:
			return True
	return False

def main():
	isDay = True

	random.seed(time.clock())
	clientCurrent = client.Client()
	clientCurrent.start()
	webcamCurrent = webcam.initWebcam()
	while True:
		image = takeImage(webcamCurrent)
		image2 = image.copy()
		image = getYellowZones(image, isDay)
		result = findContour(image)
		state = False;
		image2 = getBlueZones(image2, isDay)
		if findBlueContours(image2):
			state = True
		print(state)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if result is not None:
			(x, y) = result
			sendTo(clientCurrent, x, y, state)
	webcam.destroyWebcam(webcamCurrent)

if __name__ == "__main__":
  main()
