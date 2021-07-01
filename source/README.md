# Task's Source Code Description

## Prerequisites

Clone the repository locally


Create a python virtual environment

```bash
python3 -m venv ../path/to/venv
```

or using the "virtualenv" package:
```bash
virtualenv ../path/to/venv
```

Activate the venv and install dependancies:
```bash
source /path/to/venv/bin/activate
```
open the project folder:
```bash
pip install -r requirements.txt
```

## About the Dataset

Extract the "The Beatles Annotations (beat, chord, key).rar" file in the project.

Place the "/Beatles" folder in the project.

In the "/Beatles" folder of the extracted file, the necessary files for the project are placed in the corresponding folders, which are the "Beatles/Beat", "Beatles/Chordlab" and "Beatles/Key"


### File pre processing

Beat and keylab files have to be transformed from .lab to .txt.
The corresponding function ("lab_to_txt()") is included in each script and operates when it is necessary.


## Beat to Chord Assignment
(Script [assignBeatsToChords.py](assignBeatsToChords.py))

### 1. Beat Processing and enrichment

Beat files data processing

1. Retrieve time signature and characterise track time periods.

2. Calculate beat mean duration (from beat file, for each track)

3. Corresponding time signature zones are defined. (beatRateZone() Function)


### 2. Chord Processing and enrichment

Chord record enrichment

1. Calculate actual duration of a chord based on chord .txt file.

2. Find the corresponding signature zone for the chord (based on the Beat rate zone from above).

3. Calculate bar duration for each chord (int and frac part) with the findChordMeasure() function.

4. Characterise bar’s time signature.

5. Define a new chord Class with the enriched data.

## Key to Chord Assignment

(Script [assign_key_to_chords.py](assign_key_to_chords.py))

1. Retrieve key for each song.

2. Calculate the key for every time period.

3. Match each chord to the corresponding key.

## Convert Chords

(Script [convert_chords.py](convert_chords.py))

This script is used in order to keep only triads and tetrads.

## Convert Names

(Script [convert_to_names.py](convert_to_names.py))

This script is used to remove '.txt' from each song, so we can define our ontology instances.

## Convert Songs to RDF files

### 1. Beat enriched data

(Script [convert_chord_beats_to_rdf.py](convert_chord_beats_to_rdf.py))

1. Define the data properties (hasBars, hasTimeSignature) of our ontology.

2. Add every chord and its corresponding data property values to a graph.

### 2. Key enriched data

(Script [convert_chord_degrees_to_rdf.py](convert_chord_degrees_to_rdf.py))

1. Define the object properties (hasNext, hasPrevious, hasKey) of our ontology.

2. Add every chord and its corresponding object property values to a graph.

### Ontology

More info about the ontology can be found [here](../ontology).

## Authors

* **Giannis Dimolitsas** - [jdimol](https://github.com/jdimol)
* **Spyros Kantarelis**  - [spyroskantarelis](https://github.com/spyroskantarelis)
