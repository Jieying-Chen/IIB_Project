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
        if self.intensity_sign == 'ppp':
            return 1
        elif self.intensity_sign == 'pp':
            return 2
        elif self.intensity_sign == 'p':
            return 3
        elif self.intensity_sign == 'mp':
            return 4
        elif self.intensity_sign == 'mf':
            return 5
        elif self.intensity_sign == 'f':
            return 6
        elif self.intensity_sign == 'ff':
            return 7
        elif self.intensity_sign == 'fff':
            return 8
        return False
            

    

#Separate notes into C major and Gb major
def separate_majors(notes):
    major1 = [1,3,4,6,8,9,11]
    major2 = [0,2,3,5,7,9,10]

    for note in notes:
        #print(note)
        seq = note.pitch % 12
        #print(seq)
        if (seq in major1) and (seq not in major2):
            note.major = 1
        elif (seq in major2) and (seq not in major1):
            note.major = 2

    i = 0
    for note in notes:
        if note.major == 'None':
            if i % 2 == 0:
                note.major = 1
            else:
                note.major = 2
            i+=1
    return 


def get_intensity(cur_key, cur_freq, notes_list):
    wave_freq = notes_list[cur_key-1]
    if cur_key == 1:
        sigma = notes_list[1]-notes_list[0]
    else:
        sigma = notes_list[cur_key-1]-notes_list[cur_key-2]
    sigma = sigma/2
    intensity = np.exp(-0.5 *((cur_freq-wave_freq)/sigma)**2)
    return intensity


def intensity2sign(intensity):
    thresholds = [35,55,75]
    # threshold0 = [0.67,0.77,0.89]
    if intensity < thresholds[0]:
        return 'p'
    elif intensity < thresholds[1]:
        return 'mp'
    elif intensity < thresholds[2]:
        return 'mf'
    else:
        return 'f'
        

def picknotes(cur_key, cur_freq, cur_int, notes, notes_list):
    j = 0
    while j < len(cur_key):
        if cur_key[j] == 0:
            j += 1
            continue

        pitch = cur_key[j]
        while pitch > 88:
            pitch -= 12
        
        start = j
        ori_int = cur_int[j]
        while cur_key[j] != 0 and j < len(cur_key)-1:
            j += 1
            ori_int = max(ori_int,cur_int[j])
        end = j - 1

        if end - start < 2: 
            end = start + 2 #all to 75ms
        
        intensity = get_intensity(cur_key[j-1],cur_freq,notes_list) * ori_int
        intensity_sign = intensity2sign(intensity)
        
        notes.append(Note(pitch, start, end, intensity, intensity_sign))
        j += 1
    return notes


def remove_repetitive(notes,note_num):
    #changed
    note_set = [0]*note_num
    i = 0
    while i < len(notes):
        note = notes[i]
        if note_set[note.pitch-1] == 0:
            note_set[note.pitch-1] = [note]
        else:
            delete = False
            for n in note_set[note.pitch-1]:
                if n.start == note.start and n.end == note.end:
                    n.intensity = max(n.intensity, note.intensity)
                    n.intensity_sign = intensity2sign(n.intensity)
                    del notes[i]
                    delete = True
                    i -= 1
                    break
            if not delete:
                note_set[note.pitch-1].append(note)
        i += 1
    return notes


def separate_word(notes,word_gap):
    word_list = []
    ptr = 0
    for i in range(len(notes)-1):
        if notes[i+1].start - notes[i].end >= word_gap:
            word_list.append(notes[ptr:i+1])
            ptr = i + 1
        if i == len(notes) - 2:
            word_list.append(notes[ptr:])
    return word_list


def multichannel(notes,note_num):    
    notes = sorted(notes, key = lambda note: (note.pitch, note.start, note.end))
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
                    ##WARNING: BURTAL FIX!!! Fix method: use a stack
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
