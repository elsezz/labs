#include "FaceDetector.hpp"
#include <iostream>
#include <chrono>

FaceDetector::FaceDetector(const std::string& prototxt, const std::string& caffemodel)
    : hasNewFrame(false), running(true)
{
    net = cv::dnn::readNetFromCaffe(prototxt, caffemodel);
    if (net.empty()) {
        std::cerr << "Помилка: Не вдалось завантажити модель нейронної мережі!" << std::endl;
    }

    workerThread = std::thread(&FaceDetector::workerLoop, this);
}

FaceDetector::~FaceDetector() {
    running = false;
    workerThread.join();
}

void FaceDetector::submitFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(mtx);
    pendingFrame = frame.clone();
    hasNewFrame = true;
}

std::vector<cv::Rect> FaceDetector::getDetections() const {
    std::lock_guard<std::mutex> lock(mtx);
    return lastDetections;
}

void FaceDetector::workerLoop() {
    while (running) {
        cv::Mat frameCopy;

        {
            std::lock_guard<std::mutex> lock(mtx);
            if (hasNewFrame && !pendingFrame.empty()) {
                frameCopy = pendingFrame.clone();
                hasNewFrame = false;
            }
        }

        if (!frameCopy.empty()) {
            // std::this_thread::sleep_for(std::chrono::milliseconds(500));

            auto results = detect(frameCopy);

            std::lock_guard<std::mutex> lock(mtx);
            lastDetections = results;
        } else {
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
        }
    }
}

std::vector<cv::Rect> FaceDetector::detect(const cv::Mat& frame) {
    std::vector<cv::Rect> faces;

    int h = frame.rows;
    int w = frame.cols;

    cv::Mat blob = cv::dnn::blobFromImage(frame, 1.0, cv::Size(300, 300),
                                          cv::Scalar(104.0, 177.0, 123.0));
    net.setInput(blob);
    cv::Mat detections = net.forward();

    // detections shape: [1, 1, N, 7]
    cv::Mat detMat(detections.size[2], detections.size[3], CV_32F,
                   detections.ptr<float>());

    for (int i = 0; i < detMat.rows; i++) {
        float confidence = detMat.at<float>(i, 2);

        if (confidence > 0.5f) {
            int x1 = static_cast<int>(detMat.at<float>(i, 3) * w);
            int y1 = static_cast<int>(detMat.at<float>(i, 4) * h);
            int x2 = static_cast<int>(detMat.at<float>(i, 5) * w);
            int y2 = static_cast<int>(detMat.at<float>(i, 6) * h);

            x1 = std::max(0, x1); y1 = std::max(0, y1);
            x2 = std::min(w - 1, x2); y2 = std::min(h - 1, y2);

            faces.emplace_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
        }
    }

    return faces;
}