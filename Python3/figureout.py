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

def isRedPixel(colors):
	return colors[2] > 200 and colors[1] < 150 and colors[0] < 150

def isBluePixel(colors):
	return colors[0]  >= 2 * colors[2] and colors[0] >= 2 * colors[1]

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
	while True:
		image = takeImage(webcamCurrent)
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