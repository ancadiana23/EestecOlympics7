import random
import time

import webcam
import client


def takeImage(webcamCurrent):
	return webcam.runWebcam(webcamCurrent)


def sendTo(clientCurrent, x, y, state):
	clientCurrent.update_state(x, y, state)

def isRedRegion(x, y, image):
	return False

def isBlueAdjacent(x, y, image):
	return False

def findContour(x, y, image):
	return None

def processImage(image):
	(foundx, foundy) = (None, None)
	i = 0;
	while foundx is None and i < 1000:
		x = random.randint(0, 640)
		y = random.randint(0, 480)
		if isRedRegion(x, y, image):
			(foundx, foundy) = (x, y)
			break
		++i

	if foundx is None:
		return None

	contour = findCountour(foundx, foundy, image)

	(pressedx, pressedy) = (None, None)
	for (x, y) in contour:
		if isBlueAdjacent(x, y):
			return (x, y, 1)

	return (x, y, 0)



def main():
	random.seed(time.clock())
	clientCurrent = client.Client()
	webcamCurrent = webcam.initWebcam()
	image = takeImage(webcamCurrent)
	(x, y, state) = processImage(image)
	sendTo(clientCurrent, x, y, state)

if __name__ == "__main__":
  main()