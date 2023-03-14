# stagecast-dev

Audio files:
https://drive.google.com/drive/folders/1od362nowNgFYGuFFoTXKdnKb_01Ju9HH?usp=sharing


## Important plots:

#### Scatter plot of the best match found for every 10ms in second playthrough of La Dispute. Source times are timestamps in the second playthrough and target times are timestamps of the matches found (expected to follow first playthrough exactly):

<img width="829" alt="Screen Shot 2023-03-09 at 12 47 59 AM" src="https://user-images.githubusercontent.com/54175817/225159356-3c9a47c3-ed39-41dc-be26-346d8f1b5d9b.png">


#### Histogram of deviation in time of matched snippet as compared to the "expected time":

  - Distribution Mean:-1.71
  - Distribution Standard Deviation:33.14

<img width="838" alt="Screen-Shot-2023-03-11-at-4 30 50-PM" src="https://user-images.githubusercontent.com/54175817/225158907-7194c8b1-795b-448b-a11e-c6b2b92292d9.png">


#### Histogram of deviation in time of note down events in second playthrough as compared to the "expected time" (notedown time of first playthrough + time_diff):

<img width="830" alt="Screen Shot 2023-03-14 at 3 36 46 PM" src="https://user-images.githubusercontent.com/54175817/225159191-8478d0a3-41ce-43e7-a5a2-c639e162f4af.png">



##### Steps to reproduce:

1. Clone this repository
2. Check that you have all the requirements in requirements.txt
3. Download ladispute.txt from [here](https://github.com/stanford-stagecast/midi-recordings) and update path in Testing_Score_time_v5_fixing_percentage_target_timestamps.ipynb
4. Run all cells in Testing_Score_time_v5_fixing_percentage_target_timestamps.ipynb
5. The last few plots will give you the plots for besgt match, distribution of match timestamps, score of best match and length in ms and notes.
6. Modify filepath and start skip and end parameters to test for different midi files and sections.



