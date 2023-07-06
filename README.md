# Epistemic Preferences

A study into adding preferences (or soft goals) into the RP-MEP epistemic planning framework.

## Usage

First, build the (minimal) docker image:

```bash
docker build -t epistemic-preferences .
```

Next, enter a container with the local files accessible:

```bash
docker run -it --privileged -v $(pwd):/root/PROJECT --rm --name epistemic-preferences epistemic-preferences
```

To run the experiments from the paper:
```bash
./runall.sh
```
This will create two new directories, runs30 and and data30 (the "30" refers to the 30 second search time limit used by the experiments). You can then extract the results into a JSON file by running
```bash
python3 extract.py --time 30
```

You can also run the experiments without a time limit:
```bash
./runall_notimelimit.sh
python3 extract.py
```
This is slow and uses a lot of memory (with no time limit, it was not possible to complete all the experiments on a system with 128 GB of RAM).


## Requirements
Just Docker.

## Experimental Results

The data used to construct the table in the paper is in [data30.json](data30.json). The compilation times can be seen in [output30.txt](output30.txt). Note that the first compilation time for each problem is the RP-MEP compilation time; the times for adding the different preferences types correspond to the Keyder-Geffner compilations.

Additionally, experiments were run with no time limit for LAMA (the planner); the results are described in [tables-longer.pdf](tables-longer.pdf). This is how we were in some cases able to determine what results in the paper were (sub)optimal.


## Credits

This repository was created by Christian Muise and Toryn Q. Klassen. It corresponds to the following paper at [KR 2023](https://kr.org/KR2023/):


```
@inproceedings{KlassenKR2023epistemic,
    author    = {Toryn Q. Klassen and Christian Muise and Sheila A. McIlraith},
    title     = {Planning with Epistemic Preferences},
    booktitle = {Proceedings of the 20th International Conference on Principles of Knowledge Representation and Reasoning},
    note      = {To appear},
    year      = {2023}
}
```

A version also appears at the [HAXP workshop](https://icaps23.icaps-conference.org/program/workshops/haxp/) at [ICAPS 2023](https://icaps23.icaps-conference.org/):

```
@inproceedings{KlassenHAXP2023epistemic,
    author    = {Toryn Q. Klassen and Christian Muise and Sheila A. McIlraith},
    title     = {Towards Human-Aware {AI} via Planning with Epistemic Preferences},
    booktitle = {Human-Aware and Explainable Planning (HAXP): ICAPS'23 Workshop},
    year      = {2023},
    url       = {https://openreview.net/pdf?id=nkn1rcI6wd}
}
```

