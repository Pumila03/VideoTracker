# VideoTracker_G1

Tracking software that allows recording the positions of a moving object over time using the mouse. This provides the position of the point on each frame of the video. The collected data enables kinematic and energy analysis of the studied object. The software is developed in Python and depends on [Pillow](https://pypi.org/project/pillow/) and [OpenCV](https://pypi.org/project/opencv-python/).

## Installation

Download the latest [release](https://gitlab.emi.u-bordeaux.fr/tipiault/videotracker_g1/-/releases) or clone the repository with `git clone git@gitlab.emi.u-bordeaux.fr:tipiault/videotracker_g1.git`. In the application folder, run:

```sh
pip install -r requirements.txt
python src/Application.py
```

## Features

- Set the origin and scale of the reference frame
- Display graphs for x(t), y(t), and y(x)
- Display obtained values in a table
- Save data in CSV format
- Play the video fully or frame by frame
- Keyboard shortcuts to load a video and exit the application

## Known Bugs

- Loading a new video while another video is already loaded currently does not work

## Run Unit Tests

From the project root, with unittest installed:
```sh
python -m unittest discover tests/
```

## Credits 

Directed by Prof. __CASSEAU Christophe__

My team :
- Timeo 
- Yacoub
- Eliott