#!/bin/sh
echo Waiting for android device
adb wait-for-device
adb pull -a /storage/emulated/0/Android/data/com.sega.PhantasyStarOnline2es/files/3hwQzp8KE9T1oTpJCHPvxI5JIedD3AuT/ Databases
echo Update patch
mono ESBreakerCLI.exe > /dev/null
git commit -a
./make.sh
