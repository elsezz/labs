echo "Встановлення залежностей."
sudo apt update
sudo apt install libopencv-dev cmake gcc g++ make wget -y
 
echo "Завантаження моделі для детекції облич (ResNet-10 SSD)."
wget -q --show-progress -O deploy.prototxt \
  "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
 
wget -q --show-progress -O res10_300x300_ssd_iter_140000.caffemodel \
  "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
 
echo "Залежності та моделі успішно встановлено."vvvv