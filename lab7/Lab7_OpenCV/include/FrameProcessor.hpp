#pragma once
#include <opencv2/opencv.hpp>
#include <vector>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    FrameProcessor();
    void process(cv::Mat& frame, ProcessingMode mode, int brightnessOffset,
                 const std::vector<cv::Rect>& faceRects = {});

private:
    double lastTick;
    void drawFPS(cv::Mat& frame);
    void drawModeLabel(cv::Mat& frame, ProcessingMode mode);
};