Android Testing Tool For Kivy/Python
=========================================
A basic kivy app for testing code snippets on android and viewing 
the output

Use [buildozer](https://buildozer.readthedocs.io/en/latest/quickstart.html) 
to compile the app and run it after adding the code you wish to test 
in the 'main.py' file

The 'android_os.py' file is not essential to the build, but I kept it 
in the folder just in case it becomes relevant to the current test case.
It currently contains some methods for creating and storing encrypted
passwords on an Android device, which I couldn't find anywhere else, 
which was why I made this in the first place.

