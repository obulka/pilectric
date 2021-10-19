"""
Copyright 2021 Owen Bulka

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from fractions import Fraction

from libsonyapi import Actions
from libsonyapi import Camera as SonyCameraAPI

from ..camera import Camera


class SonyCamera(SonyCameraAPI, Camera):
    """ Class to control a Sony camera """

    def __init__(
            self,
            shutter_speed=None,
            iso=None,
            network_interface=None,
            sensor=None,
            disable_auto_iso=True):
        """ Create a connection to interface with a sony camera.

        Keyword Args:
            shutter_speed (float): The shutter speed in seconds.
            iso (int): The initial ISO.
            network_interface (str): The network interface to use when
                connecting to the camera.
            sensor (electricipy.cameras.sensors.sensor.Sensor): The sensor
                used by the camera.
            disable_auto_iso (bool): If True the ISO will be
                automatically set, disabling AUTO.

        Raises:
            requests.exceptions.ConnectionError: If the camera cannot be
                connected to.
            libsonyapi.camera.NotAvailableError: If the camera is not
                available.
        """
        SonyCameraAPI.__init__(self, network_interface=network_interface)

        self._disable_auto_iso = disable_auto_iso

        if shutter_speed is not None:
            self.shutter_speed = shutter_speed

        if iso is not None:
            self.iso = iso

        Camera.__init__(
            self,
            self.shutter_speed,
            self.iso_to_gain(self.iso),
            sensor=sensor,
        )

    @property
    def iso(self):
        """int: The camera's iso. """
        iso = self.do(Actions.getIsoSpeedRate)
        if iso == "AUTO":
            self.do(Actions.actHalfPressShutter)
            iso = self.do(Actions.getIsoSpeedRate)
            self.do(Actions.cancelHalfPressShutter)

            if self._disable_auto_iso:
                self.do(Actions.setIsoSpeedRate, iso)

        return int(iso)

    @iso.setter
    def iso(self, new_iso):
        if self.do(Actions.setIsoSpeedRate, str(new_iso)) == 0:
            if new_iso == "AUTO":
                self.do(Actions.actHalfPressShutter)
                new_iso = self.do(Actions.getIsoSpeedRate)
                self.do(Actions.cancelHalfPressShutter)

                if self._disable_auto_iso:
                    self.do(Actions.setIsoSpeedRate, new_iso)

            self._gain = self.iso_to_gain(int(new_iso))

    @property
    def shutter_speed(self):
        """float: The camera's shutter speed in seconds."""
        shutter_speed = self.do(Actions.getShutterSpeed)
        if shutter_speed == "BULB":
            return shutter_speed

        self._shutter_speed = float(Fraction(shutter_speed.strip('"')))

        return self._shutter_speed

    @shutter_speed.setter
    def shutter_speed(self, new_shutter_speed):
        shutter_speed = new_shutter_speed

        if isinstance(shutter_speed, list):
            shutter_speed = shutter_speed[0]

        if isinstance(shutter_speed, (float, int)):
            if shutter_speed < 0.4:
                shutter_speed = str(Fraction(shutter_speed).limit_denominator())

            else:
                shutter_speed = str(shutter_speed) + '"'

        elif not isinstance(shutter_speed, str):
            return

        if self.do(Actions.setShutterSpeed, shutter_speed) == 0:
            self._shutter_speed = float(Fraction(shutter_speed.strip('"')))

    def take_picture(self):
        """ Take a picture """
        self.do(Actions.actTakePicture)