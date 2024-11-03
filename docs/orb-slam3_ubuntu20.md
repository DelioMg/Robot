# Installation guide for ORB-SLAM on UBUNTU 20LTS OrangePi

# 1. Installation of ORB-SLAM 3 on a fresh installed Ubuntu 22.04
Install all liberay dependencies.
```shell

sudo apt-get update && apt-get upgrade
sudo apt-get install build-essential make cmake
sudo apt-get install libeigen3-dev
sudo apt-get install git libgtk2.0-dev libcanberra-gtk-module
sudo apt -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libopenexr-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
sudo apt-get install libtiff-dev libopenblas-dev liblapack-dev libgtk-3-dev
sudo apt-get install build-essential cmake git pkg-config libatlas-base-dev gfortran libjpeg-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
sudo apt install libdc1394-dev libavresample-dev libgflags-dev libgoogle-glog-dev libhdf5-dev tesseract-ocr libtesseract-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjasper-dev
sudo apt-get install libglew-dev libboost-all-dev libssl-dev


```
---

### Install Pangolin 0.8
```shell


wget https://github.com/stevenlovegrove/Pangolin/archive/refs/tags/v0.8.zip
unzip v0.8.zip
cd Pangolin-0.8/scripts/
sudo ./install_prerequisites.sh
cd ..
mkdir build
cd build/
cmake ..
cmake --build .
sudo make install
rm v0.8.zip
```

---

### Install OpenCV 4.6.0
The ORB-SLAM 3 was test by  
```shell
cd ~
mkdir opencv_build
cd opencv_build/
wget https://github.com/opencv/opencv/archive/refs/tags/4.7.0.zip
wget https://github.com/opencv/opencv_contrib/archive/refs/tags/4.7.0.zip
unzip 4.7.0.zip
rm 4.7.0.zip
ls
mv 4.7.0.zip.1 4.7.0.zip
unzip 4.7.0.zip
rm 4.7.0.zip
ls
pwd
cd opencv-4.7.0/
```

```shell
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_EXAMPLES=OFF -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=OFF -D WITH_GTK=ON -D OPENCV_GENERATE_PKGCONFIG=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules ..
make -j4
sudo make install
pkg-config --modversion opencv4

```
---

### BOOST 1.78

```shell
wget https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.zip
unzip boost_1_78_0.zip
rm boost_1_78_0.zip
cd boost_1_78_0
sudo ./bootstrap.sh
sudo ./b2 install
cd ..
```
---

### CHECAR BIBLIOTECAS DE /usr/local/include 

```shell
cd /usr/local/include
```
---


### ORB-SLAM 3

```shell
cd ~/Dev
git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git 
cd ORB_SLAM3
sed -i 's/++11/++14/g' CMakeLists.txt
```

Recomendado ter 8GB de RAM, caso não tenha pode trava a build tendo que modificar o build.sh para make -j2 ou criar uma partição swap 
```shell
./build.sh
```
to install  

---

# 2. Download test datasets

```shell
cd ~
mkdir -p Datasets/EuRoc
cd Datasets/EuRoc/
wget -c http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_01_easy/MH_01_easy.zip
mkdir MH01
unzip MH_01_easy.zip -d MH01/

```
Similar for another datasets in EuRoc see here [https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets]


# 3. Run simulation 
```shell
cd ~/Dev/ORB_SLAM3

# Pick of them below that you want to run

# Mono
./Examples/Monocular/mono_euroc ./Vocabulary/ORBvoc.txt ./Examples/Monocular/EuRoC.yaml ~/Datasets/EuRoc/MH01 ./Examples/Monocular/EuRoC_TimeStamps/MH01.txt dataset-MH01_mono

# Mono + Inertial
./Examples/Monocular-Inertial/mono_inertial_euroc ./Vocabulary/ORBvoc.txt ./Examples/Monocular-Inertial/EuRoC.yaml ~/Datasets/EuRoc/MH01 ./Examples/Monocular-Inertial/EuRoC_TimeStamps/MH01.txt dataset-MH01_monoi

# Stereo
./Examples/Stereo/stereo_euroc ./Vocabulary/ORBvoc.txt ./Examples/Stereo/EuRoC.yaml ~/Datasets/EuRoc/MH01 ./Examples/Stereo/EuRoC_TimeStamps/MH01.txt dataset-MH01_stereo

# Stereo + Inertial
./Examples/Stereo-Inertial/stereo_inertial_euroc ./Vocabulary/ORBvoc.txt ./Examples/Stereo-Inertial/EuRoC.yaml ~/Datasets/EuRoc/MH01 ./Examples/Stereo-Inertial/EuRoC_TimeStamps/MH01.txt dataset-MH01_stereoi
```

# 4 Validation Estimate vs Ground True
We need numpy and matplotlib installed in pytho2.7. But Ubuntu20.04 has not pip2.7
```shell
sudo apt install curl
cd ~/Desktop
curl https://bootstrap.pypa.io/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py
pip2.7 install numpy matplotlib
```

**Run and plot Ground true**
```
cd ~/Dev/ORB_SLAM3

./Examples/Stereo/stereo_euroc ./Vocabulary/ORBvoc.txt ./Examples/Stereo/EuRoC.yaml ~/Datasets/EuRoc/MH01 ./Examples/Stereo/EuRoC_TimeStamps/MH01.txt dataset-MH01_stereo
```

**Plot estimate vs Ground true**
```
cd ~/Dev/ORB_SLAM3

python evaluation/evaluate_ate_scale.py evaluation/Ground_truth/EuRoC_left_cam/MH01_GT.txt f_dataset-MH01_stereo.txt --plot MH01_stereo.pdf
```

open the pdf `MH01_stereo.pdf` and you see the 


