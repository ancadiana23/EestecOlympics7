import numpy as np
import cv2

def initWebcam():
	cap = cv2.VideoCapture(0)
	return cap

def destroyWebcam(webcam):
	cap.release()
	cv2.destroyAllWindows()

def runWebcam(cap, frame):
	
	ret, frame = cap.read()
	flipped = cv2.flip(frame, 1)
	cv2.imshow('Here be fingers', flipped)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


def main():
	cap = initWebcam()
	runWebcam(cap, frame)
	destroyWebcam(cap)

if __name__ == "__main__":
  main()