import re
import numpy as np


# Functions to deal with notes as integers vs names

def int_to_note(i):
    """ Function that converts note from integer to name
    Args:
        i: integer value corresponding to note
    Returns:
        note: note name, eg. "C4" 
    """
    
    # convert integer to note
    notes = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    return notes[i%12] + str(i//12 - 1)

def note_to_int(note):
    """ Function that converts note from name to integer
    Args:
        note: note name, eg. "C4"
    Returns:
        i: integer value corresponding to note
    """
    
    # convert integer to note
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    note = temp.match(note).groups()
    notes = {'C':0,'C#/Db':1,'C#':1,'Db':1,'D':2,'D#/Eb':3,'D#':3,'Eb':3,'E':4,'F':5,'F#/Gb':6,'F#':6,'Gb':6,'G':7,'G#/Ab':8,'Ab':8,'G#':8,'A':9,'A#/Bb':10,'A#':10,'Bb':10,'B':11}
    return notes[note[0]] + 12*(int(note[1])+1)

# Other helper Functions

def time_to_index(notes, timestamp):
    for i in range(len(notes)): # make binary search!
        if notes[i][0] >= timestamp:
            return i
        
def index_to_time(notes, index):
    return notes[index][0]

def time_to_sequence(notes, times): # assume start>end & not include start for convention
    start, end = times
    i = time_to_index(notes, end)
    sequence = []
    while i < len(notes): # make binary search!
        if notes[i][0]>=start:
            break
        sequence.append(notes[i])
        i += 1
    return sequence

def find_note(notes, time, note_val, max_time_dist = 10000):
    note_id = time_to_index(notes,time)
    op1 = None
    op2 = None
    
    end = time_to_index(notes,min(time+max_time_dist,notes[-1][0]))-1
    # checking forward
    for i in range(note_id,end):
        if notes[i][1] == note_val:
            if abs(notes[i][0]-time) > max_time_dist:
                print("UP",abs(notes[i][0]-time))
            op1 = i
            break
    
    end = time_to_index(notes,max(time-max_time_dist,0))
    # checking reverse
    for i in range(note_id-1,end,-1):
        if notes[i][1] == note_val:
            if abs(notes[i][0]-time) > max_time_dist:
                print("DOWN",abs(notes[i][0]-time),time,time-max_time_dist,note_id,end,i)
            op2 = i
            break
    
    if not op1:
        return op2
    if not op2:
        return op1
    if abs(notes[op1][0]-time) < abs(time-notes[op2][0]):
        return op1
    return op2

