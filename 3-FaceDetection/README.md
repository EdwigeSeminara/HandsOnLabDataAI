1. Download and install Python 2.7 :
https://www.python.org/downloads/

2. For windows, install pip :
https://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows

3. Download and install OpenCV :
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows

4. Open a console and install Python packages with the following commands :
```
cd C:\Python27
Python.exe -m pip install requests
Python.exe -m pip install matplotlib
Python.exe -m pip install numpy
```
5. Go on the portal Azure to create the Cognitive Services Account :
- url : http://portal.azure.com
- Click on "More services" and search "cognitive services"
- Click sur "+ Add" and search "Face API" and click on "Create"
- Set the name of the account, select the princing F0 (free), select the ressource group and click on "Create"
- When the setup of the ressource is finished, go grab your API Key and copy/past it in the variable _key of the FaceDetection.py script

6. Now you can run FaceDetection.py, open a CMD console, go into the 3-FaceDetection\ folder and run :
```
C:\Python27\python.exe FaceDetection.py
```