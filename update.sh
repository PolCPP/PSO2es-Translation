#!/bin/sh
echo Waiting for android device
adb wait-for-device
apkpath=$(adb shell pm path com.sega.PhantasyStarOnline2es | _py/_APK_package.py)
apkversion=$(adb shell dumpsys package com.sega.PhantasyStarOnline2es| _py/_APK_version.py)
mkdir -p apk
echo pulling PSO2 APK
adb pull $apkpath apk
echo Extracting DLLs
unzip -xfj apk/base.apk "assets/bin/Data/Managed/*.dll" -d apk
echo linking needed DLLs
ln -sf apk/Assembly-CSharp-firstpass.dll .
ln -sf apk/ContentsSerializer.dll .
ln -sf apk/ProtoBuffSerializer.dll .
ln -sf apk/protobuf-net.dll .
ln -sf apk/UnityEngine.dll .
mkdir -p Databases
rm -rf Databases/*
echo Getting stock Database files
adb pull -a /sdcard/Android/data/com.sega.PhantasyStarOnline2es/files/3hwQzp8KE9T1oTpJCHPvxI5JIedD3AuT/. Databases
echo Update patch
mono ESBreakerCLI.exe > /dev/null
export apkversion
git commit --m "$apkversion" -- json
./make.sh
