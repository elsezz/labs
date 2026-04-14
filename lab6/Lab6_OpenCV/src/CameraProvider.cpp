#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider(int cameraId) {
    std::string devicePath = "/dev/video" + std::to_string(cameraId);
    
    cap.open(devicePath, cv::CAP_V4L2);
    
    if (!cap.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити " << devicePath << "!" << std::endl;
    } else {
        cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
        cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
        cap.set(cv::CAP_PROP_FPS, 30); 
    }
}

CameraProvider::~CameraProvider() {
    if (cap.isOpened()) {
        cap.release();
    }
}

bool CameraProvider::getFrame(cv::Mat& frame) {
    if (!cap.isOpened()) return false;
    cap >> frame;
    return !frame.empty();
}
