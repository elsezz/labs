#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    FrameProcessor();
    void process(cv::Mat& frame, ProcessingMode mode, int brightnessOffset);

private:
    double lastTick;
    void drawFPS(cv::Mat& frame);
};
