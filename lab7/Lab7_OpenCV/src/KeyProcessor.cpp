#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(ProcessingMode::NORMAL), exitFlag(false) {}

void KeyProcessor::processKey(int key) {
    if (key == -1) return;

    switch (key) {
        case '1': currentMode = ProcessingMode::NORMAL; break;
        case '2': currentMode = ProcessingMode::INVERT; break;
        case '3': currentMode = ProcessingMode::BLUR;   break;
        case '4': currentMode = ProcessingMode::CANNY;  break;
        case '5': currentMode = ProcessingMode::FACE;   break;
        case 'q':
        case 27:  // ESC
            exitFlag = true;
            break;
    }
}

ProcessingMode KeyProcessor::getCurrentMode() const { return currentMode; }
bool KeyProcessor::shouldExit() const { return exitFlag; }