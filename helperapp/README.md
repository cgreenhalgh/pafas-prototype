# PAFAS pythong helper app

Aims:
- read pre-recorded data files and 'play' them
- read live data from real sensors (HR, pupil dilation)
- device significant measures (e.g. HR, RMSSD, breathing rate, RSA)
- send data to sonification apps (i.e. via MIDI or OSC)

Status: just starting

## Installation

Install 
[miniconda](https://docs.conda.io/en/latest/miniconda.html).
Then, in a terminal, 
```
conda create -n pafas
source activate pafas
```
Install dependencies,
```
conda install numpy
```

Run:
```
python pafas/app/main.py
```


## Requirements

- "main" UI 
  - inputs
    - file (select)
    - heartrate / empatica
    - pupil / eye tracker
  - output(s)
  - main controls: go, stop; rewind(?); reset(?)
  - status
- "settings" UI 
  - configure sensors?
  - configure output?

## Data files

### Matlab export format

These are the example text export files from Elizabeth, e.g. 
[data/S014.txt](data/S014.txt).

Ignoring blank lines:
```
S014
Breaths/Minute: 10.08
Block 1
R wave timestamps
1377
...
Inhale marker timestamps
2
...
Block 2
R wave timestamps
1223
...
Block 3
...
```
Numbers are timestamps in ms from start of session/file/block.
Each block is independent, so block needs to be selected, either on open,
in settings or in main UI.
