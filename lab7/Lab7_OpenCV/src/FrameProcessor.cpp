#include "FrameProcessor.hpp"
#include <string>

FrameProcessor::FrameProcessor() {
    lastTick = (double)cv::getTickCount();
}

void FrameProcessor::process(cv::Mat& frame, ProcessingMode mode, int brightnessOffset,
                              const std::vector<cv::Rect>& faceRects)
{
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
        case ProcessingMode::FACE:
            for (const auto& rect : faceRects) {
                cv::rectangle(frame, rect, cv::Scalar(0, 255, 0), 2);
                cv::putText(frame, "Face", cv::Point(rect.x, rect.y - 8),
                            cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
            }
            break;
        case ProcessingMode::NORMAL:
        default:
            break;
    }

    drawFPS(frame);
    drawModeLabel(frame, mode);
}

void FrameProcessor::drawFPS(cv::Mat& frame) {
    double currentTick = (double)cv::getTickCount();
    double fps = cv::getTickFrequency() / (currentTick - lastTick);
    lastTick = currentTick;

    std::string fpsText = "FPS: " + std::to_string((int)fps);
    cv::putText(frame, fpsText, cv::Point(10, 30),
                cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 0), 2);
}

void FrameProcessor::drawModeLabel(cv::Mat& frame, ProcessingMode mode) {
    std::string label;
    switch (mode) {
        case ProcessingMode::NORMAL: label = "Mode: Normal [1]";  break;
        case ProcessingMode::INVERT: label = "Mode: Invert [2]";  break;
        case ProcessingMode::BLUR:   label = "Mode: Blur   [3]";  break;
        case ProcessingMode::CANNY:  label = "Mode: Canny  [4]";  break;
        case ProcessingMode::FACE:   label = "Mode: Face   [F]";  break;
    }
    cv::putText(frame, label, cv::Point(10, 60),
                cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(255, 255, 0), 1);
}