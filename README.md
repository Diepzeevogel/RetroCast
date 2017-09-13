# RetroCast
An attempt at creating a ChromeCast like experience for retro gaming.

# Installing the required software

Install retropie the usual way and enable ssh through the raspi-config

SSH into retropie and install libcec and psutil by entering the following commands:

for psutil:

```sudo apt-get update
sudo apt-get install python-dev python-pip
sudo pip install psutil
```

and for libcec:

```sudo apt-get update
sudo apt-get install cmake libudev-dev libxrandr-dev python-dev swig
cd
git clone https://github.com/Pulse-Eight/platform.git
mkdir platform/build
cd platform/build
cmake ..
make
sudo make install
cd
git clone https://github.com/Pulse-Eight/libcec.git
```

Currently there is a bug in libcec, so you have to remove the following lines from libcec/src/libcec/cmake/CheckPlatformSupport.cmake

Use your favorite text editor like `nano` or `vim`.
```SET(PYTHON_LIB_INSTALL_PATH "/cec" CACHE STRING "python lib path")
if (${CMAKE_MAJOR_VERSION} GREATER 2 AND ${CMAKE_MAJOR_VERSION} GREATER_EQUAL 7)
    SET(PYTHON_LIB_INSTALL_PATH "" CACHE STRING "python lib path" FORCE)
else()
    if (${CMAKE_MAJOR_VERSION} GREATER_EQUAL 3)
    SET(PYTHON_LIB_INSTALL_PATH "" CACHE STRING "python lib path" FORCE)
    endif()
endif()
```

Afterwards just procede with building libcec.

```mkdir libcec/build
cd libcec/build
cmake -DRPI_INCLUDE_DIR=/opt/vc/include -DRPI_LIB_DIR=/opt/vc/lib ..
make -j4
sudo make install
sudo ldconfig
```

The script should now be functional, but requires some more work.

I'll be working on a more streamlined experience.


# Credit
Credit to [daftmike](https://github.com/imdaftmike) who built the [NESPi](http://www.daftmike.com/2016/07/NESPi.html), a mini Raspberry Pi based NES. 
If you look through the code you will see that I stole most of it from him.