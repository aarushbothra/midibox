from dataclasses import dataclass
from mido import MidiFile
import pretty_midi
import ezdxf
from ezdxf import units
import os

#name of midi file to be processed. Name gets reused as dxf file name. Must be in subdirectory "midi/" in the same directory as python file 
docName = 'midi/Avery_part-2_12-8-24.mid'

#all units in mm
distance_between_beats = 10
bottom_padding = 5.6 #distance between bottom of strip and lowest note
vertical_distance_between_notes = 2.00 #distance between each note on the strip vertically
strip_height = 70.0 #height of the strip entering music box
paper_lead = 150.0 #distance between start of strip and start of music
hole_size = 0.9

paper_max_width = 13.7*25.4 #max horizontal width of paper being cut
paper_max_height = 10.9*25.4 #max vertical height of paper being cut

#list of notes currently available on music box
note_names_available = ['F3','G3','C4','D4','E4','F4','G4','A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5','C6','C#6','D6','D#6','E6','F6','G6','A6']

# -----------------------------------------END OF GLOBALS----------------------------------------------------------

def main():
    mid = MidiFile(docName)

    #all midi note on and off events
    note_positions_unclean = []

    @dataclass
    class note:
        note_name: int
        x: float #vertical position of note on reel (corresponds with note name)
        y: float #horizontal position of note on reel (corresponds with time)
        msg_type: str
        velocity: int

    total_time = 0
    for msg in mid:
        if msg.type == 'note_on' or msg.type == 'note_off':
            total_time += msg.time
            x = -1
            if pretty_midi.note_number_to_name(msg.note) in note_names_available:
                x = (note_names_available.index(pretty_midi.note_number_to_name(msg.note))*vertical_distance_between_notes)+bottom_padding
            else:
                print("Note unavailable:", pretty_midi.note_number_to_name(msg.note))
            note_positions_unclean.append(note(msg.note,x,total_time*distance_between_beats*2,msg.type,msg.velocity))

  
    note_positions = list(filter(lambda item: item.velocity != 0 and item.x != -1 and item.msg_type != 'note_off', note_positions_unclean)) #remove midi notes represent the end of notes or don't exist in note_names_available

    print("Notes:", len(note_positions))
    docs = []
    heightOffset = 0
    widthOffset = 0
    strip_number = 0
    i = 0

    while i<len(note_positions):
        docs.append(ezdxf.new())
        docs[-1].units = units.MM
        mspLines = docs[-1].modelspace()
        mspCircles = docs[-1].modelspace()
        docs[-1].layers.add(name="Numbers", color=1)

        heightOffset = 0

        while(heightOffset+strip_height < paper_max_height and i < len(note_positions)):

            #add note holes
            y_position = 0
            while(i < len(note_positions) and y_position < paper_max_width):
                y_position = note_positions[i].y-widthOffset+paper_lead
                if y_position < paper_max_width:
                    mspCircles.add_circle(((y_position), note_positions[i].x+heightOffset),hole_size).rgb = (255, 0, 0)
                    i += 1
            
            #add strip number to bottom corner
            number = mspLines.add_text(strip_number).set_placement(
                (2, 3+heightOffset)
            )

            number.dxf.layer = "Numbers"

            if (strip_number == 0):
                #left diagonal
                mspLines.add_line((0, heightOffset), (0, strip_height/2.5+heightOffset)).rgb = (255, 0, 0)
                mspLines.add_line((0,strip_height/2.5+heightOffset), (10,strip_height+heightOffset)).rgb = (255, 0, 0)
            else:
                #left line
                mspLines.add_line((0, heightOffset), (0, strip_height+heightOffset)).rgb = (255, 0, 0)
            
            #bottom line
            mspLines.add_line((0, heightOffset), (paper_max_width, heightOffset)).rgb = (255, 0, 0)

            #right diagonal
            # mspLines.add_line((paper_max_width-10, heightOffset), (paper_max_width-10, strip_height/2.5+heightOffset)).rgb = (255, 0, 0)
            # mspLines.add_line((paper_max_width-10, strip_height/2.5+heightOffset), (paper_max_width, strip_height+heightOffset)).rgb = (255, 0, 0)

            mspLines.add_line((paper_max_width, heightOffset), (paper_max_width, heightOffset+strip_height)).rgb = (255, 0, 0)

            #top line
            if (strip_number == 0):
                mspLines.add_line((10, heightOffset+strip_height), (paper_max_width, heightOffset+strip_height)).rgb = (255, 0, 0)
            else:
                mspLines.add_line((0, heightOffset+strip_height), (paper_max_width, heightOffset+strip_height)).rgb = (255, 0, 0)
            

            strip_number += 1
            heightOffset += strip_height
            widthOffset += paper_max_width

    print("Number of Strips:",strip_number,"\nNumber of Pages:",len(docs))

    #create and save dxf files
    os.mkdir(docName[5:-4] + '_dxf_files/')
    for i in range(len(docs)):
        docs[i].saveas(docName[5:-4] + '_dxf_files/' + docName[5:-4] + '_' + str(i) + '.dxf')

    

