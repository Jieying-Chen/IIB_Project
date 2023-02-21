import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from midiutil import MIDIFile
from pprint import pprint


class Note:
    def __init__(self, pitch, start, end, intensity, intensity_sign = ' ', major = 'None', channel = -1):
        self.pitch = pitch
        self.start = start
        self.end = end
        self.intensity_sign = intensity_sign
        self.intensity = intensity
        self.major = major
        self.channel = channel

    def __repr__(self):
        return f"pitch = {self.pitch}(time = {self.start}-{self.end}), intensity sign = {self.intensity_sign}, intensity = {self.intensity:.3f}, major = {self.major}, channel = {self.channel}"

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
    major1 = [1,3,4,6,8,9,11]
    major2 = [0,2,3,5,7,9,10]

    # C_notes = []
    # Gb_notes = []

    len_all = len(notes)

    i = 0
    while i < len(notes):
        note = notes[i]
        seq = note.pitch % 12
        if (seq in major1) and (seq not in major2):
            note.major = 1
            notes.remove(note)
            #C_notes.append(notes.pop(i))
            i -= 1
        elif (seq in major1) and (seq not in major2):
            note.major = 2
            notes.remove(note)
            #Gb_notes.append(notes.pop(i))
            i -= 1
        i += 1


    j = len(notes)
    while j > 0:
        #print(notes[0].pitch % 12)
        if j % 2 == 0:
            note.major = 1
            notes.remove(note)
            #C_notes.append(notes.pop(0))
        else:
            note.major = 2
            notes.remove(note)
            #Gb_notes.append(notes.pop(0))
        j -= 1
    return 


def get_intensity(cur_key, cur_freq, notes_list):
    wave_freq = notes_list[cur_key-1]
    if cur_key == 1:
        sigma = notes_list[1]-notes_list[0]
    else:
        sigma = notes_list[cur_key-1]-notes_list[cur_key-2]
    sigma = sigma/2
    intensity = np.exp(-0.5 *((cur_freq-wave_freq)/sigma)**2)
    #print('cur', cur_freq,'wave',wave_freq)
    return intensity


def intensity2sign(intensity):
    #changed
    if intensity < 0.67:
        return 'p'
    elif intensity < 0.77:
        return 'mp'
    elif intensity < 0.89:
        return 'mf'
    else:
        return 'f'
        

def picknotes(cur_key, cur_freq, notes, notes_list):
    #changed
    j = 0
    while j < len(cur_key):
        if cur_key[j] != 0:
            if cur_key[j] > 88:
                pitch = cur_key[j] - 12
            else:
                pitch = cur_key[j]
            start = j
            while cur_key[j] != 0 and j < len(cur_key)-1:
                j += 1
            intensity = get_intensity(cur_key[j-1],cur_freq,notes_list)
            intensity_sign = intensity2sign(intensity)
            notes.append(Note(pitch, start, j - 1, intensity, intensity_sign))
        j += 1
    return notes


def remove_repetitive(notes,note_num):
    #changed
    note_set = [0]*note_num
    i = 0
    while i < len(notes):
        note = notes[i]
        if note_set[note.pitch-1] == 0:
            note_set[note.pitch-1] = [(note.start,note.end)]
        else:
            if (note.start,note.end) in note_set[note.pitch-1]:
                del notes[i]
                i -= 1
            else:
                note_set[note.pitch-1].append((note.start,note.end))
        i += 1
    return notes


def multichannel(notes,note_num):    
    channel = [0]*note_num
    start_time = [-1]*note_num
    for note in notes:
        if channel[note.pitch-1]==0:
            start_time[note.pitch-1]=note.start
            note.channel=channel[note.pitch-1]
            channel[note.pitch-1] += 1
        else:
            if note.start - start_time[note.pitch-1] < 10:
                if channel[note.pitch-1] == 16:
                    ##WARNING: BURTAL FIX!!!
                    channel[note.pitch-1] = 0
                    start_time[note.pitch-1]=note.start
                    note.channel=channel[note.pitch-1]
                    channel[note.pitch-1] += 1
                else:
                    note.channel=channel[note.pitch-1]
                    channel[note.pitch-1] += 1
            else:
                channel[note.pitch-1] = 0
                start_time[note.pitch-1]=note.start
                note.channel=channel[note.pitch-1]
                channel[note.pitch-1] += 1
    return notes


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
