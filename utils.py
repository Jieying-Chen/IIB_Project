import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from midiutil import MIDIFile
from pprint import pprint


class Note:
    def __init__(self, pitch, start, end, intensity_sign, intensity, channel = -1):
        self.pitch = pitch
        self.start = start
        self.end = end
        self.intensity_sign = intensity_sign
        self.intensity = intensity
        self.channel = channel

    def __repr__(self):
        return f"pitch = {self.pitch}(time = {self.start}-{self.end}), intensity sign = {self.intensity_sign}, intensity = {self.intensity:.3f}, channel = {self.channel}"

    def sign(self):
        if self.intensity_sign == 'p':
            return 1
        elif self.intensity_sign == 'mp':
            return 2
        elif self.intensity_sign == 'mf':
            return 3
        elif self.intensity_sign == 'f':
            return 4

    
#Separate notes into C major and Gb major
def separate_majors(notes):
    C_major = [1,3,4,6,8,9,11]
    Gb_major = [0,2,3,5,7,9,10]

    C_notes = []
    Gb_notes = []

    for i,note in enumerate(notes):
        seq = note.pitch % 12
        if (seq in C_major) and (seq not in Gb_major):
            C_notes.append(notes.pop(i))
        elif (seq in Gb_major) and (seq not in C_major):
            Gb_notes.append(notes.pop(i))
    counter = len(notes)
    while counter > 0:
        if counter % 2 == 0:
            C_notes.append(notes.pop(0))
        else:
            Gb_notes.append(notes.pop(0))
        counter -= 1
    return [C_notes, Gb_notes]



## visualization tool
def plot_notes(note_list):
    time =[]
    pitch = []
    for note in note_list:
        time.append(note.start)
        pitch.append(note.pitch)
    plt.scatter(time,pitch,s=1)

def print_list(l):
    for item in l:
        print(item)
