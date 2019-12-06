echo off
echo %~dpnx0
rem start  
py %~dp0..\..\pumba-wizardry.py --caller %~dpnx0 %*
rem simple.json

