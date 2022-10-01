# Astro Speech Recognition
In this project you are going to find the voice routines that it has Astro implemented in its core. Here you can modify
things like this:

1. voice recognition algorithms
2. text to speech / speech to text algorithms
3. voice commands
4. voice commands routines

![alt text](assets/astro-speech-recognition.jpg?raw=true "Project Architecture")

## Prepare the development environment
It's good to mention that this proyect has been tested in a Linux based environment, specifically in Raspbian, so in operating systems like Windows may not work.
This project uses pyaudio to listen from the mic, apparently this library doesn't work well in Windows or Mac Os, so you if you want to test funcionalities like the voice recognition, you need a Raspberry Pi machine or a computer with some Linux distro.

**⚠ It's very recommended to use python 3.8 or higher ⚠**

1. First of all, be sure to have installed python3, virtualenv and redis
2. Clone the repo from [this link](https://github.com/Cosmoblastos/astro-speech-recognition).
3. Go to the project folder and generate a virtual environment with: `virtualenv -p . venv`. This will create a folder in your proyect that cointains main scripts to handle an agnostic environment that has its own python, pip and dependencies versions.
4. Install all the dependencies with `pip install -r modules.txt`. This step could have a lot of errors depending on your mahcine and configuration.
5. Run the project with `python init.py`

---
## 🔧 How to fix the posible errors that can appear 🔧

1. Error while installing pyaudio on mac M1:
- Install portaudio with brew:
````
brew install portaudio
````
- Link portaudio:
````
brew link portaudio
````
- Get the path where is portaudio installed:
````
brew --prefix portaudio
````
- Create this file and paste the following lines:
````
sudo nano $HOME/.pydistutils.cfg
````
````
[build_ext]
include_dirs=<PATH FROM STEP 3>/include/
library_dirs=<PATH FROM STEP 3>/lib/
````
- Finally, install pyaudio:
````
pip install pyaudio
````

## How the project is organized
root:
- audio: this folder contain the sounds and beats that astro can play regardless of its voice. Can be button sounds, ringtones, alerts, etc.
- commands: contains the scripts to create a voice command routine. All the files on this project should be classes extended by the VoiceCommand super class.
- config: 
- lib
- tests
- venv
- init.py


## CHEAT SHEET
-CREATE A REDIS USER: ACL SETUSER astro allkeys +@string +@set -SADD >astro

## Required system dependencies

- sudo apt install flac libsox-fmt-mp3 sox portaudio19-dev

sox: contains the play command to execute audio files
portaudio19-dev: allows the usage of pyaudio


