#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

int main() {
    CameraProvider camera(0);
    KeyProcessor keyProc;
    FrameProcessor frameProc;
    Display display("Lab 6 - Video Processing");

    cv::Mat frame;

    while (!keyProc.shouldExit()) {
        if (!camera.getFrame(frame)) {
            break;
        }

        int brightnessOffset = display.getBrightnessOffset();
        
        frameProc.process(frame, keyProc.getCurrentMode(), brightnessOffset);
        
        display.show(frame);

        int key = cv::waitKey(1) & 0xFF; 
        if (key != 255) {
            keyProc.processKey(key);
        }
    }

    return 0;
}
