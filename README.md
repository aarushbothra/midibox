# midibox
Turns .midi files into .dxf files, primarily for music box paper strips with a high degree of customizability. 

Allows for variable dimensions of the strip, as well as different sized stock paper that will be cut. Will output a new .dxf file for each page of paper needed. Currently, these settings need to be edited at the top of the python file.

# How to Use
1. Put your midi file in the `midi` directory
2. In `main.py`, change `docName` to the path to your midi file, and edit any relavent global variables
3. Run `./midibox/bin/python3 gui.py` to generate your DXF file
