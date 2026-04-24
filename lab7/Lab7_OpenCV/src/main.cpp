#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"
#include <memory>
#include <iostream>

int main() {
    CameraProvider camera(0);
    KeyProcessor keyProc;
    FrameProcessor frameProc;
    Display display("Lab 7 - Video Processing + Face Detection");

    std::unique_ptr<FaceDetector> faceDetector;

    cv::Mat frame;

    while (!keyProc.shouldExit()) {
        if (!camera.getFrame(frame)) {
            break;
        }

        ProcessingMode mode = keyProc.getCurrentMode();

        if (mode == ProcessingMode::FACE && !faceDetector) {
            std::cout << "Завантаження моделі нейронної мережі..." << std::endl;
            faceDetector = std::make_unique<FaceDetector>(
                "deploy.prototxt",
                "res10_300x300_ssd_iter_140000.caffemodel"
            );
            std::cout << "Модель завантажено." << std::endl;
        }

        std::vector<cv::Rect> faceRects;

        if (mode == ProcessingMode::FACE && faceDetector) {
            faceDetector->submitFrame(frame);
            faceRects = faceDetector->getDetections();
        }

        int brightnessOffset = display.getBrightnessOffset();
        frameProc.process(frame, mode, brightnessOffset, faceRects);

        display.show(frame);

        int key = cv::waitKey(1);
        if (key >= 0) {
            key = key & 0xFF;
            keyProc.processKey(key);
        }
    }

    return 0;
}