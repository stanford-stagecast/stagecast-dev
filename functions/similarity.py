import numpy as np


# Functions to calculate similarity

def two_way_similarity(tf1,tf2,zero_penalty=1,length_incentive=500000,max_offset=600,min_dist_const=400,disp=False):
    a1,b1,c1,d1,score1 = musical_similarity(tf1,tf2,disp)
    b2,a2,d2,c2,score2 = musical_similarity(tf2,tf1,disp)
    if score1>score2:
        return a1,b1,c1,d1,score1
    return a2,b2,c2,d2,score2

def musical_similarity(tf1,tf2,zero_penalty=1,length_incentive=500000,max_offset=600,min_dist_const=400,disp=False):
    """ Function that calculates similarity score between 2 snippets 
        eg [[-17,60],[-100,62],[-101,64],[-300,60]] and [[-20,60],[-50,61],[-101,64],[-102,62],[-307,60]]
    
    Args:
        tf1: first snippet [[t,note],[t,note],[t,note],...]. Each element may also have a third parameter "velocity" which will be ignored
        tf2: second snippet [[t,note],[t,note],[t,note],...]. Each element may also have a third parameter "velocity" which will be ignored
    
    Returns:
        lastmatch1: index of tf1 corresponding to last matching note between tf1 and tf2
        lastmatch2: index of tf2 corresponding to last matching note between tf1 and tf2
        mean_offset1: mean time dist between matching notes of 2 snippets (wrt last note being matched)
        mean_offset2: should be -mean_offset1
        score: similarity - integer between 0 to 1
    
    """
    
    # TO dO: 
    # 1) trim unmatched ends of both snips before penalizing 0 scores
    # 2) penalize 0 scores more
    # 3) fix scaling
    
#     pdb.set_trace()
    
    tf1 = np.array(tf1)
    tf2 = np.array(tf2)
    
    # updating time stamps wrt first note for tf1
    sequence1 = tf1
    sequence1[:,0] = tf1[:,0]-tf1[-1,0]
    
    # updating time stamps wrt first note for tf2
    ind = np.argwhere(tf2[:,1] == tf1[-1,1])
    if ind.any():
        ind = ind[-1]
        lastmatch1 = tf1.shape[0]-1
        lastmatch2 = int(ind[0])
        mo = tf2[-1,0]-tf2[ind,0]
        if type(lastmatch1) != int or type(lastmatch2) != int:
            print(type(lastmatch1),type(lastmatch2))
        if (tf1[lastmatch1] != tf1[-1]).all():
            print("Error in lastmatch1:",lastmatch1)
    else:
        ind = -1
        lastmatch1 = None
        lastmatch2 = None
        mo = 0
    sequence2 = tf2
    sequence2[:,0] = tf2[:,0]-tf2[ind,0]
    
    seq_1_time_del = tf1[-1,0] - tf1[0,0]
    seq_2_time_del = tf2[-1,0] - tf2[0,0]
    
    time_ratio = (seq_2_time_del / seq_1_time_del) / len(tf1)
    
    # Calculating score array by comparing every note from each sequence and taking the best match
    scores, mean_offset1, mean_offset2 = note_similarity_vect2_mean(sequence1,sequence2,time_ratio*(np.arange(sequence2.shape[0],0,-1)))
    
    score = scores.max(axis=0)
    score2 = scores.max(axis=1)
    if lastmatch1 == None:
        lastmatch1, = np.nonzero(score)
        if lastmatch1.any():
            lastmatch1 = lastmatch1[-1]
        else:
            lastmatch1 = -1
        lastmatch2, = np.nonzero(score2)
        if lastmatch2.any():
            lastmatch2 = lastmatch2[-1]
        else:
            lastmatch2 = -1
    
    # For every pair of notes in both sequences, if a match was not found, add a zero score
    count_zeros = np.sum(score==0) * zero_penalty
    count_score = sequence1.shape[0] + sequence2.shape[0] + count_zeros - score.shape[0]
  
    # Similarity of the two sequences is the mean of the note similarity scores
    score_1 = np.sum(score)/(count_score)
    
    # including length in score, if at least 5 notes
    if len(tf1)>5:
        score_1 += score_1 * seq_1_time_del/length_incentive # 50 seconds yield 10% increase
    
    if disp:# and score_1>0.7:
        print("Scores:",score)
        print("Sequence1: ",sequence1)
        print("Sequence2: ",sequence2)
        print("mean_offset1: ", mean_offset1)
        print("mean_offset2: ", mean_offset2)
        print("mo: ", mo)
        print("Count zeros: ",count_zeros)
#         print("Matched vals: ",matched_targets)
        display_snippet_plot_2(sequence1,np.array(sequence2),tf1[0][0],tf2[0][0],score_1, 1)
    
    return lastmatch1, lastmatch2, mean_offset1-mo, mean_offset2+mo, score_1

def note_similarity_vect2_mean(sequence1,sequence2,ratio,max_offset=600,min_dist_const=400):
    """ Function that calculates similarity score between 2 notes - depending on note value and time.
        Score is linear with time difference between notes.
    
    Args:
        sequence1: first sequence of notes to compare [[t,note],..]
        sequence2: second sequence of notes to compare [[t,note],...]
        ratio: tempo ratio between two - not currently being used
         * These two are aligned at the last note and timestamp of every note in sequence is wrt last note
    
    Returns:
        score: similarity - integer between 0 to 1
    
    """
    
#     min_dist = 50 * ratio[:,None] # acceptable time difference for same note
    min_dist = min_dist_const #+ ratio[:,None] # acceptable time difference for same note
    
    time_diff = abs(sequence1[None,:,0] - sequence2[:,None,0]).astype(float)
    time_diff_sign = np.sign(sequence1[None,:,0] - sequence2[:,None,0]).astype(float)
    
    # re-aligning sequences
    offset = (sequence1[None,:,1] == sequence2[:,None,1]) * (time_diff) + (sequence1[None,:,1] != sequence2[:,None,1]) * 100000
    offset1 = offset.argmin(axis = 0)
    offset1 = np.diag(offset[offset1,:] * time_diff_sign[offset1,:]) * -1
    if len(np.nonzero(np.abs(offset1)<max_offset)[0]) == 0:
        offset1 = 0
    else:
        offset1 = np.sum(offset1[np.abs(offset1)<max_offset])/len(np.nonzero(np.abs(offset1)<max_offset)[0])
    offset2 = offset.argmin(axis = 1)
    offset2 = np.diag(offset[:,offset2] * time_diff_sign[:,offset2])
    if len(np.nonzero(np.abs(offset2)<max_offset)[0]) == 0:
        offset2 = 0
    else:
        offset2 = np.sum(offset2[np.abs(offset2)<max_offset])/len(np.nonzero(np.abs(offset2)<max_offset)[0])
    sequence2[:,0] += int(offset2)
    
    # calculating score based on time difference between maching notes
    time_diff = abs(sequence1[None,:,0] - sequence2[:,None,0]).astype(float)
    op = (sequence1[None,:,1] == sequence2[:,None,1]) * ((time_diff) < (min_dist)) * (1 - (time_diff)/min_dist)
    
    return op,offset1,offset2
    
