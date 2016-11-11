#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;
using namespace std;
 
int main(void) 
{
	VideoCapture cam(0);
	 
	if (!cam.isOpened()) 
		cout << "cannot open camera";
	 
	while (1) 
	{
		Mat frame;
		cam.read(frame);
		imshow("cam", frame);
		if (waitKey(30) >= 0)
			break;
	}
	return 0;
}