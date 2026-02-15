# lammlot

An app for staff at [lend-engine](https://www.lend-engine.com/) sites that creates custom stickers, to print on a sticker machine, for your items. 

## Features

* search for items by site
* select items to generate and save sticker images for, in multiple common sizes
* Supports python 3.13+ and (soon) executables for Android and Windows
* Requires an API key from your Lend Engine site (Plus or Business level account is needed)

## Credits

Created by Bil Bas at "BayShare - The Libraries of Things" (LoT group, for Morecambe Bay, that is not yet public).

Support this project: https://ko-fi.com/bilbas

## Building

### Windows

    python -m PyInstaller lammlot.spec

### Android

#### Installation

    git clone https://github.com/kivy/buildozer.git
    cd buildozer
    python setup.py install
    cd ..
    buildozer init

#### Deployment for testing

Plug in android device via USB, to build, push and run on device:

    buildozer android debug deploy run

