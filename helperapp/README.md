# PAFAS pythong helper app

Aims:
- read pre-recorded data files and 'play' them
- read live data from real sensors (HR, pupil dilation)
- device significant measures (e.g. HR, RMSSD, breathing rate, RSA)
- send data to sonification apps (i.e. via MIDI or OSC)

Status: just starting

## Installation

Install 
[Anaconda](https://docs.anaconda.com/anaconda/install/windows/) or
(for a more minimal but manual install, e.g. on MacOS) 
[miniconda](https://docs.conda.io/en/latest/miniconda.html).

Then, in a (Anaconda) terminal, 
```
conda create -n pafas
conda activate pafas
```
Install dependencies,
```
conda install numpy
```
you can check the version,
```
python --version
```
I'm currently "Python 3.10.4"

Run:
```
python pafas/app/main.py
```

## Usage

To use test data,
- press 'Load...' and select a Matlab text export data file
- (optionally) choose a different data block
- press 'Play'
- the 'light' at the end should flash on each heartbeat

## Design

### Requirements

- "main" UI 
  - inputs
    - file (select), "Block", go, stop/rewind
    - empatica link
    - pupil / eye tracker
  - status
    - heartrate beat, IBI
    - RMSSD, etc.
  - output(s)
  - main controls?: go, stop; rewind(?); reset(?)
- "settings" UI 
  - configure sensors?
  - configure output?

### Data files: Matlab export format

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

### MaxMSP notes

As of 2022-07-25 the Max patch is driven by MIDI note-on messages from a custom Matlab script
the Matlab script
- reads/replays the matlab data files
- calculates dervied measures
- does simple threshold-based classification
- send MIDI note messages accordingly

### Software design notes

general
- use Tkinter GUI (and hence timers and input device selection)
- try to separate out non-gui engine
- use Event class with listener/callbacks
- divide gui into Frames that can be slotted together

signal path - version 1 (heartbeat)
- heartbeat input - file or empatica bridge
- heartbeat monitor - with callback for gui status
- heartbeat analyser
- heartbeat classifier ? - simple thresholds, adaptive?, trained??
- MIDI output
