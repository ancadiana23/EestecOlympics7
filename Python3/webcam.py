import numpy as np
import cv2

def runWebcam():
	cap = cv2.VideoCapture(-1)
	i=0;
	while(True):
		ret, frame = cap.read()
		cv2.imshow('Here be fingers', frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

def main():
	runWebcam();

if __name__ == "__main__":
  main()