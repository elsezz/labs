#!/bin/bash
echo "Запуск програми."

cp -n deploy.prototxt res10_300x300_ssd_iter_140000.caffemodel build/

cd build
./Lab7_OpenCV