import time
import learn_sci_2
from PIL import Image
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import scipy.ndimage

class SlidingWindow:

	def init(self):
	    self.sl_width = 20
	    self.sl_height = 30

	    self.ratio = 13

            self.hand_detector, self.click_detector = learn_sci_2.train()

	    self.sl_size = self.sl_width, self.sl_height

	def detect(self, img):
		img_n = scipy.ndimage.zoom(img, 0.076, order=0)
		
		height = len(img_n)
		width = len(img_n[0])

		sl_width = 20
		sl_height = 30

		i = 0
		j = 0
		
		while i < height - sl_height:
			while j < width - sl_width:

				img_1 = img_n[i : (i + sl_height), j : (j + sl_width)]
				window = [element for line in img_1 for element in line]

				output = self.hand_detector.predict([window])[0]

				if output == 0:
					output = self.click_detector.predict([window])[0]
					return i, j, output
				j += 1
			i += 1
		return -1, -1, -1
	
if __name__ == "__main__":
	i, j, c = main()
	
