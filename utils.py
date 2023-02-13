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
        return f"pitch = {self.pitch}({self.start}, {self.end}), intensity sign = {self.intensity_sign}, intensity = {self.intensity:.3f}, channel = {self.channel}"

    def sign(self):
        if self.intensity_sign == 'p':
            return 1
        elif self.intensity_sign == 'mp':
            return 2
        elif self.intensity_sign == 'mf':
            return 3
        elif self.intensity_sign == 'f':
            return 4

    

## visualization tool
def plot_notes(note_list):
    time =[]
    pitch = []
    for note in note_list:
        time.append(note.start)
        pitch.append(note.pitch)
    plt.scatter(time,pitch,s=1)