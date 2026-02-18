# ESONIC Paus De Deux Code

### Hey look guys I'm making a fancy README!

Ok so this is gonna be the repo for our project. I'm using a virtual environment in VS Code so you'll have to set that up. I'm on python version 3.13.1 but probably any python version 3 or above will do.

You'll have to set up the virtual environment yourself if you don't know how just ask me. I could make some fancy tutorial for how to do it in this README file but ehhhh I don't wanna. 

Here's the basic file layout:

### Network:
This will be for receiving the data sent by our ESP32s. Right now I have it set up as a UDP server running asynchronously and expects the files in JSON format. If its different I can reconfigure it but this seems to work pretty well. 

### Processing: 
I haven't done anything in this yet but it'll probably just be data processing. 

### State:
All I have in this right now is a basic enum class representing the different states our instrument can be in since it has the locking mechanism and all. Maybe I'll make a fancy FSM Diagram and put it in this README but probably not because that's a waste of time. 

### Testing:
I'm just simulating sending the UDP server data here since we don't have the ESP32s set up yet.

Hey Marcos if you wanna help out with the software stuff you can help me out with all this while Leslie and Natalie are setting up the hardware. 

