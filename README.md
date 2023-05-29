# COMODORO  
Comodoro is a cross platform Graphical User Interface (GUI) and Command Line Interface (CLI) app that implements the [pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) technique.  
## STATUS  
This project is currently on alpha stage. A lot of features hasn't been implemented yet.  
## INSTALLATION  
At this point, comodoro doesn't have an installer, so you will have to build a stand alone executable yourself or run it from source. We will only cover running it from source for now. Installers will be created when the project is at beta stage.  
### DEPENDENCIES  
**Dependencies not related to python**  
To be able to play a sound when a timer is done, you'll have to install the
libvlc library or vlc. If you already have vlc, you are good to go.  
#### [LINUX](https://code.videolan.org/videolan/LibVLCSharp/blob/master/docs/linux-setup.md)  
To install libvlc on ubuntu, open a terminal and run this command:  
```bash
sudo apt-get install libvlc-dev
```  
#### [WINDOWS](https://www.videolan.org/vlc/)  
Open your terminal and run the command:  
```bash
winget install VideoLAN.VLC.SDK
```
#### [MACOS](https://www.videolan.org/vlc/)  
Open your terminal and run this command:  
```bash
brew install libvlc
```
### Running From Source  
1. You will need python3.10.x. We aren't using the latest version of python (python3.11) because the GUI library comodoro is using has a [bug](https://github.com/wxWidgets/Phoenix/issues/2296) that makes installing it via pip buggy. If you don't have python, you can get one [here](https://www.python.org/downloads/).  
2. To run it from source, start by cloning this repo:  
    ```bash
    git clone https://arfs6/comodoro
    ```
    3. change your working folder / directory to the root of the project:  
```bash
cd comodoro
```
4. Next, install all the required python packages using pip:  
```bash
pip install -r requirements.txt
```
### Creating Standalone Executable  
1. Do all the above steps for running from source.  
2. Change your directory to the src directory.  
	```bash
	$ cd src
	```
3. Start the build process. 
	```bash
	$ python setup.py build
	```
	The executable will be found in `build/*/Comodoro.exe`.  
## USAGE  
You can use comodoro in two ways. Using the GUI and CLI.  
### GUI  
To start comodoro and show the GUI:  
1. Just click the main.pyw file from your GUI.
2. Run the main.pyw file from terminal without any argument  
### CLI  
This is currently not supported but will be added shortly. 
## Contributions  
All contributions are highly welcomed. Read our
(contributing.md)[./CONTRIBUTING.md] on how to contribute to comodoro.  
## LICENSE  
This software is licensed under the GNU General Public License. You can find
the license in the [LICENSE.md](./LICENSE.md) file.
