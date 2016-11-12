import numpy as np
import cv2

def initWebcam():
	cap = cv2.VideoCapture(-1)
	return cap

def destroyWebcam(cap):
	cap.release()
	cv2.destroyAllWindows()

def runWebcam(cap):
	ret, frame = cap.read()
	flipped = cv2.flip(frame, 1)
	return flipped


def main():
	cap = initWebcam()
	i=0
	while(True):
		ret, frame = cap.read()
		flipped = cv2.flip(frame, 1)
		cv2.imshow('Here be fingers', flipped)
		cv2.imwrite("ref" + str(i) + ".jpg", flipped)
		i = i+1
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	destroyWebcam(cap)

if __name__ == "__main__":
  main()