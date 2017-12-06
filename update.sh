#!/bin/sh
echo Waiting for android device
adb wait-for-device
pmapkpath=`adb shell pm path com.sega.PhantasyStarOnline2es`
apkpath=$(echo $pmapkpath|_py/APKcut.py)
adb pull $apkpath tmp
unzip -xfj apk/base.apk "assets/bin/Data/Managed/*.dll" -d apk
ln -sf apk/Assembly-CSharp-firstpass.dll .
ln -sf apk/ContentsSerializer.dll .
ln -sf apk/ProtoBuffSerializer.dll .
ln -sf apk/protobuf-net.dll .
ln -sf apk/UnityEngine.dll .
rm -rf Databases/*
adb pull -a /storage/emulated/0/Android/data/com.sega.PhantasyStarOnline2es/files/3hwQzp8KE9T1oTpJCHPvxI5JIedD3AuT/. Databases
echo Update patch
mono ESBreakerCLI.exe > /dev/null
git commit -a
./make.sh
