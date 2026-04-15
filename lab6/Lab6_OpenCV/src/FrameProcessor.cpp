#include "FrameProcessor.hpp"
#include <string>

FrameProcessor::FrameProcessor() {
    lastTick = (double)cv::getTickCount();
}

void FrameProcessor::process(cv::Mat& frame, ProcessingMode mode, int brightnessOffset) {
    frame.convertTo(frame, -1, 1, brightnessOffset);

    switch (mode) {
        case ProcessingMode::INVERT:
            cv::bitwise_not(frame, frame);
            break;
        case ProcessingMode::BLUR:
            cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0);
            break;
        case ProcessingMode::CANNY:
            cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
            cv::Canny(frame, frame, 50, 150);
            cv::cvtColor(frame, frame, cv::COLOR_GRAY2BGR); 
            break;
        case ProcessingMode::NORMAL:
        default:
            break;
    }

    drawFPS(frame);
}

void FrameProcessor::drawFPS(cv::Mat& frame) {
    double currentTick = (double)cv::getTickCount();
    double fps = cv::getTickFrequency() / (currentTick - lastTick);
    lastTick = currentTick;

    std::string fpsText = "FPS: " + std::to_string((int)fps);
    cv::putText(frame, fpsText, cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 0), 2);
}
