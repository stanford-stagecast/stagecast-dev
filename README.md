# stagecast-dev

Audio files:
https://drive.google.com/drive/folders/1od362nowNgFYGuFFoTXKdnKb_01Ju9HH?usp=sharing


## Nomenclature:
- **Input:** .txt midi_file with each line having for hex nubmers: 1) timestamp, 2) event type (eg. note on), 3) note value, 4) velocity.
- **Notes:** Input file is converted to an array of tuples [timestamp, note, velocity].
- **Curr Time:** The assumed "present" time if we were running in real time. The time at which we need to a find a match, and prediction. (in ms)
- **History:** Timestamps 0 to Curr Time - 5 seconds.
- **Source Snippet:** Snippet of notes leading up to Curr Time for which we are searching for a match in the History.
- **Target Snippet:** Snippet of notes in History that are a potential match for Source Snippet.
- **Source Time:** Same as Curr Time. Timestamp at which Source Snippet ends. (in ms)
- **Source Start:** Same as Curr Time. Timestamp at which Source Snippet ends. (in ms)
- **Source End:** Time at which Source Snippet starts. Timestamp of first note in Source Snippet. (in ms) Note that Source End < Source Start
- **Source Id Start:** Index to notes array for the first note **after** Source Start. This note is **not** included in the Source Snippet.
- **Source Id End:** Index to notes array for the **first** note in Source Snippet. Note that Source Id End < Source Id Start
- **Target Time:** Timestamp at which target snippet ends. (in ms)
- **Target Start:** Same as Target Time. Timestamp at which target snippet ends. (in ms)
- **Target End:** Time at which Target Snippet starts. Timestamp of first note in Target Snippet. (in ms) Note that Target End < Target Start
- **Target Id Start:** Index to notes array for the first note **after** Target Start. This note is **not** included in the Target Snippet.
- **Target Id End:** Index to notes array for the **first** note in Target Snippet. Note that Target Id End < Target Id Start

## Important plots:

#### Scatter plot of the best match found for every 10ms in second playthrough of La Dispute. Source times are timestamps in the second playthrough and target times are timestamps of the matches found (expected to follow first playthrough exactly):

<img width="934" alt="Screenshot 2023-05-02 at 7 25 32 PM" src="https://user-images.githubusercontent.com/54175817/236644187-df92409d-89da-46f1-ba56-8f2e835c5341.png">


#### Histogram of deviation in time of matched snippet as compared to the "expected time":

  - Distribution Mean:-1.49
  - Distribution Standard Deviation:9.17

<img width="905" alt="Screenshot 2023-05-02 at 7 25 40 PM" src="https://user-images.githubusercontent.com/54175817/236644197-8e0b0b5a-fe5a-4d6d-9c2d-f3689d9f7f3c.png">


#### Plot showing deviation in time of matched snippet as compared to the "expected time" against source timestamp:

<img width="1135" alt="Screenshot 2023-05-02 at 7 26 02 PM" src="https://user-images.githubusercontent.com/54175817/236644258-add15e76-fd89-43c6-ad8d-d3104ba51546.png">


#### Plots showing alignment of the worst match with expected and actual:

<img width="1078" alt="Screenshot 2023-05-03 at 5 18 42 PM" src="https://user-images.githubusercontent.com/54175817/236644294-774f9bbc-6fab-4282-ae54-75eb025a6f88.png">
<img width="1072" alt="Screenshot 2023-05-03 at 5 18 49 PM" src="https://user-images.githubusercontent.com/54175817/236644299-ba17a4e3-a267-4b14-a452-befe16f86e46.png">


##### Steps to reproduce:

1. Clone this repository
2. Check that you have all the requirements in requirements.txt
3. Download ladispute.txt from [here](https://github.com/stanford-stagecast/midi-recordings) and update path in Testing_Score_time_v8_speeding_target.ipynb
4. Run all cells in Testing_Score_time_v8_speeding_target.ipynb
5. The last few plots will give you the plots for besgt match, distribution of match timestamps, score of best match and length in ms and notes.
6. Modify filepath and start skip and end parameters to test for different midi files and sections.



