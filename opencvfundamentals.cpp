// ENME 489Y: Remote Sensing
// Week 3: OpenCV Fundamentals

// Files to use
#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>
#include <thread>

// Libaries to use
using namespace cv;
using namespace std;

using Clock = std::chrono::steady_clock;
using std::chrono::time_point;
using std::chrono::duration_cast;
using std::chrono::milliseconds;
using namespace std::literals::chrono_literals;
using std::this_thread::sleep_for;

// Main function
int main()
{
	// Optional timer to assess how long it takes to run program
	time_point<Clock> start = Clock::now();

	cout << "ENME 489Y: Remote Sensing" << endl;
	cout << "OpenCV Fundamentals" << endl;
	cout << "Program is" << " running!" << endl;

	// Displaying & resizing images
	Mat image = imread("testudo.png");
	imshow("Old School Testudo Logo",image);
	waitKey(0);

	// Resize image (if needed)
	Mat image_scaled;
	resize(image, image_scaled, cv::Size(image.cols * 0.9, image.rows * 0.9), 0, 0, CV_INTER_LINEAR);
	imshow("Old School Testudo Logo: Resized", image_scaled);
	waitKey(0);

	// Write image to disk (save image)
	imwrite("resizedTestudo.jpg", image_scaled);

	// Image shape (dimensions)
	cout << " " << endl;
	cout << "    ------------    " << endl;
	cout << " " << endl;
	cout << "Image width: " << image.size().width << endl;
	cout << "Image height: " << image.size().height << endl;

	// Pixel operations & image slicing
	cout << " " << endl;
	cout << "    ------------    " << endl;
	cout << " " << endl;
	cout << "Pixel at (0, 0) has the following BGR characteristics:" << endl;
	cout << image_scaled.at<Vec3b>(0, 0) << endl;

	for (int i = 0; i < 100; i++)
	{
		for (int j = 0; j < 50; j++) 
		{
			image_scaled.at<Vec3b>(i, j) = Vec3b(0, 255, 0);
		}
	}
	imshow("Corner", image_scaled);
	waitKey(0);

	cout << " " << endl;
	cout << "    ------------    " << endl;
	cout << " " << endl;
	cout << "Pixel at (0, 0) has the following BGR characteristics:" << endl;
	cout << image_scaled.at<Vec3b>(0, 0) << endl;

	// Image blurring
	Mat a = image.clone();
	Mat a_blur;
	blur(a, a_blur, Size(3, 3), Point(-1, -1));

	Mat a_concat;
	hconcat(a, a_blur, a_concat);
	imshow("Average Blurring", a_concat);
	waitKey(0);

	Mat b = image.clone();
	Mat b_blur;
	GaussianBlur(b, b_blur, Size(3, 3), 0, 0);
	
	Mat b_concat;
	hconcat(b, b_blur, b_concat);
	imshow("Gaussian Blurring", b_concat);
	waitKey(0);

	Mat c = image.clone();
	Mat c_blur;
	medianBlur(c, c_blur, 3);
	
	Mat c_concat;
	hconcat(c, c_blur, c_concat);
	imshow("Median Blurring", c_concat);
	waitKey(0);

	Mat d = image.clone();
	Mat d_blur;
	bilateralFilter(d, d_blur, 5, 21, 21);
	
	Mat d_concat;
	hconcat(d, d_blur, d_concat);
	imshow("Bilateral Filtering", d_concat);
	waitKey(0);

	// Drawing lines & rectangles
	Mat canvas(500, 500, CV_8UC3, Scalar(0, 0, 0));
	imshow("Canvas", canvas);
	waitKey(0);

	line(canvas, Point(0, 0), Point(400, 500), Scalar(0, 255, 0));
	imshow("Green Line", canvas);
	waitKey(0);

	line(canvas, Point(500, 0), Point(0, 500), Scalar(0, 0, 255), 3);
	imshow("Red Line", canvas);
	waitKey(0);

	rectangle(canvas, Point(40, 50), Point(100, 100), Scalar(0, 255, 0));
	imshow("Green Rectangle", canvas);
	waitKey(0);

	rectangle(canvas, Point(50, 400), Point(400, 225), Scalar(0, 0, 255), 5);
	imshow("Red Rectangle", canvas);
	waitKey(0);

	rectangle(canvas, Point(350, 150), Point(400, 425), Scalar(255, 0, 0), -1);
	imshow("Blue Rectangle", canvas);
	waitKey(0);

	// Drawing circles
	Mat canvas2(500, 500, CV_8UC3, Scalar(0, 0, 0));
	imshow("Canvas2", canvas2);
	waitKey(0);

	circle(canvas2, Point(canvas2.size().height/2, canvas2.size().width/2), 100, Scalar(255, 255, 255));
	imshow("Circle", canvas2);
	waitKey(0);

	// Overlay text on top of an image
	putText(canvas2, "Hello World!", Point(30, 30),
		FONT_HERSHEY_COMPLEX_SMALL, 1, Scalar(0, 0, 255), 1, CV_AA);
	imshow("Text Overlay", canvas2);
	waitKey(0);

	// Transforming images / flipping
	Mat hflip;
	flip(image, hflip, 1);
	imshow("Flipped Horizontally", hflip);
	waitKey(0);

	Mat vflip;
	flip(image, vflip, 0);
	imshow("Flipped Vertically", vflip);
	waitKey(0);

	Mat hvflip;
	flip(image, hvflip, -1);
	imshow("Flipped Horizontally & Vertically", hvflip);
	waitKey(0);

	// Rectangular mask
	Mat image1 = imread("testudo.jpg");
	imshow("Old School Testudo Logo", image1);
	waitKey(0);

	Mat image_scaled1;
	resize(image1, image_scaled1, cv::Size(image1.cols * 0.8, image1.rows * 0.8), 0, 0, CV_INTER_LINEAR);
	imshow("Old School Testudo Logo: Resized", image_scaled1);
	waitKey(0);

	Mat mask(image_scaled1.size().height, image_scaled1.size().width, CV_8UC3, Scalar(0, 0, 0));
	int cX = image_scaled1.size().height / 2;
	int cY = image_scaled1.size().width / 2;
	rectangle(mask, Point(cX - 75, cY - 75), Point(cX + 75, cY + 75), Scalar(255, 255, 255), -1);
	imshow("Mask", mask);
	waitKey(0);

	Mat masked; 
	bitwise_and(image_scaled1, mask, masked);
	imshow("Bitwise AND: Rectangular Mask", masked);
	waitKey(0);

	// Circular mask
	Mat circular_mask(image_scaled1.size().height, image_scaled1.size().width, CV_8UC3, Scalar(0, 0, 0));
	circle(circular_mask, Point(cX, cY), 100, Scalar(255, 255, 255), -1);
	imshow("Circular Mask", circular_mask);
	waitKey(0);

	Mat circular_masked;
	bitwise_and(image_scaled1, circular_mask, circular_masked);
	imshow("Bitwise AND: Circular Mask", circular_masked);
	waitKey(0);

	// End of timer
	time_point<Clock> end = Clock::now();
	milliseconds diff = duration_cast<milliseconds>(end - start);
	cout << diff.count() << "ms" << endl;
	waitKey(0);

	return 0;
}
