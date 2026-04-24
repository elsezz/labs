#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
public:
    FaceDetector(const std::string& prototxt, const std::string& caffemodel);
    ~FaceDetector();

    void submitFrame(const cv::Mat& frame);

    std::vector<cv::Rect> getDetections() const;

private:
    cv::dnn::Net net;

    mutable std::mutex mtx;
    cv::Mat pendingFrame;
    bool hasNewFrame;
    std::vector<cv::Rect> lastDetections;

    std::thread workerThread;
    std::atomic<bool> running;

    void workerLoop();
    std::vector<cv::Rect> detect(const cv::Mat& frame);
};