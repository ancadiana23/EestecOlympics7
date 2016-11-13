import numpy as np
import cv2
from sliding_window import SlidingWindow

def main():
    SL = SlidingWindow()
    SL.init()

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#frame_list = [x for row in frame for pixel in row for x in pixel]
        a, b, c = SL.detect(gray)
        if a != -1:
            print(a, b, c)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
