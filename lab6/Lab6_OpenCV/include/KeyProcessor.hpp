#pragma once

enum class ProcessingMode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY
};

class KeyProcessor {
public:
    KeyProcessor();
    void processKey(int key);
    ProcessingMode getCurrentMode() const;
    bool shouldExit() const;

private:
    ProcessingMode currentMode;
    bool exitFlag;
};
