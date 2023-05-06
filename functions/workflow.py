import numpy as np
from similarity import two_way_similarity
from helper import *

from LSH import *
from collections import defaultdict


# Functions to execute workflow

def calculate_similarity_time(notes,hashed_notes,n,k,permutation,source_id,currTime,max_matches=None,timestamp_max_before_source=5000,zero_penalty=1,length_incentive=500000,max_offset=600,min_dist_const=400,skip = 100,disp=False):
    """ Function that calls musical similarity on targets generated for a source_id.
        Target snips start at every 100 ms, and has same time length as source.
    
    Args:
        notes: list of all notes from a recording [[t,note,vel],[t,note,vel],[t,note,vel],...]
        source_id: indices of note array corresponding to current time snippet (source_id_start>source_id_end) 
                   [source_id_start, source_id_end]
        currTime: time stamp at which we are searching for matches (ms)
        max_matches: optional param to state how many matches to stop after
        skip: interval at which to iterate over target timestamps
        disp: boolean whether to print each match (defaults True)
    
    Returns:
        matches: list of matches [[currTime, pastTime1, score1], [currTime, pastTime2, score2],...] 
    
    """
    
    matches = []
    last_id_end = 0 # track previous end index of target
    last_id_start = 0
    source_id_start, source_id_end = source_id
    source_end = notes[source_id_end][0] # start and end time stamps of source
    length_ms = currTime - source_end #in milliseconds
    
    target_start = length_ms
    while target_start < currTime-timestamp_max_before_source:
        # print("target_start: {}; currTime-timestamp_max_before_source: {}".format(target_start, currTime-timestamp_max_before_source))
        target_end = target_start - length_ms # pick target_end by time length of course snip
        # print(target_start, currTime-timestamp_max_before_source)
        # finding new end index
        for i in range(last_id_end,len(notes)):
            if notes[i][0] >= target_end:
                target_id_end = i
                break
             
        # finding new start index
        for i in range(target_id_end,len(notes)):
            if notes[i][0] > target_start:
                target_id_start = i
                break
                
        if target_id_end > target_id_start-4:
            last_id_end = target_id_end
            last_id_start = target_id_start
            target_start += skip
            continue
        if target_id_end == last_id_end and last_id_start == target_id_start:
            target_start += skip
            continue

        sample = notes[source_id_end:source_id_start][:,1]
        len_of_notes = len(sample)
        source_hash = get_hash(sample, n, len_of_notes, permutation)[0]
        # add to the dict
        if not hashed_notes[len_of_notes]:
            target_hash = get_hash(notes[:source_end,1], n, len_of_notes, permutation)
            hashed_notes[len_of_notes] = target_hash
        else: target_hash = hashed_notes[len_of_notes]
        indices = get_k_highest_scores(target_hash, source_hash, k)
        if source_id_start not in indices:
            last_id_end = target_id_end
            last_id_start = target_id_start
            target_start += skip
            continue
        
        lm1,lm2,mo1,mo2,score = two_way_similarity(notes[source_id_end:source_id_start], notes[target_id_end:target_id_start],zero_penalty=zero_penalty,length_incentive=length_incentive,max_offset=max_offset,min_dist_const=min_dist_const,disp=disp)
        
        if score:
            if score>0.7:
#                 count += 1
                # Dsiplaying matches > 0.7 if disp is True
                if disp:
                    display_snippet_plot(notes, source_id_start, source_id_end, target_id_start, target_id_end, score, source_end, notes[target_id_end][0])
                    # play_match(piano_audio, currTime, source_end, target_start, target_end)
                    # predict(notes, source_id_start, source_id_end, target_id_start, target_id_end, currTime, target_start)
                    # time.sleep(5)

            if score>0.5:
                target_time = target_start
                
                # case 1 - good alignment of source snippet
                if lm1 >= source_id_start - source_id_end - 2:
                    target_time = notes[target_id_start-1][0] + int(mo2) + (currTime - notes[source_id_start-1][0])
                
                # case 2 - run again with target slightly ahead?
                elif lm2 >= target_id_start - target_id_end - 2:
                    if currTime - notes[source_id_end+lm1][0] < 1:
                        print("oops something went wrong with time calculations - might end in infinite loop")
                    target_start += currTime - notes[source_id_end+lm1][0]
                    continue
                
                # In all cases where good score and we do not rerun,
                # Find optimal timestamp and store the match
                target_time = notes[target_id_start-1][0] - int(mo2) + (currTime - notes[source_id_start-1][0])    
                if target_time<currTime-5000:
                    matches.append([currTime, target_time, score, source_id_start, source_id_end, time_to_index(notes, target_time), target_id_end])
        
        last_id_end = target_id_end
        last_id_start = target_id_start
        target_start += skip
        
    return matches

def get_source_notes(notes, start_time, min_notes, max_notes, min_time):
    """ Function that ...
    
    Args:
        notes: array of all notes in a recording, where each note is [t,note,vel]
        start_time: start index of notes array - corresponding to current time
        min_notes: min number of notes for a valid sequence, integer
        max_notes: max note length for a snippet, integer
        min_time: min time length for a valid sequence, integer (ms)\
    
    Returns:
        matches: list of matches [[currTime, pastTime1, score1], [currTime, pastTime2, score2],...] 
    
    """
    start_index = np.argwhere(notes[:,0] > start_time)
    if start_index.any():
        start_index = start_index[0]
    else:
        print("Error: Start time too large")
        return np.array([None,None])
    
    if start_index<min_notes:
        return np.array([None,None])
    
    end_index = np.arange(start_index-min_notes, start_index - max_notes - 1, -1)
    ids = (start_time - notes[end_index,0] >= min_time) * end_index
    ids = ids[np.nonzero(ids)]
    if ids.any():
        source_id = np.array([start_index[0],ids[0]])
        return source_id
        
    return np.array([None,None])

def find_matches_at_timestamp(i,n,k,permutation,hashed_notes,notes,minNotes,minTime,maxNotes,maxTime,thresh,timestamp_max_before_source=5000,zero_penalty=1,length_incentive=500000,max_offset=600,min_dist_const=400,disp=False):
    """Function that finds similarity from lengths minNotes to maxNotes ...
    
    Args:
        i:
        notes:
        minNotes:
        minTime:
        maxNotes:
        maxTime:
        thresh:
        disp:
    
    Returns:
        sims_arr: np array of every match >0.5 found of the form -
            ['source_timestamp', 'target_timestamp','score',
            'source_id_start','source_id_end','target_id_start','target_id_end','match_len','match_time']
    
    """
    sims_arr = []
    print("\r",end="")
    print("i:",i,end="   ")
    offset = 500
    numSourceNotes = 0
    sourceTime = 0
    while sourceTime < maxTime and numSourceNotes < maxNotes:
        sourceId = get_source_notes(notes, i, minNotes, maxNotes, sourceTime+offset)
        if not sourceId.any():
            break

        # num notes in source snippet
        numSourceNotes = (sourceId[0] - sourceId[1])
        # total time in ms in source snippet
        sourceTime = i - notes[sourceId[1]][0]
        
        sim = calculate_similarity_time(notes,hashed_notes,n,k,permutation,sourceId,i,timestamp_max_before_source=timestamp_max_before_source,zero_penalty=zero_penalty,length_incentive=length_incentive,max_offset=max_offset,min_dist_const=min_dist_const,disp=disp)
        for match in sim:
            match.append(numSourceNotes)
            match.append(sourceTime)
        sims_arr.extend(sim)
        offset += 500

    return np.array(sims_arr)

