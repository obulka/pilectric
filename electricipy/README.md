# electricipy

This module allows for easy control over a variety of hardware components.


## Setup

1. This project's dependencies are managed by pipenv. If you just want to run the project, run: `pipenv install`

2. For development, enter the virtual environment by running: `pipenv shell`

3. If it is your first time in the virtual environment run: `pipenv sync --dev`

## Examples

### Connect to Camera

This example connects to a Sony camera and takes a picture. Before running this you must turn on the camera and go to Menu->Application List->Smart Remote Embedded.

```python
from libsonyapi import Actions
from electricipy.cameras.sony import SonyCamera

camera = SonyCamera(network_interface="wlan0")
camera.iso = 400
camera.shutter_speed = 0.1
camera.take_picture()
```

### Intervalometer

This example connects to a camera and takes 10 pictures, with a delay of 1 second in between.

```python
import time

from libsonyapi import Actions

from electricipy.cameras.intervalometer import Intervalometer
from electricipy.cameras.sony import SonyCamera

camera = SonyCamera(
    shutter_speed=1,
    iso=400,
    network_interface="wlan0",
)

intervalometer = Intervalometer(camera, 10, delay=1)
intervalometer.start()

while intervalometer.running:
    print("Still running...")
    time.sleep(5)
```