#include "Display.hpp"

Display::Display(const std::string& winName) : windowName(winName) {
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);
    
    cv::createTrackbar("Brightness", windowName, NULL, 100);
    
    cv::setTrackbarPos("Brightness", windowName, 50);
}

void Display::show(const cv::Mat& frame) {
    cv::imshow(windowName, frame);
}

int Display::getBrightnessOffset() const {
    int pos = cv::getTrackbarPos("Brightness", windowName);
    return (pos - 50) * 2; 
}
