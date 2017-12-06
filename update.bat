@echo off
echo Waiting for android device
adb wait-for-device
adb pull -a /storage/emulated/0/Android/data/com.sega.PhantasyStarOnline2es/files/3hwQzp8KE9T1oTpJCHPvxI5JIedD3AuT/ Databases
echo Making patch
ESBreakerCLI.exe > nul
git commit -a
call make.bat
