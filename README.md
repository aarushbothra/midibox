# midibox
Turns .midi files into .dxf files, primarily for music box paper strips with a high degree of customizability. 

Allows for variable dimensions of the strip, as well as different sized stock paper that will be cut. Will output a new .dxf file for each page of paper needed. Currently, these settings need to be edited at the top of the python file.

# Prerequisites
Requires Python 3.8, as well as libraries mido, ezdxf, and pretty_midi to be installed on the system running the program

# How to Use
Before starting, edit the global variables above the dashed lines to match the specifications of the music box and paper you will be using. Next, run the gui.py file, and a subdirectory should be created with your .dxf files in the same directory as gui.py. I plan on creating an actual GUI in the future to make this process easier. You can test these features using the midi files provided in /midi.

