# lammlot
Client to the lend-engine API, to create an app that will make custom stickers (and hopefully more functionality)

## Building for Windows

    python -m PyInstaller lammlot.spec

## Building for Android

### Installation

    git clone https://github.com/kivy/buildozer.git
    cd buildozer
    python setup.py install
    cd ..
    buildozer init

Install buildozer dependences (like python-for-android)

### Deployment for testing

Plug in android device via USB, to build, push and run on device:

    buildozer android debug deploy run

