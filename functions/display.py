import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt


#  Functions to help judge quality of match

def play_match(piano_audio, source_start, source_end, target_start, target_end, pausebetween=False):
    """ Function that plays portion of audio file corresponding to each sequence of a match
    Args:
        source_start: 
        source_end: 
        target_start: 
        target_end: 
    """
    
    ss = (source_start * samplerate) // 1000
    se = (source_end * samplerate) // 1000
    te = (target_end * samplerate) // 1000
    ts = (target_start * samplerate) // 1000
    #Source
    sd.play(piano_audio[se:ss], samplerate, blocking = True)
    if pausebetween:
        time.sleep(1)
    #Target
    sd.play(piano_audio[te:ts], samplerate, blocking = True)
    if pausebetween:
        time.sleep(1)
        
def display_snippet_plot(notes, source_start, source_end, target_start, target_end, score, sourceStart, targetStart):
    plt.figure(figsize = (10,5))
    lenSource = source_start-source_end
    lenTarget = target_start-target_end
    timeStampSourceEnd = notes[(lenSource - 1)+source_end][0]-sourceStart
    timeStampTargetEnd = notes[(lenTarget - 1)+target_end][0]-targetStart

    if timeStampSourceEnd >= timeStampTargetEnd:
        xmax = timeStampSourceEnd
    else:
        xmax = timeStampTargetEnd

#     plt.xlim(0,xmax)
    plt.xlabel("Relative Snippet Time (in MS)")
    # yscale = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    # plt.yticks(range(0,len(yscale)),yscale)
    plt.ylabel("Note (Integer Representation)")
    title = "Snippet Plot:" + ", Source @ " + str(notes[source_end][0]) + " ms, Target @ " + str(notes[target_end][0]) + " ms, Score: " + str(round(score,4))
    plt.title(title)
    plt.locator_params(axis="both", integer=True, tight=True)

    sourceX = []
    sourceY = []
    targetX = []
    targetY = []
    for i in range(min(source_start-source_end, target_start-target_end)):
        sourceX.append(notes[i+source_end][0]-sourceStart)
        sourceY.append((notes[i+source_end][1]))
        targetX.append(notes[i+target_end][0]-targetStart)
        targetY.append((notes[i+target_end][1]))
    for i in range(target_start-target_end, source_start-source_end):
        sourceX.append(notes[i+source_end][0]-sourceStart)
        sourceY.append((notes[i+source_end][1]))
    for i in range(source_start-source_end, target_start-target_end):
        targetX.append(notes[i+target_end][0]-targetStart)
        targetY.append((notes[i+target_end][1]))

    plt.scatter(sourceX, sourceY, label="Source",marker='*')
    plt.scatter(targetX, targetY, label="Target",marker='.')
    plt.legend()
    plt.show()

def display_snippet_plot_2(sequence_source,sequence_target,source_start,target_start,score=0,time_ratio=1):
#     plt.figure(figsize = (10,5))

#     plt.xlim(0,xmax)
    plt.xlabel("Relative Snippet Time (in MS)")
    # yscale = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    # plt.yticks(range(0,len(yscale)),yscale)
    plt.ylabel("Note (Integer Representation)")
    plt.locator_params(axis="both", integer=True, tight=True)

    sourceX = [] # x axis - source timestamp in ms
    sourceY = [] # y axis - note integer repr for source
    targetX = []
    targetY = []
    for i in range(len(sequence_source)):
        sourceX.append(sequence_source[i][0]*time_ratio)
        sourceY.append(sequence_source[i][1])

    for i in range(len(sequence_target)):
        targetX.append(sequence_target[i][0])
        targetY.append(sequence_target[i][1])

    title = "Snippet Plot:" + ", Source @ " + str(source_start) + " ms, Target @ " + \
        str(target_start) + " ms, Score: " + str(score) + ", Length (ms): "+ str(sourceX[-1]-sourceX[0])
    plt.title(title)
    plt.scatter(sourceX, sourceY, label="Source",marker='*')
    plt.scatter(targetX, targetY, label="Target",marker='.')
    plt.legend()
    plt.show()
    

def display_expected_actual(sequence_source,sequence_target,source_start,target_start,t1,t2,t3,diff,score,lent,l1="Source",l2="Matching Target",l3="Expected Target"):
    fig, ax1 = plt.subplots()

    sourceX = [] # x axis - source timestamp in ms
    sourceY = [] # y axis - note integer repr for source
    targetX = []
    targetY = []
    for i in range(len(sequence_source)):
        sourceX.append(sequence_source[i][0])
        sourceY.append(sequence_source[i][1])

    for i in range(len(sequence_target)):
        targetX.append(sequence_target[i][0])
        targetY.append(sequence_target[i][1])
        
    def s2t(x):
        return x+diff
    def t2s(x):
        return x-diff
    
    ax1.plot(np.full(2, t1),[0,88],linewidth=3, label=l1)
    ax1.plot(np.full(2, t2),[0,88], label=l2)
    ax1.plot(np.full(2, t3),[0,88], label=l3)
    ax1.scatter(sourceX, sourceY, marker='*')
    ax1.scatter(targetX, targetY, marker='.')

    title = "Snippet Plot: Source @ {:d} ms, Target @ {:d} ms, Score: {:.2f}, Length (ms): {:d}\
    ".format(source_start,target_start,score,lent)
    
    secax = ax1.secondary_xaxis('top', functions=(s2t, t2s))
    fig.tight_layout()
    plt.title(title)
    ax1.set_xlabel("Source Snippet Time (in ms)")
    secax.set_xlabel("Target Snippet Time (in ms)")
    ax1.set_ylabel("Note (Integer Representation)")
    ax1.legend()
    plt.show()








  