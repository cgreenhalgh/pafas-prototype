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
